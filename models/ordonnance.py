from odoo import models, fields, api
import base64

class Ordonnance(models.Model):
    _name = 'gestion.clinique.ordonnance'
    _description = 'Ordonnance'
    
    prescription_number = fields.Char(string='Prescription Number')
    rendezvous_id = fields.Many2one('gestion.clinique.rendezvous', string='Rendez-vous')
    patient_id = fields.Many2one('gestion.clinique.patient', string='Patient')
    age = fields.Integer(string='Age',related='patient_id.age',store=True, readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender',related='patient_id.gender',store=True, readonly=True)
    file_number = fields.Char(string='File Number',related='patient_id.phone',store=True, readonly=True)
    medicament_ids = fields.Many2many('gestion.clinique.medicament', string='Medications')
    allergies = fields.Text(string='Allergies')
    special_instructions = fields.Text(string='Special Instructions')
    doctor_id = fields.Many2one('gestion.clinique.medecin', string='Doctor')
    prescription_date = fields.Date(string='Prescription Date', default=fields.Date.context_today)
    doctor_specialty = fields.Char(string='Doctor Specialty')
    signature = fields.Binary(string='Signature',related='doctor_id.signature_field',store=True, readonly=True)
    total_price = fields.Float(string='Total des Prix', compute='_compute_total_price', store=True)
    tax_amount = fields.Float(string='Tax (15%)', compute='_compute_tax_amount', store=True)
    total_to_pay = fields.Float(string='Total à Payer', compute='_compute_total_to_pay', store=True)
    

    

   
    @api.depends('medicament_ids')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(med.prix_unitaire for med in record.medicament_ids)

    @api.depends('total_price')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = record.total_price * 0.15

    @api.depends('total_price', 'tax_amount')
    def _compute_total_to_pay(self):
        for record in self:
            record.total_to_pay = record.total_price + record.tax_amount