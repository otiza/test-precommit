from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class Horaire(models.Model):
    _name = 'gestion.clinique.horaire'
    _description = 'Dispositions'

    name = fields.Char(string='Nom', unique=True , compute='_compute_name', store=True)
    medcin_id = fields.Many2one('gestion.clinique.medecin', string='Médecin')
    date_dispo = fields.Date(string='Date de dispo', default=fields.Date.today)
    end_datetime = fields.Datetime(string='Stop Date', required=True)


    @api.constrains('date_dispo')
    def _check_date_dispo(self):
        for record in self:
            if record.date_dispo < fields.Date.today():
                raise ValidationError('Cannot create appointment in the past.')
    @api.depends('medcin_id')
    def _compute_name(self):
        for record in self:
            record.name = record.medcin_id.name if record.medcin_id else ''
