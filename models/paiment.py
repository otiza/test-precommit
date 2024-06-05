from odoo import models, fields

class Paiment(models.Model):
    _name = 'gestion.clinique.paiment'
    _description = 'Paiment Model'

    name = fields.Char(string='Paiment Reference', required=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Paiment Date', default=fields.Date.today())
    patient_id = fields.Many2one('gestion.clinique.patient', string='Patient')
    description = fields.Text(string='Description')
