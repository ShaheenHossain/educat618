# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpAdmissionRegister(models.Model):
    _name = 'op.admission.register'
    _inherit = 'mail.thread'
    _description = 'Admission Register'

    name = fields.Char(
        'Name', required=True, readonly=True,
        states={'draft': [('readonly', False)]})
    start_date = fields.Date(
        'Start Date', required=True, readonly=True,
        default=fields.Date.today(), states={'draft': [('readonly', False)]})
    end_date = fields.Date(
        'End Date', required=True, readonly=True,
        default=(datetime.today() + relativedelta(days=30)),
        states={'draft': [('readonly', False)]})
    course_id = fields.Many2one(
        'op.course', 'Course', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, track_visibility='onchange')
    min_count = fields.Integer(
        'Minimum No. of Admission', readonly=True,
        states={'draft': [('readonly', False)]})
    max_count = fields.Integer(
        'Maximum No. of Admission', readonly=True,
        states={'draft': [('readonly', False)]}, default=30)
    product_id = fields.Many2one(
        'product.product', 'Product', required=True,
        domain=[('type', '=', 'service')], readonly=True,
        states={'draft': [('readonly', False)]}, track_visibility='onchange')
    admission_ids = fields.One2many(
        'op.admission', 'register_id', 'Admissions')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('cancel', 'Cancelled'), ('application', 'Application Gathering'),
         ('admission', 'Admission Process'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')

    @api.multi
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = fields.Date.from_string(record.end_date)
            if start_date > end_date:
                raise ValidationError(_("End Date cannot be set before \
                Start Date."))

    @api.multi
    @api.constrains('min_count', 'max_count')
    def check_no_of_admission(self):
        for record in self:
            if (record.min_count < 0) or (record.max_count < 0):
                raise ValidationError(_("No of Admission should be positive!"))
            if record.min_count > record.max_count:
                raise ValidationError(_(
                    "Min Admission can't be greater than Max Admission"))

    @api.multi
    def confirm_register(self):
        self.state = 'confirm'

    @api.multi
    def set_to_draft(self):
        self.state = 'draft'

    @api.multi
    def cancel_register(self):
        self.state = 'cancel'

    @api.multi
    def start_application(self):
        self.state = 'application'

    @api.multi
    def start_admission(self):
        self.state = 'admission'

    @api.multi
    def close_register(self):
        self.state = 'done'
