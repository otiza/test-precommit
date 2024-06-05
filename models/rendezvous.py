import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class RendezVous(models.Model):
    _name = 'gestion.clinique.rendezvous'
    _description = 'Rendez-vous'
    
    def _default_name(self):
        return 'RDV.'

    name = fields.Char(string='Nom', unique=True, default=_default_name)
    fichier_id = fields.Many2one('gestion.clinique.fichier', string='Fichier')
    description = fields.Char(string='Description')
    patient_id = fields.Many2one('gestion.clinique.patient', string='Patient')
    etat = fields.Selection([('planifie', 'Planifié'), ('en_cours', 'En cours'), ('termine', 'Terminé'), ('annule', 'Annulé')], string='État', default='planifie')
    medcin_id = fields.Many2one('gestion.clinique.medecin', string='Médecin')
    date_rendezvous = fields.Date(string='Date de rendez-vous', default=fields.Date.today)
    cas_urgence = fields.Selection([('normale', 'Normale'), ('urgence', 'Urgence')], string='Cas d\'urgence', default='normale')
    start_datetime= fields.Datetime(string='Start Date', required=True)
    end_datetime = fields.Datetime(string='Stop Date', required=True)

    @api.constrains('date_rendezvous')
    def _check_date_rendezvous(self):
        for record in self:
            if record.date_rendezvous < fields.Date.today():
                raise ValidationError('Cannot create appointment in the past.')
    @api.constrains('name')
    def _check_nom_patient(self):
        for record in self:
            if record.name and not re.match(r'^[a-zA-Z .]+$', record.name):
                raise ValidationError("Le nom du patient ne doit contenir que des lettres, des espaces et des points.")

    @api.constrains('description')
    def _check_description(self):
        for record in self:
            if record.description and not re.match(r'^[a-zA-Z ]+$', record.description):
                raise ValidationError("La description ne doit contenir que des lettres et des espaces.")
    @api.constrains('start_datetime', 'end_datetime', 'medcin_id')
    def _check_doctor_availability(self):
        for rec in self:
            if rec.start_datetime and rec.end_datetime and rec.medcin_id:
                # Check doctor availability using the Horaire model or your availability logic
                availability = self.env['gestion.clinique.horaire'].browse(rec.medcin_id.id).date_dispo(rec.start_datetime, rec.end_datetime)
                if not availability:
                    raise ValidationError("Selected doctor is not available at this time.")

    @api.model
    def create(self, vals):
        if 'medcin_id' in vals and 'start_datetime' in vals and 'end_datetime' in vals:
            medcin_id = vals['medcin_id']
            start_datetime = vals['start_datetime']
            end_datetime = vals['end_datetime']
            horaire_obj = self.env['gestion.clinique.horaire']
            horaire_record = horaire_obj.search([('medcin_id', '=', medcin_id)])
            if horaire_record and horaire_record.date_dispo(start_datetime, end_datetime):
                return super(RendezVous, self).create(vals)
            else:
                raise ValidationError("Selected doctor is not available at this time.")
        return super(RendezVous, self).create(vals)
