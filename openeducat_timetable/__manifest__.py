{
    'name': 'Eagle Education Timetable',
    'version': '10.0.3.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage TimeTables',
    'complexity': "easy",
    'author': 'Md. Shaheen Hossain',
    'website': 'http://www.eagle-erp.com',
    'depends': ['openeducat_classroom'],
    'data': [
        'views/timetable_view.xml',
        'views/timing_view.xml',
        'views/faculty_view.xml',
        'report/report_timetable_student_generate.xml',
        'report/report_timetable_teacher_generate.xml',
        'report/report_menu.xml',
        'wizard/generate_timetable_view.xml',
        'wizard/time_table_report.xml',
        'dashboard/timetable_student_dashboard.xml',
        'dashboard/timetable_faculty_dashboard.xml',
        'security/ir.model.access.csv',
        'security/op_timetable_security.xml',
        'timetable_menu.xml',
        'wizard/session_confirmation.xml',
        'views/timetable_templates.xml',
    ],
    'demo': [
        'demo/timing_demo.xml',
        'demo/op_timetable_demo.xml'
    ],
    'test': [
        'test/timetable_sub_value.yml',
        'test/generate_timetable.yml'
    ],
    'images': [
        'static/description/openeducat_timetable_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
