from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
class Opération(models.Model):
    _name = 'gestion.clinique.operation'
    _description = 'Opération'
    
    patient_id = fields.Many2one('gestion.clinique.patient', string='Patient')
    medecin_id = fields.Many2one('gestion.clinique.medecin', string='Médecin')
    state = fields.Selection([
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], string='État', default='in_progress')
    operation_type = fields.Char(string="Type d'Opération")
    medication_type = fields.Char(string="Médicament Préop")
    days_stay_after_operation = fields.Integer(string="Jours Séjour Postop")
    analysis_type_before_operation = fields.Char(string="Analyse Préop")
    operation_rooms_count = fields.Integer(string="Chambres d'Opération")
    operation_date = fields.Date(string="Date de l'Opération")
    anesthesiologist_id= fields.Many2one('gestion.clinique.medecin', string="Médecin Anesthésiste")


    @api.model
    def get_operations_in_progress(self):
        operations = self.search([('state', '=', 'in_progress')])
        return operations
    
    @api.model
    def get_operations_cancelled(self):
        operations = self.search([('state', '=', 'cancelled')])
        return operations
    @api.model
    def get_operations_history(self):
        operations = self.search([('state', '=', 'done')])
        return operations
    @api.constrains('operation_type', 'medication_type', 'analysis_type_before_operation')
    def _check_fields(self):
        for record in self:
            if record.operation_type and not re.match(r'^[a-zA-Z ]+$', record.operation_type):
                raise ValidationError("Le type d'opération ne doit contenir que des lettres et des espaces.")
            if record.medication_type and not re.match(r'^[a-zA-Z ]+$', record.medication_type):
                raise ValidationError("Le type de médicament ne doit contenir que des lettres et des espaces.")
            if record.analysis_type_before_operation and not re.match(r'^[a-zA-Z ]+$', record.analysis_type_before_operation):
                raise ValidationError("Le type d'analyse ne doit contenir que des lettres et des espaces.")
