
{
    'name': 'Classroom',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Classroom',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_core', 'openeducat_facility', 'product'],
    'data': [
        'views/classroom_view.xml',
        'classroom_menu.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/classroom_demo.xml',
        'demo/facility_line_demo.xml'
    ],
    'images': [
        'static/description/openeducat_classroom_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
