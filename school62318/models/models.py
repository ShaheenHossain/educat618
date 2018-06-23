# -*- coding: utf-8 -*-

from odoo import models, fields, api

class eschool_res_company(models.Model):
    _inherit='res.company'
    email_suffix = fields.Char('Default Email Suffix for New Contacts',default='dsblsc.com')

class opCourse(models.Model):
    _inherit = 'op.course'
    # medium_id=fields.Many2one('eschool.medium',required=True)
    name=fields.Char('Name',required=True)
    # standard_id = fields.Many2one('eschool.standard','Class', required=True)
    batch_id=fields.Many2one('op.batch','Batch',required=True)
    code=fields.Char('Code',size=30)
    parent_id = fields.Many2one('op.course',"Next Class")
    _sql_constraints = [
        ('unique_course',
         'unique(name)',
         'class must be unique!'),
    ]
class opbatchInherit(models.Model):
    _inherit = 'op.batch'
    current=fields.Boolean("Current", help="Set Batch Active")
    code = fields.Char('Code', required=True)
    course_id=fields.One2many('op.course','batch_id','Classes')
class opAdmissionInherit(models.Model):
    _inherit = 'op.admission'

    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.product_id.lst_price
        self.batch_id=self.course_id.batch_id
    @api.onchange('name')
    def generate_email(self):
            self.email = '%s.%s@dsblsc.com' %(self.name,self.application_number)
            self.country_id=20

    @api.onchange('course_id')
    def onchange_course(self):
        # self.batch_id = False
        term_id = False
        if self.course_id and self.course_id.fees_term_id:
            term_id = self.course_id.fees_term_id.id
        self.fees_term_id = term_id
class insertStudentsforAttendance(models.Model):
    _inherit = 'op.attendance.sheet'
    got_student=fields.Boolean('Got Student?')

    @api.multi
    def get_students(self):
        student_in_course= self.env['op.student.course'].search([('course_id','=',self.course_id.id)])
        for student in student_in_course:
            self.env['op.attendance.line'].create({'attendance_id': self.id,'student_id':student.student_id.id,'register_id':self.register_id,'batch_id': self.batch_id.id,'present': True})
        self.got_student=True