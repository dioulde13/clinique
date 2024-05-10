# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FacturationHeritage(models.Model):
    _inherit = 'account.move'

    motif = fields.Text(string='Motif')
    # company_id = fields.Many2one('res.company', readonly=True)
