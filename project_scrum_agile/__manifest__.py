# See LICENSE file for full copyright and licensing details.
{
    'name': 'Project Scrum Management Agile Methodology',
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.,David DRAPEAU',
    'category': 'Project Scrum Management',
    'website': "http://www.serpentcs.com",
    'summary': '''
        This application respects the scrum.org protocol
        and has been developed and is maintained by ITIL Certified Member
        (in course of certification).
        ''',
    'description': """This application respects the scrum.org protocol
        and has been developed and is maintained by ITIL Certified Member
        (in course of certification)
        Project Scrum Portal Agile
        agile project management using scrum
		scrum agile project management methodology
		scrum program management
		scrum project methodology
		scrum software open source
		scrum project management methodology
		agile project management with scrum
		project scrum portal agile methodology
		Agile Project Management Software
		Agile project management with Scrum
		Agile Project Management and Scrum
		Agile Project Management
		project scrum portal agile office
		project scrum portal agile online
		project scrum portal agile payroll
		project scrum portal agile software
		project scrum portal agile solutions
		Project Scrum Management Agile Methodology
		Project Scrum Management
		Project Agile Scrum
		scrum task management
		scrum management system 
		scrum management software 
		scrum project management software
		scrum project management
		Project Scrum Management
		project scrum portal agile development
		project scrum portal agile online
		Project Scrum Portal
		Scrum management portal
		Agile Management portal
		project agile
		odoo scrum portal
		Scrum Project
		odoo Project management
		Project scrum management
		Agile
		odoo portal project management
		scrum portal
		odoo scrum agile
		odoo user account
		Scrum methodology
		scrum 
		""",    
    'sequence': 1,
    'depends': [
        'sale_timesheet',
        'calendar',
    ],
    'data': [
        'security/project_scrum_security.xml',
        'security/ir.model.access.csv',
        'views/email_template.xml',
        'views/hr_employee_view.xml',
        'views/project_scrum_view.xml',
        'views/account_analytic_line_view.xml',
        'views/project_scrum_release_view.xml',
        'views/project_view.xml',
        'wizards/user_story_sandbox_to_backlog_view.xml',
        'wizards/project_scrum_backlog_create_task_view.xml',
        'views/project_scrum_sandbox_view.xml',
        'views/project_scrum_role_view.xml',
        'wizards/project_scrum_email_view.xml',
        'wizards/analytic_timesheet_view.xml',
        'views/project_scrum_devteam_view.xml',
    ],
    'demo': ['data/project_scrum_extended_data.xml'],
    'images': ['static/description/Project Scrum Management Agile Methodology_banner.png'],
    'live_test_url': 'https://www.youtube.com/watch?v=5Za9ShZfa5s',
    'installable': True,
    'application': True,
    'price': 145,
    'currency': 'EUR',
}
