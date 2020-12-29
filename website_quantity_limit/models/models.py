from odoo import models, fields, api
class ProductMinimumQuantity(models.Model):
    _inherit = 'product.product'
    min_quantity_limit = fields.Integer('Minimum Quantity Limit')
    max_quantity_limit = fields.Integer('Maximum Quantity Limit')