# -*- coding: utf-8 -*-

from odoo import models, fields, api


class departement(models.Model):
    _name = 'clinique.departement'
    _description = 'Departement Clinique'

    name = fields.Char()

