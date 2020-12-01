from odoo import models, fields, api


class PosProductMinimum(models.Model):
    _inherit = 'product.template'
    contained_quantity = fields.Integer('Contained Quantity')