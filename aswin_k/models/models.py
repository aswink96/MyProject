# -*- coding: utf-8 -*-
from odoo import models, fields, api


class VoxtronTask(models.Model):
    _inherit = 'sale.order'

    customer_type = fields.Selection([('new', 'New'),
                              ('existing', 'Existing')], required=True, default='new')
    customer_reference = fields.Char('Customer Reference')
    representative_id = fields.Many2one('representative.representative', string="Representative")