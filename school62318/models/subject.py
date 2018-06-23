# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
class eschoolSubjectGroup(models.Model):
    _name = 'eschool.subject.group'
    _description='Subject Group'
    name=fields.Char("Subject Group")
    description=fields.Text("Description")


class eschoolsubject(models.Model):
    _inherit = 'op.subject'
    subject_group=fields.Many2one('eschool.subject.group','Subject Group')
    objective=fields.Boolean("Subjective/Objective")
    total_mark=fields.Integer('Total Mark')
    total_pass_mark=fields.Integer('Total Pass Mark')
    practical_mark=fields.Integer('Practical Mark')
    practical_pass_mark=fields.Integer('Practical Pass Mark')
    theory_mark=fields.Integer('Theory Mark')
    subjective_mark=fields.Integer('Subjective Mark')
    subjective_pass_mark=fields.Integer('Subjective Pass Mark')
    objective_mark=fields.Integer('Objective Mark')
    objective_pass_mark=fields.Integer('Objective Pass Mark')
    theory_pass_mark=fields.Integer('Theory Pass Mark')
    batch_id=fields.Many2one('op.batch',"Batch",required=True)
    syllabus=fields.Binary('Syllabus')
    @api.onchange('total_mark','type','total_pass_mark')
    def justify_total_mark(self):
        if self.type == 'theory':
            self.theory_mark=self.total_mark
            self.practical_mark = 0
            self.theory_pass_mark = self.total_pass_mark
            self.practical_pass_mark = 0
            if self.objective==False:
                self.subjective_mark=self.theory_mark
                self.objective_mark=0
                self.subjective_pass_mark=self.theory_pass_mark
                self.objective_pass_mark=0
        elif self.type == 'practical':
            self.practical_mark=self.total_mark
            self.theory_mark =0
            self.practical_pass_mark = self.total_pass_mark
            self.theory_pass_mark = 0

    @api.onchange('practical_mark', 'type')
    def justify_practical_mark(self):
        if self.type == 'both':
            self.theory_mark = self.total_mark-self.practical_mark
    @api.onchange('theory_mark', 'type')
    def justify_theory_mark(self):
        if self.type == 'both':
            self.practical_mark = self.total_mark-self.theory_mark
    @api.onchange('practical_pass_mark', 'type')
    def justify_practical_pass_mark(self):
        if self.type == 'both':
            self.theory_pass_mark = self.total_pass_mark-self.practical_pass_mark
    @api.onchange('theory_pass_mark', 'type')
    def justify_theory_pass_mark(self):
        if self.type == 'both':
            self.practical_pass_mark = self.total_pass_mark-self.theory_pass_mark

    @api.constrains('practical_pass_mark')
    def _check_marks(self):
        if self.practical_mark<self.practical_pass_mark:
            raise ValidationError(("Error ! pass mark cann't be greater than total mark , check practical marks."))
        elif self.theory_mark<self.theory_pass_mark:
            raise ValidationError(("Error ! pass mark cann't be greater than total mark , check Theory marks."))
        elif self.theory_mark+self.practical_mark>self.total_mark:
            raise ValidationError(("Error ! sum of practical and theory is greater than Total !"))
        elif self.theory_pass_mark+self.practical_pass_mark>self.total_pass_mark:
            raise ValidationError(("Error ! sum of practical and theory pass mark is greater than Total !"))

        return True
    @api.onchange('subjective_mark','subjective_pass_mark')
    def check_subjective_marks(self):
        self.objective_mark=self.theory_mark-self.subjective_mark
        self.objective_pass_mark = self.theory_pass_mark - self.subjective_pass_mark


    @api.onchange('objective_mark', 'objective_pass_mark')
    def check_objective_marks(self):
        self.subjective_mark = self.theory_mark - self.objective_mark

        self.subjective_pass_mark = self.theory_pass_mark - self.objective_pass_mark


class eschoolSubjectRegistration(models.Model):
    _inherit='op.subject.registration'
    _description = 'op.subject.registration Inherit'

    @api.onchange('student_id')
    def get_course_batch(self):
        for rec in self.env['op.student.course'].search([('student_id','=',self.student_id.id)]):
            self.course_id = rec.course_id
            self.batch_id=rec.batch_id

            # self.env['op.student.course'].search([('course_id', '=', self.course_id.id)])