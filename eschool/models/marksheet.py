# -*- coding: utf-8 -*-

from odoo import models, fields, api

class opMarksheetLineInherit(models.Model):
    _inherit = 'op.marksheet.line'


    @api.multi
    @api.depends('percentage')
    def _compute_grade(self):
        for record in self:
            grades = record.marksheet_reg_id.result_template_id.grade_ids
            for grade in grades:
                if grade.min_per <= record.percentage and \
                        grade.max_per >= record.percentage:
                    record.grade = grade.result
