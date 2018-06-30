##############################################################################
#    Copyright (C) 2017 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

import logging
import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


# Pharmacy Management

class OeHealthPharmacy(models.Model):
    _name = 'oeh.medical.health.center.pharmacy'
    _description = "Information about the pharmacy"
    _inherits={
        'res.partner': 'partner_id',
    }

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade', help='Partner-related data of the hospitals')
    pharmacist_name = fields.Many2one('oeh.medical.physician', string='Pharmacist Name', domain=[('is_pharmacist','=',True)], required=True)
    institution = fields.Many2one('oeh.medical.health.center', string='Health Center')
    pharmacy_lines = fields.One2many('oeh.medical.health.center.pharmacy.line', 'pharmacy_id', string='Pharmacy Lines')
    info = fields.Text(string='Extra Information')

    @api.model
    def create(self, vals):
        vals["is_pharmacy"] = True
        vals["is_company"] = True
        pharmacy = super(OeHealthPharmacy, self).create(vals)
        return pharmacy

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

class OeHealthPharmacyLines(models.Model):
    _name = 'oeh.medical.health.center.pharmacy.line'
    _description = 'Pharmacy Lines'

    STATES = [
        ('Draft', 'Draft'),
        ('Invoiced', 'Invoiced'),
    ]

    @api.depends('prescription_lines.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the Prescription lines.
        """
        for order in self:
            val = 0.0
            for line in order.prescription_lines:
                val += line.price_subtotal
            order.update({
                'amount_total': val,
            })

    name = fields.Many2one('oeh.medical.prescription', string='Prescription #', required=True, ondelete='cascade', readonly=True, states={'Draft': [('readonly', False)]})
    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=True, readonly=True, states={'Draft': [('readonly', False)]})
    doctor = fields.Many2one('oeh.medical.physician', string='Physician', help="Current primary care / family doctor", domain=[('is_pharmacist','=',False)], readonly=True, states={'Draft': [('readonly', False)]})
    prescription_lines = fields.One2many('oeh.medical.health.center.pharmacy.prescription.line', 'prescription_id', string='Prescription Lines', readonly=True, states={'Draft': [('readonly', False)]})
    pharmacy_id = fields.Many2one('oeh.medical.health.center.pharmacy', string='Pharmacy Reference', readonly=True, states={'Draft': [('readonly', False)]})
    amount_total = fields.Monetary(compute=_amount_all, string='Total', store=True, multi='sums', help="The total amount.")
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', help="Pricelist for current prescription", readonly=True, states={'Draft': [('readonly', False)]})
    currency_id = fields.Many2one(related='pricelist_id.currency_id', string="Currency", readonly=True)
    info = fields.Text(string='Extra Information', readonly=True, states={'Draft': [('readonly', False)]})
    state = fields.Selection(STATES, string='State', readonly=True, default=lambda *a: 'Draft')

    # Fetching prescription lines values
    def onchange_prescription_id(self,prescription_id=False):
        phar_pres_line_obj = self.env['oeh.medical.health.center.pharmacy.prescription.line']
        pres_obj = self.env['oeh.medical.prescription']
        prescription_ids =[]

        #defaults
        res = {'value':{
                      'prescription_lines':[],
                      'doctor':'',
                      'patient':'',
                }
            }

        if (not prescription_id):
            return res

        # Getting prescription values
        pr = pres_obj.browse(prescription_id)
        res['value'].update({
            'patient': pr.patient.id,
            'doctor':pr.doctor.id,
        })

        # Getting prescription lines values
        query = _("select name, indication, qty from oeh_medical_prescription_line where prescription_id = %s")%(str(prescription_id))
        self.env.cr.execute(query)
        vals = self.env.cr.fetchall()
        if vals:
            for va in vals:
                # Getting item pricing
                med_price = 0.0

                query1 = _("select pt.list_price from oeh_medical_medicines om, product_product po, product_template pt where po.product_tmpl_id=pt.id and om.product_id=po.id and om.id = %s")%(str(va[0]))
                self.env.cr.execute(query1)
                vals1 = self.env.cr.fetchone()
                if vals1:
                    med_price = vals1[0]
                pres = {
                          'name': va[0],
                          'indication': va[1],
                          'qty': va[2],
                          'actual_qty': va[2],
                          'price_unit': med_price,
                          'price_subtotal': float(va[2]) * float(med_price),
                        }
                prescription_ids += [pres]

            res['value'].update({
                'prescription_lines': prescription_ids,
            })
        return res

    # Create Prescription invoice

    @api.multi
    def _default_account(self):
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        return journal.default_credit_account_id.id

    def action_prescription_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        inv_ids = []

        for pres in self:
            # Create Invoice
            if pres.patient:
                curr_invoice = {
                    'partner_id': pres.patient.partner_id.id,
                    'account_id': pres.patient.partner_id.property_account_receivable_id.id,
                    'patient': pres.patient.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice': datetime.datetime.now(),
                    'origin': pres.name.name,
                }

                inv_ids = invoice_obj.create(curr_invoice)

                if inv_ids:
                    prd_account_id = self._default_account()
                    inv_id = inv_ids.id
                    if pres.prescription_lines:
                        for ps in pres.prescription_lines:

                            # Create Invoice line
                            curr_invoice_line = {
                                'name': ps.name.product_id.name,
                                'product_id': ps.name.product_id.id,
                                'price_unit': ps.price_unit,
                                'quantity': ps.actual_qty,
                                'account_id':prd_account_id,
                                'invoice_id':inv_id,
                            }

                            inv_line_ids = invoice_line_obj.create(curr_invoice_line)

                res = self.write({'state': 'Invoiced'})
        return res

    # Preventing deletion of a prescription which is not in draft state
    @api.multi
    def unlink(self):
        for priscription in self.filtered(lambda priscription: priscription.state not in ['Draft']):
            raise UserError(_('You can not delete a prescription which is in "Invoiced" state !!'))
        return super(OeHealthPharmacyLines, self).unlink()

class OeHealthPharmacyMedicineLines(models.Model):
    _name = 'oeh.medical.health.center.pharmacy.prescription.line'
    _description = 'Pharmacy Medicine Lines'

    @api.multi
    def _amount_line(self):
        """
        Compute the total amounts of the Prescription lines.
        """
        for line in self:
            price = line.price_unit * line.actual_qty
            line.price_subtotal = price
        return True

    name = fields.Many2one('oeh.medical.medicines', string='Medicines', help="Prescribed Medicines", domain=[('medicament_type','=','Medicine')], required=True)
    indication = fields.Many2one('oeh.medical.pathology', string='Indication', help="Choose a disease for this medicament from the disease list. It can be an existing disease of the patient or a prophylactic.")
    qty = fields.Integer(string='Prescribed Qty', help="Quantity of units (eg, 2 capsules) of the medicament")
    actual_qty = fields.Integer(string='Actual Qty Given', help="Actual quantity given to the patient")
    prescription_id = fields.Many2one('oeh.medical.health.center.pharmacy.line', string='Pharmacy Prescription Reference')
    price_unit = fields.Float(string='Unit Price', required=True, default=lambda *a: 0.0)
    price_subtotal = fields.Float(compute=_amount_line, string='Subtotal', default=lambda *a: 0.0)

    # Autopopulate selected medicine values
    @api.multi
    def onchange_medicine_id(self,medicine=False):
        result = {}
        if medicine:
            med_obj = self.env['oeh.medical.medicines']
            med_price_ids1 = med_obj.search([('id', '=', medicine)])
            if med_price_ids1:
                result['price_unit'] = med_price_ids1.lst_price
        return {'value': result}

    # Change subtotal pricing
    @api.multi
    def onchange_qty_and_price(self,qty=False,price_unit=False):
        result = {}
        if qty and price_unit:
            result['price_subtotal'] = price_unit * qty
        return {'value': result}
