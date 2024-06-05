import re
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class Medecin(models.Model):
    _name = 'gestion.clinique.medecin'

    name = fields.Char(string='Name')
    date_naissance = fields.Date(string='Date de naissance')

    image = fields.Binary(string='     ')
    gender = fields.Selection([('male', 'Homme'), ('female', 'Femme')], string='Genre')
    identity_number = fields.Char(string="Numéro d'identité")
    speciality = fields.Selection([
        ('cardiologue', 'Cardiologue'),
        ('pédiatre', 'Pédiatre'),
        ('généraliste', 'Médecin généraliste'),
        ('dermatologue', 'Dermatologue'),
        ('gynécologue', 'Gynécologue'),
        ('ophtalmologue', 'Ophtalmologue'),
        ('dentiste', 'Dentiste'),
        ('psychiatre', 'Psychiatre'),
        ('urologue', 'Urologue'),
        ('chirurgien', 'Chirurgien'),
        ('radiologue', 'Radiologue'),
        ('neurologue', 'Neurologue'),
        ('oncologue', 'Oncologue'),
        ('endocrinologue', 'Endocrinologue'),
        ('orthopédiste', 'Orthopédiste'),
        ('rhumatologue', 'Rhumatologue'),
        ('allergologue', 'Allergologue'),
        ('gastro-entérologue', 'Gastro-entérologue'),
        ('néphrologue', 'Néphrologue'),
        ('pneumologue', 'Pneumologue'),
        ('anesthésiste', 'Anesthésiste'),
        ('ORL', 'Oto-rhino-laryngologiste'),
        ('chirurgien plastique', 'Chirurgien plastique'),
        ('vétérinaire', 'Vétérinaire'),
        ('autre', 'Autre'),
    ], string='Spécialité médicale')
    education = fields.Selection([
        ('médecin_généraliste', 'Médecin généraliste'),
        ('médecin_spécialiste', 'Médecin spécialiste'),
        ('internat', 'Internat'),
        ('résidanat', 'Résidanat'),
        ('pharmacie', 'Pharmacie'),
        ('biologie_médicale', 'Biologie médicale'),
        ('odontologie', 'Odontologie'),
        ('sage-femme', 'Sage-femme'),
        ('paramédical', 'Paramédical'),
        ('autre', 'Autre'),
    ], string='Formation/Éducation')
    date_of_birth = fields.Date(string='Date de naissance')
    age = fields.Integer(string='Âge', compute='_compute_age')
    address = fields.Char(string='Adresse')
    phone = fields.Char(string='Téléphone')
    email = fields.Char(string='Email')
    city = fields.Char(string='City')
    country = fields.Char(string='Country')
    zip_code = fields.Char(string='zip_code')
    Religion =fields.Selection([
    ('islam', 'Islam'),
    ('christianity', 'Christianisme'),
    ('hinduism', 'Hindouisme'),
    ('buddhism', 'Bouddhisme'),
    ('judaism', 'Judaïsme'),
    ('other', 'Autre'),
], string='Religion')
    Statut_matrimonial=fields.Selection([('single', 'Célibataire'),('married', 'Marié(e)'),
], string='Statut matrimonial')
    signature_field = fields.Binary(string='Signature', widget='signature', help='Utilisez ce champ pour capturer la signature.')
    
    operation_type = fields.Char(string="Type d'Opération")
    amount_to_pay = fields.Float(string="Montant à Payer")
    disponibilite_lundi = fields.Boolean(string='Lundi')
    disponibilite_mardi = fields.Boolean(string='Mardi')
    disponibilite_mercredi = fields.Boolean(string='Mercredi')
    disponibilite_jeudi = fields.Boolean(string='Jeudi')
    disponibilite_vendredi = fields.Boolean(string='Vendredi')
    disponibilite_samedi = fields.Boolean(string='Samedi')
    disponibilite_dimanche = fields.Boolean(string='Dimanche')
    @api.depends('date_naissance')
    def _compute_age(self):
        for record in self:
            if record.date_naissance:
                birth_date = fields.Date.from_string(record.date_naissance)
                today = fields.Date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age if age >= 0 else 0
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        if 'date_naissance' in vals:
            birth_date = fields.Date.from_string(vals['date_naissance'])
            today = fields.Date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 0 or age > 150:
                raise ValidationError("L'âge doit être un nombre positif et inférieur à 150.")
        return super(Medecin, self).create(vals)
    
    @api.constrains('name', 'identity_number', 'address', 'phone', 'email', 'city', 'country', 'zip_code', 'operation_type')
    def _check_text_fields(self):
        for record in self:
            if record.name and not re.match(r'^[a-zA-Z ]+$', record.name):
                raise ValidationError("Le nom ne doit contenir que des lettres et des espaces.")
            if record.identity_number and not re.match(r'^[a-zA-Z0-9]+$', record.identity_number):
                raise ValidationError("Le numéro d'identité ne doit contenir que des lettres et des chiffres.")
            if record.address and not re.match(r'^[a-zA-Z0-9 ]+$', record.address):
                raise ValidationError("L'adresse ne doit contenir que des lettres, des chiffres et des espaces.")
            if record.phone and not re.match(r'^[0-9]+$', record.phone):
                raise ValidationError("Le téléphone ne doit contenir que des chiffres.")
            if record.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', record.email):
                raise ValidationError("L'adresse email n'est pas valide.")
            if record.city and not re.match(r'^[a-zA-Z ]+$', record.city):
                raise ValidationError("La ville ne doit contenir que des lettres et des espaces.")
            if record.country and not re.match(r'^[a-zA-Z ]+$', record.country):
                raise ValidationError("Le pays ne doit contenir que des lettres et des espaces.")
            if record.zip_code and not re.match(r'^[0-9]+$', record.zip_code):
                raise ValidationError("Le code postal ne doit contenir que des chiffres.")
            if record.operation_type and not re.match(r'^[a-zA-Z ]+$', record.operation_type):
                raise ValidationError("Le type d'opération ne doit contenir que des lettres et des espaces.")

    @api.constrains('amount_to_pay')
    def _check_amount_to_pay(self):
        for record in self:
            if record.amount_to_pay < 0:
                raise ValidationError("Le montant à payer ne peut pas être négatif.")