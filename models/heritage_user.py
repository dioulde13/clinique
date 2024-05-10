# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    name = fields.Char(string='Nom', tracking=True)
