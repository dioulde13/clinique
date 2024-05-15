# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FacturationHeritage(models.Model):
    _inherit = 'account.move'

    motif = fields.Text(string='Motif')
