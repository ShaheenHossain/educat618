# -*- coding: utf-8 -*-
{
    'name': "eschool",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        this module is designed for DSBLSC
    """,

    'author': "SM Ashraf",
    'website': "http://www.eagle-it-services.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.9',
    "application": True,
    # any module necessary for this one to work correctly
    'depends': ['base','openeducat_erp','openeducat_core','openeducat_admission','report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'data/eschool.course.division.csv',
        'data/eschool.level.csv',
        'data/eschool.religion.csv',
        'data/op.batch.csv',
        'data/op.category.csv',
        # 'data/op.grade.configuration.csv',
        'data/eschool.class.section.csv',
        # 'data/op.student.csv',

        'report/tabulation.xml',
        'report/report_menu.xml',
        'report/some.xml',
        'report/report_student_idcards.xml',

        'data/op.batch.csv',
        'data/op.course.csv',
        # 'views/campus.xml',
        'views/admission.xml',
        'views/attendance.xml',
        'views/course.xml',
        'views/views.xml',
        'views/exam.xml',
        'views/subject.xml',
        'views/student.xml',
        'views/templates.xml',
        'wizards/tabulation_wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}