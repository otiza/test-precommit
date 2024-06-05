from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class Patient(models.Model):
    _name = 'gestion.clinique.patient'
    _description = 'Patient'

    name = fields.Char(string='Nom', unique=True)
    identity_number = fields.Char(string="Numéro d'identité")
    first_doctor_id = fields.Many2one('gestion.clinique.medecin', string='Premier médecin')
    image = fields.Binary(string='     ')
    age = fields.Integer(string='Âge', compute='_compute_age', store=True)
    gender = fields.Selection([('male', 'Homme'), ('female', 'Femme')], string='Genre')
    address = fields.Char(string='Adresse')
    date_naissance = fields.Date(string='Date de naissance')
    phone = fields.Char(string='Téléphone')
    email = fields.Char(string='Email')
    city = fields.Char(string='Ville')
    country = fields.Char(string='Pays')
    zip_code = fields.Char(string='Code postal')

    blood_type = fields.Selection([('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], string='Groupe sanguin')
    height = fields.Float(string='Taille (cm)')
    weight = fields.Float(string='Poids (kg)')
    allergies = fields.Selection([
        ('peanut', 'Arachides'),
        ('gluten', 'Gluten'),
        ('shellfish', 'Fruits de mer'),
        ('lactose', 'Lactose'),
        ('pollen', 'Pollen'),
        ('medication', 'Médicaments'),
        ('other', 'Autre'),
    ], string='Allergies')
    medical_history = fields.Text(string='Antécédents médicaux')
    Statut_matrimonial = fields.Selection([('single', 'Célibataire'), ('married', 'Marié(e)')], string='Statut matrimonial')
    Religion = fields.Selection([
        ('islam', 'Islam'),
        ('christianity', 'Christianisme'),
        ('hinduism', 'Hindouisme'),
        ('buddhism', 'Bouddhisme'),
        ('judaism', 'Judaïsme'),
        ('other', 'Autre'),
    ], string='Religion')
    metier = fields.Char(string='Métier')
    tribu = fields.Selection([
        ('masai', 'Masai'),
        ('navajo', 'Navajo'),
        ('inuit', 'Inuit'),
        ('maori', 'Maori'),
        ('cherokee', 'Cherokee'),
        ('autre', 'Autre'),
    ], string='Tribu')
    temperature = fields.Float(string='Température (°C)')
    respiratory_rate = fields.Integer(string='Fréquence Respiratoire')
    blood_pressure_systolic = fields.Integer(string='Tension Artérielle Systolique')
    blood_pressure_diastolic = fields.Integer(string='Tension Artérielle Diastolique')
    heart_rate = fields.Integer(string='Fréquence Cardiaque')
    medical_alert = fields.Selection([
        ('allergy', 'Allergie'),
        ('asthma', 'Asthme'),
        ('diabetes', 'Diabète'),
        ('hypertension', 'Hypertension'),
        ('anemia', 'Anémie'),
        ('migraine', 'Migraine'),
        ('other', 'Autre')
    ], string='Alerte médicale', default='allergy')
    previous_medical_history = fields.Text(string='DMA')
    disease = fields.Text(string='Maladie')
    concerned_doctor = fields.Text(string='Médecin Concerné')
    medical_treatment = fields.Text(string='Traitement Médical')
    mere_pere = fields.Text(string='Mère/Père')
    proche = fields.Text(string='Proches')
    Maladie_genetique = fields.Text(string='Maladie génétique')
    date = fields.Date(string='Date')
    description = fields.Text(string='Description')
    resultat = fields.Text(string='Résultat')
    hospital_doctor = fields.Many2one('gestion.clinique.medecin', string='Médecin Hospitalier')
    date_of_death = fields.Date(string='Date du décès')
    cause_of_death = fields.Text(string='Cause du décès')
    next_of_kin = fields.Char(string='Proche parent')

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
        return super(Patient, self).create(vals)
    def _check_phone(self):
        phone_regex = re.compile(r'^\+?1?\d{9,15}$')
        for record in self:
            if record.phone and not phone_regex.match(record.phone):
                raise ValidationError("Le numéro de téléphone doit être au format international (ex: +123456789).")

    @api.constrains('email')
    def _check_email(self):
        email_regex = re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$')
        for record in self:
            if record.email and not email_regex.match(record.email):
                raise ValidationError("L'adresse e-mail n'est pas valide.")

    @api.constrains('identity_number')
    def _check_identity_number(self):
        id_regex = re.compile(r'^[A-Za-z0-9]+$')
        for record in self:
            if record.identity_number and not id_regex.match(record.identity_number):
                raise ValidationError("Le numéro d'identité doit être alphanumérique.")

    @api.onchange('name')
    def _onchange_name(self):
        if self.name and not self.name.isalpha():
            self.name = False
            return {
                'warning': {
                    'title': "Erreur de validation",
                    'message': "Le nom ne doit contenir que des lettres."
                }
            }

    @api.constrains('address')
    def _check_address(self):
        if self.address and len(self.address) < 5:
            raise ValidationError("L'adresse doit contenir au moins 5 caractères.")

    @api.constrains('metier')
    def _check_metier(self):
        if self.metier and not self.metier.replace(" ", "").isalpha():
            raise ValidationError("Le métier ne doit contenir que des lettres et des espaces.")

    @api.constrains('city')
    def _check_city(self):
        if self.city and not self.city.replace(" ", "").isalpha():
            raise ValidationError("La ville ne doit contenir que des lettres et des espaces.")

    @api.onchange('address')
    def _onchange_address(self):
        if self.address and len(self.address) < 5:
            self.address = False
            return {
                'warning': {
                    'title': "Erreur de validation",
                    'message': "L'adresse doit contenir au moins 5 caractères."
                }
            }

    @api.onchange('metier')
    def _onchange_metier(self):
        if self.metier and not self.metier.replace(" ", "").isalpha():
            self.metier = False
            return {
                'warning': {
                    'title': "Erreur de validation",
                    'message': "Le métier ne doit contenir que des lettres et des espaces."
                }
            }

    @api.onchange('city')
    def _onchange_city(self):
        if self.city and not self.city.replace(" ", "").isalpha():
            self.city = False
            return {
                'warning': {
                    'title': "Erreur de validation",
                    'message': "La ville ne doit contenir que des lettres et des espaces."
                }
            }
    @api.onchange('zip_code')
    def _onchange_zip_code(self):
        zip_code_regex = re.compile(r'^\d{5}$')
        if self.zip_code and not zip_code_regex.match(self.zip_code):
            self.zip_code = False
            return {
                'warning': {
                    'title': "Erreur de validation",
                    'message': "Le code postal doit contenir exactement 5 chiffres."
                }
            }
    @api.constrains('country')
    def _check_country(self):
        for record in self:
            if record.country and not record.country.isalpha():
                raise ValidationError("Le pays doit être composé uniquement de lettres.")
    @api.constrains('height', 'weight', 'temperature', 'respiratory_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate')
    def _check_numeric_values(self):
        for record in self:
            if record.height < 0 or record.weight < 0 or record.temperature < 0 or record.respiratory_rate < 0 or record.blood_pressure_systolic < 0 or record.blood_pressure_diastolic < 0 or record.heart_rate < 0:
                raise ValidationError("Les champs numériques doivent contenir des nombres positifs.")
    @api.constrains('previous_medical_history', 'disease', 'medical_treatment', 'Maladie_genetique', 'description', 'resultat', 'cause_of_death')
    def _check_letters_only(self):
        for record in self:
            if any(field and not field.replace(" ", "").isalpha() for field in [
                record.previous_medical_history,
                record.disease,
                record.medical_treatment,
                record.Maladie_genetique,
                record.description,
                record.resultat,
                record.cause_of_death,
            ]):
                raise ValidationError("Les champs doivent contenir uniquement des lettres et des espaces.")