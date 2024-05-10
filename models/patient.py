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
    telephone = fields.Char(string='Téléphone')
    reference = fields.Char(string='Reference')
    email = fields.Char(string='Email')
    age = fields.Integer(string='Âge', compute='_compute_age', tracking=True)
    date_naissance = fields.Date(string='Date de naissance', tracking=True)
    profession = fields.Char(string='Profession')
    derniere_visite = fields.Datetime(string='Dernière Visite')


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


