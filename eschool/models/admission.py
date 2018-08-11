# -*- coding: utf-8 -*-

from odoo import models, fields, api


class opadmissioninherit(models.Model):
    _inherit = 'op.admission'
    classes_id=fields.Many2one('eschool.classes',"Class")
    section_id=fields.Many2one('eschool.class.section',"section")
    roll_no=fields.Integer('Roll No')