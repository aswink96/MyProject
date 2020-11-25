from odoo import models, fields, api


class PosFixedDiscount(models.Model):
    _inherit = 'pos.config'
    _description = 'Pos Discount'
    pos_task_discount_config =fields.Boolean(string="Discount Type",default=True, store=True)
    discount_type = fields.Selection([('discount_percentage','Discount Percentage'),('discount_amount','Discount Amount')], string='Product Discount')
    discount_value = fields.Float(string='Discount Percentage')
    # discount_product_id = fields.Many2one('product.product', string='Service Product',
    #                                      domain="[('available_in_pos', '=', True),"
    #                                             "('sale_ok', '=', True)]")