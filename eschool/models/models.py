# -*- coding: utf-8 -*-

from odoo import models, fields, api

class eschool_res_company(models.Model):
    _inherit='res.company'
    email_suffix = fields.Char('Default Email Suffix for New Contacts',default='dsblsc.com')

class eschoolCourseDivision(models.Model):
    _name='eschool.course.division'
    _order = 'name asc'
    name=fields.Char('Division')
    description=fields.Char('Description')
    code=fields.Char('Code')
    level_ids=fields.Many2many('eschool.level',string='Level')


class eschoolClassSection(models.Model):
    _name='eschool.class.section'
    _order = 'sequence asc'
    sequence=fields.Integer('SL')
    _description='this is for the sections like A,B,C....'
    name=fields.Char('Section',required=True)
    description=fields.Char('Description')
    code=fields.Char('Code',required=True)
    course_ids=fields.Many2many('op.course',string='Courses')
class eschoolReligion(models.Model):
    _name="eschool.religion"
    name=fields.Char('Religion')
    code=fields.Char('Code')
    description=fields.Char('Description')

class opbatchInherit(models.Model):
    _inherit = 'op.batch'
    current=fields.Boolean("Current", help="Set Batch Active")
    code = fields.Char('Code', required=True)
    course_id = fields.One2many('op.course','batch_id', string="Course")
    active=fields.Boolean('Active?',default=True)


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


class eschoolLevels(models.Model):
    ''' Defining Standard Information '''
    _name = 'eschool.level'
    _description = 'Level Information'
    _order = "sequence"

    sequence = fields.Integer('Sequence', required=True)
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    group_ids=fields.Many2many('eschool.course.division',string="Groups")
    # section_ids=fields.Many2many('eschool.class.section',string="Sections")


class opClassRoomInherit(models.Model):
    _inherit = 'op.classroom'
    section_id=fields.Many2one('eschool.class.section',"section")
