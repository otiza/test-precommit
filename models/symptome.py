from odoo import models, fields

class Symptome(models.Model):
    _name = 'gestion.clinique.symptome'
    _description = 'Symptôme'

    name = fields.Char(string='Nom', required=True)
    maladie_ids = fields.Many2many('gestion.clinique.maladie', string='Maladies', relation='symptome_maladie_rel')
