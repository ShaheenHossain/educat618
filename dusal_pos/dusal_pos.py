# -*- coding: utf-8 -*-
##############################################################################
#
#    Addon for Odoo sale by Dusal.net
#    Copyright (C) 2015 Dusal.net Almas
#
##############################################################################


import openerp
from openerp import SUPERUSER_ID
from openerp import tools
from openerp import fields, osv
from openerp import models

class pos_config(models.Model):
    _inherit = 'pos.config'

    print_company_logo = fields.Boolean('Print company logo', readonly=False, help="Print company logo on receipt", default=False)
    print_orderno_barcode = fields.Boolean('Print barcode', readonly=False, help="Print POS order number as barcode on receipt", default=False)
    # one_click_pays = fields.Char('One click pays', help="Additional buttons for keypad. k means thousand and need to seperate comma.", default='100,500,1k,5k,10k,20k,40k,50k,100k')
    max_payment_limit = fields.Integer('Cash payment limit', default=0, help="Max cash payment limit", size=20)
    hide_price_button = fields.Boolean("Hide \"Price\" button", default=False)
    hide_discount_button = fields.Boolean("Hide \"Discount\" button", default=False)
    zero_product = fields.Selection([('hide', 'Hide'), ('restrict', 'Restrict to sell')], string='Out of Stock Products Handling', help="Manage Out of Stock Products")
    categorize_receipt = fields.Boolean("Categorize products on receipt", default=False)
