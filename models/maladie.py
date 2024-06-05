from odoo import models, fields

class Maladie(models.Model):
    _name = 'gestion.clinique.maladie'
    _description = 'Maladie'

    name = fields.Char(string='Nom', required=True)
    symptomes_ids = fields.Many2many('gestion.clinique.symptome', string='Symptômes', relation='maladie_symptome_rel')
