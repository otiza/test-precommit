from odoo import models, fields

class Diagnostic(models.Model):
    _name = 'gestion.clinique.diagnostic'
    _description = 'Diagnostic'

    name = fields.Char(string='Diagnostic Name', required=True)  # Assurez-vous que ce champ est défini
    patient_id = fields.Many2one('gestion.clinique.patient', string='Patient', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    diagnosis = fields.Text(string='Diagnosis')
