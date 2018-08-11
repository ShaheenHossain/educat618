from odoo import api, fields, models


class inheritAttendanceRegister(models.Model):
    _inherit='op.attendance.register'
    batch_id = fields.Many2one('op.batch', 'Batch',related='course_id.batch_id', store=True, required=False,readonly=True)



class inheritAttendanceLine(models.Model):
    _inherit = 'op.attendance.line'
    sms_sent=fields.Boolean('SMS Sent?')


class inheritAttendanceSheet(models.Model):
    _inherit='op.attendance.sheet'
    @api.multi
    def sms_action(self):
        self.ensure_one()
        for record in self:
            absentlist=[]
            absent = self.env['op.attendance.line'].search(
                [('present', '=', False), ('attendance_id', '=', record.id), ('sms_sent', '=', False)])
            for students in absent:
                StId = students.student_id.partner_id.id
                smsbody= "Dear Gurdian, Your pet, ${object.name} is absent to school Today."
                absentlist.append(StId)
                StId = students.student_id.partner_id.id
                # search last sms id
                # smsid=self.env['sms.mass'].search([])[-1].id

                #self.env['res_partner_sms_mass_rel'].create({'sms_mass_id':smsid,'res_partner_id': StId})
                print StId #(self.env['sms.mass'].search([])[-1].id)
                # print smsid  #(students.student_id.partner_id)

            self.env['sms.mass'].create({'from_mobile': 1, 'mass_sms_state': 'draft','sms_template_id':1, 'stop_message': "hizibizi",
                                         'selected_records': [[6, 0, absentlist]], 'message_text': smsbody})
