# -*- coding: utf-8 -*-

from odoo import models, fields, api


class opResultLineInherit(models.Model):
    _inherit = 'op.result.line'
    @api.multi
    @api.depends('marks')
    def _compute_grade(self):
        for record in self:
            grades = self.env['op.grade.configuration']
            for grade in grades:
                if grade.min_per <= record.marks and \
                        grade.max_per >= record.marks:
                    record.grade = grade.result

class opMarkSheetLineInherit(models.Model):
    _inherit = 'op.marksheet.line'
    @api.multi
    @api.depends('percentage')
    def _compute_grade(self):
        grades = self.env['op.grade.configuration'].search([])
        for record in self:

            for grade in grades:
                if grade.min_per <= record.total_marks and \
                        grade.max_per >= record.total_marks:
                    record.grade = grade.result