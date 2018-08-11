# -*- coding: utf-8 -*-

from datetime import datetime
import time

from odoo import models, api



class ReportTabulationReport(models.AbstractModel):
    _name = 'report.eschool.tabulation_report'

    def get_objects(self, objects,data=None):
        obj = []
        object=self.env['op.exam.session']
        obj.extend(object)
        return obj
    def get_subjects(self, objects):
        sbj = []
        for object in objects.exam_ids:
            sbj.extend(object.subject_id)
        return sbj
    def get_exams(self, objects):
        exm = []
        for object in objects.exam_ids:
            exm.extend(object)
        return exm
    def get_students(self, objects):
        student = []
        for object in objects.exam_ids:
            for attendees in object.attendees_line:
                if attendees.student_id not in student :
                    student.extend(object.student_id)
        return student


    def get_lines(self, objects):
        lines = []
        for examid in objects.exam_ids:
            for line in examid.attendees_line :
                lines.extend(line)
        return lines

    def get_date(self, date):
        date1 = datetime.strptime(date, "%Y-%m-%d")
        return str(date1.month) + ' / ' + str(date1.year)

    def get_total(self, marksheet_line):
        total = [x.exam_id.total_marks for x in marksheet_line.result_line]
        return sum(total)

    @api.model
    def render_html(self, docids, data=None):
        docs = self.env['op.exam.session'].browse(docids)
        data = {}
        docargs = {
            'doc_model': 'op.exam.session',
            'docs': docs,
            'time': time,
            'get_objects': self.get_objects,
            'get_subjects': self.get_subjects,
            'get_students': self.get_students,
            'get_exams': self.get_exams,
            'get_lines': self.get_lines,
            'get_date': self.get_date,
            'get_total': self.get_total,
        }
        return self.env['report'] \
            .render('eschool.tabulation_report', docargs)
