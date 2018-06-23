# -*- coding: utf-8 -*-

from odoo import models, fields, api

class eschoolStudent(models.Model):
    _inherit = 'op.student'
    nationality = fields.Many2one('res.country', 'Nationality', default=20)
class eschoolStudentCourse(models.Model):
    _inherit = 'op.student.course'
    course_id = fields.Many2one('op.course', 'Class', required=True)

