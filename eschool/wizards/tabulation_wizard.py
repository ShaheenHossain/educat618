# -*- coding: utf-8 -*-

from odoo import models, fields, api



class tabulationWizard(models.TransientModel):
    _name = 'eschool.tabulation.wizard'
    _description='filter tabulation data'
    exam_session =fields.Many2one('op.exam.session',"Exam Session")
    course_id=fields.Many2one('op.course',string="Course",related='exam_session.course_id',readonly=True)
    batch_id=fields.Many2one('op.batch',string='Batch',related='exam_session.batch_id',readonly=True)
    section=fields.Many2one('eschool.class.section')

    @api.multi
    def check_report(self):
        data = {}
        data['form'] = self.read(['exam_session', 'course_id', 'batch_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['exam_session', 'course_id', 'batch_id'])[0])
        return self.env['report'].get_action(self, 'eschool.tabulation_report', data=data)