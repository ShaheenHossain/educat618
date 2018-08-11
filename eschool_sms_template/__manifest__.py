# -*- coding: utf-8 -*-
{
    'name': "eschool_sms_template",

    'summary': """
        SMS Template for eschool_SMS""",

    'description': """
        Abrief and parfect template to send to the absent student's guardian from school
    """,

    'author': "SM Ashraf",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'SMS',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['eschool_sms'],

    # always loaded
    'data': [
        'data/sms.template.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}