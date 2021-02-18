from odoo import models, fields, api
from datetime import datetime


class Representative(models.Model):
    _name = 'representative.representative'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string="Name")
    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")