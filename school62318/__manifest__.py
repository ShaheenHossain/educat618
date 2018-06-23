# -*- coding: utf-8 -*-
{
    'name': "eschool",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SM Ashraf",
    'website': "http://www.eagle-it-services.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    "application": True,
    # any module necessary for this one to work correctly
    'depends': ['base','openeducat_erp','openeducat_core','openeducat_admission'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/eschool.standard.csv',
        # 'data/eschool.medium.csv',


        'reports/report_menu.xml',
        'reports/report_student_idcards.xml',

        # 'data/op.batch.csv',
        # 'data/op.course.csv',
        # 'views/campus.xml',
        'views/views.xml',
        'views/exam.xml',
        'views/subject.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}