# -*- coding: utf-8 -*-

from odoo import models, fields, api

class eschoolStudent(models.Model):
    _inherit = 'op.student'
    _rec_name='code'
    code=fields.Char("code")
    nationality = fields.Many2one('res.country', 'Nationality', default=20)
    religion=fields.Many2one('eschool.religion',string="Religion" , required=True)
    doa=fields.Date('Date Of Admission')
    coa=fields.Many2one('op.course',"class Of Admission")
    father=fields.Char("Father's Name",required=True)
    mother=fields.Char("Mother's Name",required=True)
    guardian=fields.Selection([('father', 'Father'),
                                ('mother', 'Mother'),
                                ('other', 'Other')
                                ],'Guardian',default='father')
    gname=fields.Char('Guardian')
    fcontact=fields.Char("Mobile")
    mcontact=fields.Char('Mobile')
    gcontact=fields.Char('Mobile')
    active = fields.Boolean("Active ?", default=True)
    vill = fields.Char('Village')
    po = fields.Char('Post Office')
    ps = fields.Char('Thana')
    dst = fields.Char('District')
    country = fields.Many2one('res.country', string='Country', ondelete='restrict',default=20)
    @api.onchange('guardian','father','mother')
    def change_gurdian_details(self):
        for rec in self:
            if rec.guardian=='father':
                rec.gname=rec.father
                rec.gcontact=rec.fcontact
            elif rec.guardian=='mother':
                rec.gname=rec.mother
                rec.gcontact=rec.mcontact
    @api.multi
    # @api.onchange('gr_no','name','middle_name','last_name','gr_no')
    def get_code(self):
        for r in self:
            display=""
            if r.name:
                display=r.name + '_'
            if r.middle_name:
                display=display+r.middle_name + "_"
            if r.last_name:
                    display=display+r.last_name
            if r.gr_no:
                display = str(r.gr_no) +'_'+ display
                r.email=str(r.gr_no)+"@dsblsc.com"
            r.code=display

    @api.multi
    def name_get(self):
        result = []
        for r in self:

            if r.name:
                display=r.name + '_'
            if r.middle_name:
                display=display+r.middle_name + "_"
            if r.last_name:
                    display=display+r.last_name
            if r.gr_no:
                display = str(r.gr_no) +'_'+ display
                r.code=display
            result.append((r.id, display))
        return result
    # @api.multi
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = str(record.gr_no) + ',' + record.name+ record.gr_no
    #         result.append((record.id, name))
    #     return result

class eschoolStudentCourse(models.Model):
    _inherit = 'op.student.course'
    section_id = fields.Many2one('eschool.class.section', 'Section', required=True)
    classes_id=fields.Many2one("eschool.classes","classes")

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(course_id,batch_id,student_id)',
         'Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,section_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]
