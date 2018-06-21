{
    'name': 'Eagle Education Support',
    'category': 'Planner',
    'summary': 'Help to configure OpenEduCat',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    "sequence": 3,
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['web'],
    'data': [
        'views/web_planner_templates.xml',
    ],
    'qweb': ['static/src/xml/web_planner.xml', 'static/src/xml/web.xml'],
    'images': [
        'static/description/openeducat_support_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
}
