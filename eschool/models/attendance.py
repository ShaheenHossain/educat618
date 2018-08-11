# -*- coding: utf-8 -*-

from odoo import models, fields, api
class OpAttendanceRegister(models.Model):
    _name = 'op.attendance.register'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    id=fields.Integer("id")
    name = fields.Char('Name', size=16, compute='get_name_code', track_visibility='onchange')
    # classes_id = fields.Many2one('eschool.classes', 'Class')

    code = fields.Char('Code', size=16, related='course_id.code')
    course_id = fields.Many2one('op.course', 'Course', required=True, track_visibility='onchange')
    batch_id = fields.Many2one('op.batch', 'Batch', required=True,related='course_id.batch_id', track_visibility='onchange')
    subject_id = fields.Many2one('op.subject', 'Subject', track_visibility='onchange')

    _sql_constraints = [
        ('unique_attendance_register_code',
         'unique(code)', 'Code should be unique per attendance register!')]


    @api.onchange('course_id')
    def get_name_code(self):
        for rec in self:
            rec.name=rec.course_id.name
            rec.code=rec.course_id.code


class insertStudentsforAttendance(models.Model):
    _inherit = 'op.attendance.sheet'
    name = fields.Char('Name', required=True,track_visibility="on_change")
    section_id=fields.Many2one('eschool.class.section',related='classes_id.section_id',string='section')
    classes_id=fields.Many2one('eschool.classes',string='Class')
    got_student=fields.Boolean('Got Student?')
    @api.onchange('register_id','attendance_date')
    def get_course_section(self):
        self.ensure_one()
        self.course_id=self.register_id.course_id.id
        self.section_id=self.classes_id.section_id.id
        self.name=str(self.register_id.name)+ str(self.attendance_date)

    @api.multi
    def get_students(self):
        lineStudentList=[]
        sheetAttendanceLine = self.env['op.attendance.line'].search([('attendance_id.id', '=', self.id)])
        for rec in sheetAttendanceLine:
            lineStudentList.append(rec.student_id.id)
        student_in_course= self.env['op.student.course'].search([('course_id','=',self.course_id.id),('section_id','=',self.section_id.id)])
        for student in student_in_course:
            if student.student_id.id not in lineStudentList:
                self.env['op.attendance.line'].create({'attendance_id': self.id,'student_id':student.student_id.id,
                                                       'classes_id': self.classes_id.id,'section_id':self.section_id.id,'roll_no':student.roll_number,
                                                   'register_id':self.register_id,'batch_id': self.batch_id.id,'present': True})
        self.got_student=True


class opattendancelineinherit(models.Model):
    _inherit='op.attendance.line'
    classes_id=fields.Many2one('eschool.classes','Class')
    roll_no=fields.Integer('Roll No')
    group_id=fields.Many2one('eschool.course.division',"Group")
    section_id=fields.Many2one('eschool.class.section',"section")
    @api.onchange('classes_id')
    def get_course_section(self):
        for rec in self:
            rec.section_id=rec.classes_id.section_id.id
            rec.group_id=rec.classes_id.group_id.id
