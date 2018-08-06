# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Dusal.net
#
##############################################################################

{
    "name" : "Extension for Point of Sale",
    'summary' : "Display available products count, merge order lines, company logo, barcode on receipt, quantity, hide buttons",
    "version" : "3.2",
    "description": """
        This module extends POS with many useful functions and settings. Contact and support email: almas@dusal.net
    """,
    'author' : 'Dusal Solutions',
    'support': 'almas@dusal.net',
    'license': 'Other proprietary',
    'category' : 'Point of Sale',
    'price': 30,
    'currency': 'EUR',
    'images': ['static/images/main_screenshot.png', 'static/images/screenshot1.png', 'static/images/screenshot.png', 'static/images/screenshot2.png', 'static/images/ss1.png', 'static/images/ss3.png', 'static/images/ss4.png', 'static/images/ss5.png', 'static/images/ss2.png', 'static/images/ss6.png', 'static/images/ss7.png'],
    "depends" : [
                 "point_of_sale",
    ],
    "data" : [  'views/views.xml',
                'views/templates.xml',
                ],
    'qweb': ['static/src/xml/pos.xml',],
    'js': [
        'static/src/js/pos.js',
    ],
    "auto_install": False,
    "installable": True,
}
