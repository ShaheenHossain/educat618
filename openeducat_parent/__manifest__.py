{
    'name': 'Eagle Education Parent',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Parent',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_core'],
    'data': [
        'security/op_parent_security.xml',
        'data/parent_user_data.xml',
        'views/parent_view.xml',
        'parent_menu.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/res_users_demo.xml',
        'demo/parent_demo.xml',
    ],
    'images': [
        'static/description/openeducat_parent_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
