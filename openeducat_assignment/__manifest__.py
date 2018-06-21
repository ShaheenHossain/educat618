{
    'name': 'Eagle Education Assignment',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Assgiments',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_core', 'base_action_rule'],
    'data': [
        'security/ir.model.access.csv',
        'security/op_assignment_security.xml',
        'views/assignment_view.xml',
        'views/assignment_type_view.xml',
        'views/assignment_sub_line_view.xml',
        'views/student_view.xml',
        'dashboard/assignment_student_dashboard.xml',
        'dashboard/assignment_faculty_dashboard.xml',
        'assignment_menu.xml',
        'data/action_rule_data.xml',
    ],
    'demo': [
        'demo/assignment_type_demo.xml',
        'demo/assignment_demo.xml',
        'demo/assignment_sub_line_demo.xml'
    ],
    'test': [
        'test/res_users_test.yml',
        'test/assignment_sub_values.yml',
        'test/assignment_creation_submission.yml'
    ],
    'images': [
        'static/description/openeducat_assignment_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
