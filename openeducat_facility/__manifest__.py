{
    'name': 'Eagle Education Facility',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Facility',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_core'],
    'data': [
        'views/facility_view.xml',
        'views/facility_line_view.xml',
        'security/ir.model.access.csv',
        'facility_menu.xml',
    ],
    'demo': [
        'demo/facility_demo.xml'
    ],
    'images': [
        'static/description/openeducat_facility_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
