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
    objective=fields.Boolean("Objective ?")
    total_mark=fields.Integer('Total Mark')
    total_pass_mark=fields.Integer('Total Pass Mark')
    tutorial_mark=fields.Integer('Tutorial Mark')
    tutorial_pass_mark=fields.Integer('Tutorial Pass Mark')
    # theory_mark=fields.Integer('Theory Mark')
    # theory_pass_mark=fields.Integer('Theory Pass Mark')

    subjective_mark=fields.Integer('Subjective Mark')
    subjective_pass_mark=fields.Integer('Subjective Pass Mark')

    objective_mark=fields.Integer('Objective Mark')
    objective_pass_mark=fields.Integer('Objective Pass Mark')

    practical_mark = fields.Integer('Practical Mark')
    practical_pass_mark = fields.Integer('Practical Pass Mark')

    batch_id=fields.Many2one('op.batch',"Batch",required=True)
    syllabus=fields.Binary('Syllabus')
    @api.multi
    def justify_total_mark(self):
        for r in self:
            totalMark=r.tutorial_mark+r.subjective_mark + r.objective_mark +r.practical_mark
            totalPassMark=r.tutorial_pass_mark+r.subjective_pass_mark+r.objective_pass_mark +r.practical_pass_mark
            if r.total_mark!=totalMark:
                raise ValidationError(("Error ! Sum of tutorial, subjectiv,objective and practical mark is not equals Total mark!"))
            elif r.total_pass_mark!=totalPassMark:
                raise ValidationError(("Error ! Sum of tutorial, subjectiv,objective and practical Pass mark is not equals Total Pass mark!"))



    @api.onchange('type')
    def type_changed(self):
        for r in self:
            if r.type == 'practical':
                r.subjective_mark = 0
                r.subjective_pass_mark = 0
                r.objective_mark = 0
                r.objective_pass_mark = 0
            elif r.type=='theory':
                r.practical_mark=0
                r.practical_pass_mark=0
    @api.onchange('objective')
    def objective_changed(self):
        for r in self:
            if r.objective == False:
                r.objective_mark = 0
                r.objective_pass_mark = 0



class eschoolSubjectRegistration(models.Model):
    _inherit='op.subject.registration'
    _description = 'op.subject.registration Inherit'
    classes_id = fields.Many2one('eschool.classes', 'Class Section', required=True)
    section_id = fields.Many2one('eschool.class.section', 'Section')
    active = fields.Boolean('Active ?',related='batch_id.active')
    @api.onchange('student_id')
    def get_course_batch(self):
        for rec in self.env['op.student.course'].search([('student_id','=',self.student_id.id)]):
            self.course_id = rec.course_id
            self.batch_id=rec.batch_id

    @api.onchange('classes_id')
    def classes_id_changed(self):
        for rec in self:
            rec.section_id = rec.classes_id.section_id.id
            rec.course_id = rec.classes_id.course_id
            rec.batch_id = rec.classes_id.batch_id

            # self.env['op.student.course'].search([('course_id', '=', self.course_id.id)])