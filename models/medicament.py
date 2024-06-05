from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError
import re

class Medicament(models.Model):
    _name = 'gestion.clinique.medicament'
    _description = 'Gestion des Médicaments'

    name = fields.Char(string='Nom du Médicament', required=True)
    description = fields.Char(string='Description')
    stock = fields.Float(string='Stock', default=0.0)
    prix_unitaire = fields.Float(string='Prix Unitaire', required=True)
    posologie = fields.Char(string='Dosage')
    ordonnance_ids = fields.Many2many('gestion.clinique.ordonnance', string='Ordonnances')
    image = fields.Binary(string='Image')
    categorie = fields.Selection([
        ('antibiotique', 'Antibiotique'),
        ('analgesique', 'Analgésique'),
        ('antipyretique', 'Antipyrétique'),
        ('anti-inflammatoire', 'Anti-inflammatoire')
    ], string='Catégorie')

    stock_status = fields.Selection([
        ('low', 'Bas'),
        ('medium', 'Moyen'),
        ('high', 'Élevé')
    ], string='Statut du Stock', compute='_compute_stock_status', store=True)

    stock_warning = fields.Boolean(string='Avertissement de Stock Bas', compute='_compute_stock_warning', store=True)
    stock_warning_message = fields.Char(string='Message d\'Avertissement de Stock Bas', compute='_compute_stock_warning_message', store=True)
    stock_reminder_date = fields.Date(string='Date du Rappel de Stock')

    @api.depends('stock')
    def _compute_stock_warning(self):
        for med in self:
            med.stock_warning = med.stock < 50

    @api.depends('stock')
    def _compute_stock_status(self):
        for med in self:
            if med.stock < 50:
                med.stock_status = 'low'
            elif 50 <= med.stock <= 90:
                med.stock_status = 'medium'
            else:
                med.stock_status = 'high'

    @api.constrains('name', 'description', 'posologie')
    def _check_text_fields(self):
        for med in self:
            if med.name and not re.match(r'^[a-zA-Z0-9 ]+$', med.name):
                raise ValidationError("Le nom du médicament ne doit contenir que des lettres, des chiffres et des espaces.")
            if med.description and not re.match(r'^[a-zA-Z0-9 ]+$', med.description):
                raise ValidationError("La description ne doit contenir que des lettres, des chiffres et des espaces.")
            if med.posologie and not re.match(r'^[a-zA-Z0-9 ]+$', med.posologie):
                raise ValidationError("La posologie ne doit contenir que des lettres, des chiffres et des espaces.")

    @api.constrains('prix_unitaire')
    def _check_prix_unitaire(self):
        for med in self:
            if med.prix_unitaire < 0:
                raise ValidationError("Le prix unitaire ne peut pas être négatif.")

    def send_low_stock_notification(self):
        for med in self.search([('stock', '<', 50)]):
            message = f'Le stock du médicament {med.name} est bas ({med.stock} unités). Veuillez réapprovisionner.'
            med.message_post(body=message, subject='Avertissement de Stock Bas', message_type='notification')

    def save_with_low_stock(self):
        for med in self:
            if med.stock < 50:
                med.stock_warning = False
                med.stock_reminder_date = False
