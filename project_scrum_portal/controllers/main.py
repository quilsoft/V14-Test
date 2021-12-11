# See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from datetime import datetime

from odoo import http, fields,_
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request


class CustomerPortal(CustomerPortal):

    @http.route(['/my/projects', '/my/projects/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_projects(self, page=1, date_begin=None, date_end=None,
                           sortby=None, **kw):
        result = super(CustomerPortal, self).portal_my_projects(
            page=1, date_begin=date_begin, date_end=date_end, sortby=sortby,
            **kw)
        project_val = ''
        if request.params and request.params.get('project', False):
            project_val = '?project=' + str(request.params.get('project'))
        result.qcontext.update({
            'project_val': project_val,
        })
        return result

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None,
                        project=None, sortby=None, **kw):
        result = super(CustomerPortal, self).portal_my_tasks(
            page=1, date_begin=date_begin, date_end=date_end, project=project,
            sortby=sortby, **kw)
        project_val = ''
        domain = [('project_id.privacy_visibility', '=', 'portal')]
        domain += [('project_id.id', '=', request.params.get('project'))]
        tasks = request.env['project.task'].search(domain)
        if request.params and request.params.get('project', False):
            project_val = '?project=' + str(request.params.get('project'))
        result.qcontext.update({
            'project_val': project_val,
            'tasks': tasks,
        })
        return result

    @http.route(['/my/sprints'], type='http', auth='user', website=True)
    def my_sprints(self, **post):
        project_val = ''
        if request.params and request.params.get('project', False):
            project_val = '?project=' + str(request.params.get('project'))
        stg_new = {}
        stage_lst = []
        sprints = request.env['project.scrum.sprint'].sudo().search(
            [('project_id.id', '=', post.get('project'))])
        product_backlog = request.env[
            'project.scrum.product.backlog'].sudo().search(
            [('project_id.id', '=', post.get('project')),
             ('sprint_id', '=', False)
             ])
        tags_id = request.env['project.tags'].sudo().search([])
        project_ids = request.env['project.project'].sudo().search([])
        release_ids = request.env['project.scrum.release'].sudo().search([])
        user_ids = request.env['res.users'].sudo().search([])
        responsible_ids = request.env['res.users'].sudo().search([])
        hr_job_ids = request.env['hr.job'].sudo().search([])
        for task in sprints:
            if task in stg_new:
                stg_new[task].append(task.id)
            else:
                stg_new[task] = [task.id]
        if stg_new:
            for key, value in stg_new.items():
                state = ''
                if key.state == 'draft':
                    state = 'Draft'
                elif key.state == 'open':
                    state = 'Open'
                elif key.state == 'pending':
                    state = 'Pending'
                elif key.state == 'cancel':
                    state = 'Cancel'
                elif key.state == 'done':
                    state = 'Done'
                data = {
                    'stage': key.name,
                    'stage_id': key.id,
                    'state': state,
                    'start_date': key.date_start,
                    'end_date': key.date_stop
                }
                stage_lst.append(data)
        return request.render('project_scrum_portal.my_sprints', {
            'sprints': sprints,
            'project_val': project_val,
            'product_backlog': product_backlog,
            'sprints_kanban': stage_lst,
            'tags': tags_id,
            'projects': project_ids,
            'release': release_ids,
            'author': user_ids,
            'responsible': responsible_ids,
            'role2': hr_job_ids
        })

    @http.route(['/my/backlogs'], type='http', auth='user', website=True)
    def my_backlogs(self, **post):
        """This method returns backlogs's detail"""
        backlogs_lst = []
        stg_new = {}
        project_val = ''
        if request.params and request.params.get('project', False):
            project_val = '?project=' + str(request.params.get('project'))
        backlogs = request.env['project.scrum.product.backlog'].sudo().search([
            ('project_id.id', '=', post.get('project'))])
        for backlog in backlogs:
            if backlog.stage_id in stg_new:
                stg_new[backlog.stage_id].append(backlog.stage_id.id)
            else:
                stg_new[backlog.stage_id] = [backlog.stage_id.id]
        if stg_new:
            for key, value in stg_new.items():
                state = ''
                if key.name:
                    state = key.name
                else:
                    state = 'Undefined'
                data = {
                    'stage': state,
                    'stage_id': key.id
                }
                backlogs_lst.append(data)
        return request.render("project_scrum_portal.my_backlogs", {
            'backlogs': backlogs_lst,
            'project_val': project_val
        })

    @http.route('/update_backlog_stage', type='json', auth='user',
                website=True)
    def update_backlog_stage(self, **post):
        backlog_obj = request.env['project.scrum.product.backlog']
        if post.get('backlog_id'):
            backlog = backlog_obj.sudo().search(
                [('id', '=', post.get('backlog_id'))])
            if backlog:
                backlog.sudo().write({'stage_id': post.get('target_id')})
        return True

    @http.route(['/my/meetings'], type='http', auth='user', website=True)
    def my_meetings(self, **post):
        dict = {}
        dates = []
        cookie_value = request.httprequest.cookies.get('project_id_cookie')
        meetings = request.env['project.scrum.meeting'].sudo().search([
            ('user_id', '=', request.env.user.id),
            ('project_id.id', '=', post.get('project'))])
        project_val = ''
        if request.params and request.params.get('project', False):
            project_val = '?project=' + str(request.params.get('project'))
        for meeting in meetings:
            if not meeting.allday:
                if dict.get(meeting.start and fields.Date.to_string(meeting.start)[:10], False):
                    dict[meeting.start[:10]].append(meeting.id)
                else:
                    dict.update({meeting.start and fields.Date.to_string(meeting.start)[:10]: [meeting.id]})
            else:
                if dict.get(meeting.start_date, False):
                    dict[meeting.start_date].append(meeting.id)
                else:
                    dict.update({meeting.start_date: [meeting.id]})
        if dict:
            for key, value in dict.items():
                data = {
                    'meeting_date': key,
                    'meeting_id': value
                }
                dates.append(data)
        return request.render('project_scrum_portal.my_meetings', {
            'meetings': meetings,
            'meeting_dates': dates,
            'cookie_value': cookie_value,
            'project_val': project_val
        })

    @http.route('/update_sprint_stage', type='json', auth='user', website=True)
    def update_sprint_stage(self, **post):
        backlog_obj = request.env['project.scrum.product.backlog']
        if post.get('sprint_id'):
            backlog = backlog_obj.sudo().search(
                [('id', '=', post.get('sprint_id'))])
            if backlog:
                backlog.sudo().write(
                    {'sprint_id': post.get('target_id'), 'state': ''})
        return True

    @http.route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, page=1, date_begin=None, date_end=None, project=None,
             sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'),
                       'order': 'date_last_stage_update desc'},
        }
        project_val = ''
        if request.params and request.params.get('project', False):
            project_val = '?project=' + str(request.params.get('project'))
        projects = request.env['project.project'].search(
            [('privacy_visibility', '=', 'portal')])
        cookie_value = request.httprequest.cookies.get('project_id_cookie')
        project_filters = {
            # 'all': {'label': '', 'domain': []},
        }
        for proj in projects:
            project_filters.update({
                str(proj.id): {'label':proj.name,
                               'domain': [('project_id', '=', proj.id)]}
            })
        domain = [('project_id.privacy_visibility', '=', 'portal')]
        # domain += project_filters.get(project, project_filters['all'])[
        #     'domain']
        order = sortings.get(sortby, sortings['date'])['order']
        # archive groups - Default Group By 'create_date'
#         archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin),
                       ('create_date', '<=', date_end)]
        # pager
        pager = request.website.pager(
            url="/my/home",
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'project': project},
            total=request.env['project.task'].search_count([]),
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        tasks = request.env['project.task'].search(domain, order=order,
                                                   limit=self._items_per_page,
                                                   offset=pager['offset'])
        default_sprints = False
        sprints = request.env['project.scrum.sprint'].sudo().search(
            [('project_id.id', '=', request.params.get('project'))])
        for spr in sprints:
            if spr.state == 'open':
                default_sprints = \
                request.env['project.scrum.sprint'].sudo().search(
                    [('state', '=', 'open'),
                     ('project_id.id', '=', request.params.get('project'))])[
                    0].id
            else:
                default_sprints = \
                request.env['project.scrum.sprint'].sudo().search(
                    [('project_id.id', '=', request.params.get('project'))])[
                    0].id
        project_dashbord = request.env['project.project'].sudo().search(
            [('id', '=', request.params.get('project'))])
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'project_filters': OrderedDict(sorted(project_filters.items())),
            'projects': projects,
            'project': project,
            'sortings': sortings,
            'sortby': sortby,
            'tasks': tasks,
            'sprints': sprints,
            'project_dashbord': project_dashbord,
            'page_name': 'task',
#             'archive_groups': archive_groups,
            'default_url': '/my/home',
            'pager': pager,
            'cookie_value': cookie_value,
            'project_val': project_val,
            'default_sprints': default_sprints
        })
        return request.render("portal.portal_my_home", values)

    @http.route('/get_sprint_data', type='json', auth='user', website=True)
    def get_sprint_data(self, **post):
        burndown_list1 = []
        burndown_list2 = []
        stg_new = {}
        if post.get('sprint_id'):
            domain = [('sprint_id', '=', int(post.get('sprint_id')))]
            burndown = request.env[
                'project.scrum.sprint.burndown.log'].sudo().search(domain)
            for burn in burndown:
                if burn in stg_new:
                    stg_new[burn].append(burn.id)
                else:
                    stg_new[burn] = [burn.id]
            if stg_new:
                a1_sorted_keys = sorted(stg_new, key=stg_new.get)
                for r in a1_sorted_keys:
                    data = {
                        'label': r.date,
                        'y': r.remaining_points
                    }
                    burndown_list1.append(data)
                    data1 = {
                        'label': r.date,
                        'y': r.remaining_hours
                    }
                    burndown_list2.append(data1)
        result = {'remaining_points': burndown_list1,
                  'remaining_hours': burndown_list2}
        return result

    @http.route('/get_sprint_wise_data', type='json', auth='user',
                website=True)
    def get_sprint_wise_data(self, **post):
        sprint_list1 = []
        sprint_list2 = []
        stg_new = {}
        result = {}
        if post.get('project_id'):
            domain = [('project_id', '=', int(post.get('project_id')))]
            sprints = request.env['project.scrum.sprint'].sudo().search(domain)
            for sprint in sprints:
                if sprint in stg_new:
                    stg_new[sprint].append(sprint.id)
                else:
                    stg_new[sprint] = [sprint.id]
            if stg_new:
                a1_sorted_keys = sorted(stg_new, key=stg_new.get)
                for r in a1_sorted_keys:
                    data = {
                        'label': r.name,
                        'y': r.expected_hours
                    }
                    sprint_list1.append(data)
                    data1 = {
                        'label': r.name,
                        'y': r.effective_hours
                    }
                    sprint_list2.append(data1)
#         result = {'estimated_hours': sprint_list1, 'spent_hours': sprint_list2}
            result = {'sprint_data': [sprint.get('label') for sprint in sprint_list1], 
                    'expected_hrs': [expect.get('y') for expect in sprint_list1], 
                    'effective_hrs': [effect.get('y') for effect in sprint_list2]}
        return result

    @http.route('/get_meeting_data', type='json', auth='user', website=True)
    def get_meeting_data(self, **post):
        meeting_list = []
        meetings = request.env['project.scrum.meeting'].sudo().search([
            ('user_id', '=', request.env.user.id)])
        for scrum in meetings:
            start = datetime.strptime(scrum.start_date,
                                      "%Y-%m-%d %H:%M:%S")
            formate_date = start.strftime('%m-%d-%Y %H:%M:%S')
            data = {
                'title': '[' + scrum.sprint_id.sprint_number + ']' + ' ' +
                         scrum.sprint_id.name,
                'start': formate_date
                }
            meeting_list.append(data)
        return meeting_list

    @http.route('/get_task_data', type='json', auth='user', website=True)
    def get_task_data(self, **post):
        task_list = []
        stg_new = {}
        result = {}
        if post.get('project_id'):
            domain = [('project_id', '=', int(post.get('project_id')))]
            tasks = request.env['project.task'].sudo().search(domain)
            for task in tasks:
                if task.stage_id in stg_new:
                    stg_new[task.stage_id].append(task.stage_id.id)
                else:
                    stg_new[task.stage_id] = [task.stage_id.id]
            if stg_new:
                for key, value in stg_new.items():
                    data = {
                        'label': key.name,
                        'y': len(value)
                    }
                    task_list.append(data)
            result =  {'stages': [task.get('label') for task in task_list], 'stage_data':  [task.get('y') for task in task_list]}
        return result

    @http.route('/get_team_data', type='json', auth='user', website=True)
    def get_team_data(self, **post):
        team_list = []
        stg_new = {}
        result = {}
        if post.get('project_id'):
            projects = request.env['project.project'].sudo().search(
                [('id', '=', int(post.get('project_id')))])
            for project in projects:
                scrums = request.env['project.scrum.devteam'].sudo().search(
                    [('id', '=', project.team_id.id)])
                for scrum in scrums:
                    for scr in scrum.developer_ids:
                        if scr in stg_new:
                            stg_new[scr].append(scr.id)
                        else:
                            stg_new[scr] = [scr.id]
                    if stg_new:
                        for key, value in stg_new.items():
                            hours = 0.00
                            user_hours = request.env[
                                'project.task'].sudo().search([
                                ('user_id', '=', key.id),
                                ('project_id', '=',
                                 int(post.get('project_id')))])
                            for hour in user_hours:
                                hours += hour.planned_hours
                            data = {
                                'label': key.name,
                                'y': hours
                            }
                            team_list.append(data)
            result = {'team_member': [task.get('label') for task in team_list],
                       'member_load':  [task.get('y') for task in team_list]}
        return result
