# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProjectScrumSandbox(models.Model):
    _name = 'project.scrum.sandbox'
    _description = 'Project Scrum Sandbox'

    role_id = fields.Many2one('res.partner', "Who", required=True)
    name = fields.Char('Wants', required=True)
    for_then = fields.Char('For', required=True)
    project_id = fields.Many2one(
        'project.project',
        "Project",
        required=True,
        domain=[('is_scrum', '=', True)]
    )
    developer_id = fields.Many2one(
        'res.users',
        'Author',
        default=lambda self: self.env.user
    )
    create_date = fields.Date('Date taken')
    meeting_id = fields.Many2one(
        'project.scrum.meeting',
        'Meeting'
    )
