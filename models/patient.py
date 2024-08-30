# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class CLiniquePatient(models.Model):
    _name = 'clinique.patient'
    _description = 'Patient Clinique'
    _inherit = ['mail.thread']

    name = fields.Char(string='Nom', tracking=True)
    genre = fields.Selection([('homme', 'Homme'), ('femme', 'Femme')], string='Genre', tracking=True)
    adresse = fields.Text(string='Adresse')
    partner_id = fields.Many2one('res.partner')
    telephone = fields.Char(string='Téléphone')
    reference = fields.Char(string='Reference')
    email = fields.Char(string='Email')
    age = fields.Integer(string='Âge', compute='_compute_age', tracking=True)
    date_naissance = fields.Date(string='Date de naissance', tracking=True)
    profession = fields.Char(string='Profession')
    derniere_visite = fields.Datetime(string='Dernière Visite')
    priority = fields.Selection(
        [
            ('0', 'Nouveau'),
            ('1', 'En cours'),
            ('2', 'En attente'),
            ('3', 'Resolu'),
            ('4', 'Annuler'),
        ], string="Priority")

    state = fields.Selection(
        [
            ('nouveau', 'Nouveau'),
            ('en_cours', 'En cours'),
            ('en_attente', 'En attente'),
            ('resolu', 'Resolu'),
            ('annuler', 'Annuler'),
        ], default='nouveau', string="Status")

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('clinique.patient')
        return super(CLiniquePatient, self).create(vals)

    @api.depends('date_naissance')
    def _compute_age(self):
        for patient in self:
            today = date.today()
            if patient.date_naissance:
                patient.age = today.year - patient.date_naissance.year
            else:
                patient.age = 1

    def action_en_cours(self):
        self.state = 'en_cours'

    def action_en_attente(self):
        self.state = 'en_attente'

    def action_resolu(self):
        self.state = 'resolu'

    def action_annuler(self):
        self.state = 'annuler'
