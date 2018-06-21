{
    'name': 'Eagle Education Activity',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Activities',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/op_activity_security.xml',
        'wizard/student_migrate_wizard_view.xml',
        'views/activity_view.xml',
        'views/activity_type_view.xml',
        'views/student_view.xml',
        'activity_menu.xml'
    ],
    'demo': [
        'demo/activity_type_demo.xml',
        'demo/activity_demo.xml',
    ],
    'images': [
        'static/description/openeducat_activity_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
