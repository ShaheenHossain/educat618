# -*- coding: utf-8 -*-

from odoo import models, fields, api

class opExamInherit(models.Model):
    _inherit = 'op.exam.session'
    generated=fields.Boolean('Generated?')
    @api.multi
    def get_exams(self):
        rec = self.env['op.subject'].search([('course_id','=',self.course_id.id),('batch_id','=',self.batch_id.id)])
        # Here create Exams
        for subject in rec:
            self.env['op.exam'].create(
                {'session_id': self.id, 'course_id': self.course_id.id, 'subject_id': subject.id,
                 'batch_id': self.batch_id.id,'min_marks':subject.total_pass_mark,'total_marks':subject.total_mark ,
                 'name':self.name +' '+self.course_id.name+' '+subject.name,'state':'draft',
                 'start_time': self.start_date,'end_time': self.start_date,'exam_code':self.exam_code+self.course_id.code+subject.code})
        self.generated=True

class opExamAttendeesInherit(models.Model):
    _inherit='op.exam.attendees'
    practical_mark=fields.Integer('Practical')
    subjective_mark=fields.Float('Subjective')
    objective_mark=fields.Float('Objective')
    marks = fields.Integer('Marks',compute='compute_total_mark')


    @api.one
    def compute_total_mark(self):
        self.marks=self.practical_mark +self.subjective_mark+self.objective_mark
class OpGradeConfigurationInherit(models.Model):
    _inherit='op.grade.configuration'
    score=fields.Float('Score')
