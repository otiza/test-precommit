from odoo import models, fields

class Fichier(models.Model):
    _name = 'gestion.clinique.fichier'
    _description = 'Dossier Médical'

    patient_id = fields.Many2one('gestion.clinique.patient', string='Patient', required=True)
    rendezvous_ids = fields.One2many('gestion.clinique.rendezvous', 'fichier_id', string='Rendez-vous')
    fichier_id = fields.Many2one('autre.module', string='Fichier')  # Ou peut-être 'gestion.clinique.fichier' si vous voulez une relation Many2one à lui-même
