# -*- coding: utf-8 -*-

from odoo import models, fields, api


class eschoolOpCourseInherit(models.Model):
    _inherit = 'op.course'
    _rec_name = 'code'
    order='level'
    section = fields.Char('Section', size=32,required=False)
    section_ids=fields.Many2many("eschool.class.section",string="Sections")
    level=fields.Many2one('eschool.level',string='level',required=True)
    name=fields.Char('Name',compute='getcourse_code',required=True)
    has_group=fields.Boolean('Group Division ?',default=False)
    group = fields.Many2one('eschool.course.division', default=1,required=True)
    # standard_id = fields.Many2one('eschool.standard','Class', required=True)
    batch_id=fields.Many2one('op.batch',string="Batch",required=True)
    code = fields.Char('Code' ,compute='getcourse_code', required=True )
    parent_id = fields.Many2one('op.course',"Parent Course",invisible=True)
    course_student_ids=fields.One2many('op.student.course','course_id',string="Students")
    active=fields.Boolean("Active ?" ,related='batch_id.active')
    classes_ids=fields.One2many('eschool.classes',"course_id",'Classes')

    _sql_constraints = [
        ('unique_courseees_code',
         'unique(level,group,batch_id)',
         'Course must be unique by Class,Group and Batch!')]
    @api.multi
    def create_classes(self):
        #create a list of existing classes to check existance for new class to create
        for course in self:
            existingclass = self.env['eschool.classes'].search([('course_id','=',course.id)])
            existingclasslist=[]
            for classexist in existingclass:
                existingclasslist.append(classexist.section_id.id)
            for section in course.section_ids:
                if section.id not in existingclasslist:
                    sectionName=course.name + '-'+section.code
                    existingclass.create({'course_id': course.id,
                                        'section_id': section.id,
                                          'section_name': sectionName})

        return True

    #Here i want to create classes for alll the course batches and sections
    #
    #
    @api.onchange('level','group')
    def getcourse_code(self):
        for record in self:
            if record.level :
                if record.group:
                        if record.group.id==1:
                            if record.batch_id:
                                record.code= record.level.code + record.batch_id.code
                                record.name= record.level.name + record.batch_id.name

                        elif  record.group.id!=1:
                            if record.batch_id:
                                record.code= record.level.code+"-"+ record.group.code +"-"+ record.batch_id.code
                                record.name= record.level.name+"-"+ record.group.name +"-"+ record.batch_id.name
            # for ids in self.env['op.student.course'].search([('batch_id', '=', self.id )]):
            #     print (ids.id)
class eschoolClasses(models.Model):
    _name='eschool.classes'
    name=fields.Char('Class' ,compute='get_class_name',required=True)
    code=fields.Char('Code',compute='get_class_name' ,required=True)
    course_id=fields.Many2one('op.course','Course',required=True)
    batch_id=fields.Many2one('op.batch',string='Batch',related="course_id.batch_id")
    section_id=fields.Many2one('eschool.class.section',required=True)
    group_id=fields.Many2one('eschool.course.division','group',required=True)
    section_name=fields.Char('Section Name',required=True)
    class_room=fields.Many2one('op.classroom',"Class Room")
    student_id=fields.Many2many('op.student',string='Student')
    active = fields.Boolean("Active ?", default=True)
    _sql_constraints = [
        ('unique_Classes_code',
         'unique(code)',
         'classes must be unique')
    ]
    @api.model
    @api.onchange('course_id','section_id')
    def get_class_name(self):
        for rec in self:
            if rec.course_id.id  and rec.section_id.id  and rec.section_name:
                rec.name=rec.course_id.name +" "+ rec.section_id.name
                rec.code=rec.course_id.code  +" "+ rec.section_id.code

    class eschoolCreateClasses(models.Model):
        _name = 'eschool.create.classes'
        batch_id = fields.Many2one('op.batch', 'Batch')
        section_ids = fields.Many2one('eschool.class.section', 'Section')
        course_ids = fields.Many2one('op.course', string="courses")

        @api.multi
        def create_classes(self):
            classes = self.env['eschool.classes']
            for courses in self.course_ids:
                classes.create({
                    'course_id': courses.id,
                    'batch_id': self.batch_id.id,
                    'section_id': self.section_id.id,
                    'section_name': self.section_id.name,
                })

