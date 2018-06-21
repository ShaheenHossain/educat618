{
    'name': 'Eagle Education Fees',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Fees',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_core', 'account_accountant'],
    'data': [
        'views/fees_terms_view.xml',
        'views/student_view.xml',
        'views/course_view.xml',
        'security/fees_security.xml',
        'security/ir.model.access.csv'
    ],
    'images': [
        'static/description/openeducat_fees_banner.jpg',
    ],
    'demo': [
        'demo/fees_terms_line_demo.xml',
        'demo/fees_terms_demo.xml',
        'demo/course_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
