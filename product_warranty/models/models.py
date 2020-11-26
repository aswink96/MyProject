# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from openerp.exceptions import ValidationError


# Adding new fields to the product form
class warranty_period_inherit(models.Model):
    _inherit = 'product.template'
    warranty_type = fields.Selection([('replace', 'Replacement'), ('service', 'Service')], string='Warranty Type',
                                     deafult='replace')
    warranty_period = fields.Integer(string='Warranty Period')
    property_stock_warranty = fields.Many2one("stock.location", string='Warranty Location',
                                                domain=[('location_id', '=', 8)])

    def _get_value(self):
        return 41


    has_warranty = fields.Boolean(string='Has Warranty?')
# smart button
class search(models.Model):
    _inherit = 'account.move'
    warranty_count = fields.Integer(compute='compute_count')
    warranty_details = fields.One2many('product_warranty.product_warranty',
                                       'invoice', string='Warranty Info')

    def compute_count(self):
        for record in self:
            record.warranty_count = self.env['product_warranty.product_warranty'].search_count(
                [('invoice', '=', self.id)])

    def get_warranty(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Warranty Requests',
            'view_mode': 'tree',
            'res_model': 'product_warranty.product_warranty',
            'domain': [('invoice', '=', self.id)],
            'context': "{'create': False}"
        }


# model for product warranty module
class product_warranty(models.Model):
    _name = 'product_warranty.product_warranty'
    _rec_name = 'warranty_number'

    def get_stockmove(self):
        # """function for getting stock moves into warranty form"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Moves',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.invoice.invoice_origin)],
            'context': "{'create': False}"
        }

    def button_reset(self):
        for rec in self:
            rec.state = 'draft'

    def button_to_approve(self):
        for rec in self:
            rec.write({'state': 'to approve'})

    def button_approved(self):
        for rec in self:
            rec.write({'state': 'product received'})

        product_location = self.env['stock.quant'].search([('product_id', '=', self.product.id),
                                                       ('location_id', '!=', [14, 41, 5])])

    # stock move when warranty type is replacement warranty
        if self.product.warranty_type == 'replacement_warranty':
           self.env['stock.picking'].create({
               'location_id':self.env.ref('stock.stock_location_customers').id,
               'location_dest_id': 41,
               'picking_type_id': self.env.ref('stock.picking_type_in').id,
               'partner_id': self.partner.id,
               'origin':self.warranty_number,
               'move_ids_without_package': [(0, 0, {
                'name': 'name',
                'location_id': self.env.ref('stock.stock_location_customers').id,
                'location_dest_id':41,
                'picking_type_id': self.env.ref('stock.picking_type_in').id,
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'product_uom_qty': 1,
                'quantity_done': 1
            })],

        })

           move = self.env['stock.move'].create({
            'name': self.warranty_number,
            'location_id': self.env.ref('stock.stock_location_customers').id,
            'location_dest_id':41,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 1,
            'reference': self.warranty_number
        })
           move._action_confirm()
           move._action_confirm()
           move.move_line_ids.write(
            {'qty_done': 1}
        )
           move._action_done()
        else:
        # stock move when warranty type is service warranty
            self.env['stock.picking'].create({
            'location_id': self.env.ref('stock.stock_location_customers').id,
            'location_dest_id': 41,
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'partner_id': self.partner.id,
            'move_ids_without_package': [(0, 0, {
                'name': 'name',
                'location_id': self.env.ref('stock.stock_location_customers').id,
                'location_dest_id': 41,
                'picking_type_id': self.env.ref('stock.picking_type_in').id,
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'product_uom_qty': 1,
                'quantity_done': 1
            })],
        })

            self.env['stock.move'].create({
            'name': self.warranty_number,
            'location_id': self.env.ref('stock.stock_location_customers').id,
            'location_dest_id': 41,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 1,
            'reference': self.warranty_number
        })


    def button_returnproduct(self):
    # """function for return product button"""
        for rec in self:
         rec.write({'state': 'done'})
         product_location = self.env['stock.quant'].search([('product_id', '=', self.product.id),
                                                            ('location_id', '!=', [14, 41, 5])])
         if self.product.warranty_type =='replacement_warranty':
              self.env['stock.picking'].create({
                  'location_id': product_location.location_id.id,
                  'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                  'picking_type_id': self.env.ref('stock.picking_type_out').id,
                  'partner_id': self.partner.id,
                  'origin': self.warranty_number,
                  'move_ids_without_package': [(0, 0, {
                      'name': 'name',
                      'location_id': product_location.location_id.id,
                      'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                      'picking_type_id': self.env.ref('stock.picking_type_out').id,
                      'product_id': self.product.id,
                      'product_uom': self.product.uom_id.id,
                      'product_uom_qty': 1,
                      'quantity_done': 1
                  })],
              })

              move = self.env['stock.move'].create({
                   'name': self.warranty_number,
                   'location_id': product_location.location_id.id,
                   'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                   'product_id': self.product.id,
                   'product_uom': self.product.uom_id.id,
                   'product_uom_qty': 1,
                   'reference': self.warranty_number
              })

              move._action_confirm()
              move._action_confirm()
              move.move_line_ids.write(
                  {'qty_done': 1}
              )
              move._action_done()
         else:
             self.env['stock.picking'].create({
                   'location_id': 41,
                   'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                   'picking_type_id': self.env.ref('stock.picking_type_out').id,
                   'partner_id': self.partner.id,
                   'state': 'done',
                   'origin': self.warranty_number,
                   'move_ids_without_package': [(0, 0, {
                   'name': 'name',
                   'location_id': 41,
                   'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                   'picking_type_id': self.env.ref('stock.picking_type_out').id,
                   'product_id': self.product.id,
                   'product_uom': self.product.uom_id.id,
                   'product_uom_qty': 1,

                   'quantity_done': 1
                   })],
             })

             self.env['stock.move'].create({
                   'name': self.warranty_number,
                   'location_id': 41,
                   'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                   'product_id': self.product.id,
                   'product_uom': self.product.uom_id.id,
                   'product_uom_qty': 1,

                   'reference': self.warranty_number
             })

    def button_cancel(self):
        for rec in self:
         rec.write({'state': 'cancelled'})

    warranty_number = fields.Char(string="Warranty Number", readonly=True, required=True, copy=False, default='New',unique=True)
    product = fields.Many2one("product.product", string='Product')
    invoice = fields.Many2one("account.move", string='Invoice',
                              domain=[('invoice_payment_ref', '!=', False),
                                      ('invoice_payment_state', '=', "paid")])
    partner = fields.Many2one("res.partner", string='Partner', related='invoice.partner_id', store=True)
    partner_street = fields.Char('Street', related='partner.street')
    partner_city = fields.Char('City', related='partner.city')
    invoice_date = fields.Date('Invoice date', related='invoice.invoice_date')
    serial_number = fields.Many2one("stock.production.lot", string='Serial number')
    current_date = fields.Date('Current date', default=datetime.today())
    expiry_date = fields.Date('Expiry date')
    state = fields.Selection([('draft', 'Draft'),
                              ('to approve', 'To Approve'),
                              ('approved', 'Approved'),
                              ('product received', 'Product Received'),
                              ('done', 'Done'),
                              ('cancelled', 'Cancelled'),
                              ], required=True, default='draft')

    @api.onchange('partner')
    def onchange_partner(self):
        """function for autofilling of partner address"""
        for rec in self:
            return

    # Function for generating warranty number
    # @api.model
    # def create(self, vals):
    #     if vals.get('warranty_number', 'New') == 'New':
    #         vals['warranty_number'] = self.env['ir.sequence'].next_by_code(
    #             'self.service') or 'New'
    #     product_id = self.env['product.product'].search([('id', '=', vals['product'])])
    #     account_move_id = self.env['account.move'].search([('id', '=', vals['invoice'])])
    #     expiry_date = account_move_id.invoice_date + timedelta(product_id.product_tmpl_id.warranty_period)
    #     vals['expiry_date'] = expiry_date
    #     result = super(product_warranty, self).create(vals)
    #     return result

    # Function for getting product id from invoice
    @api.onchange('invoice')
    def onchange_invoice(self):
        pro = []
        for rec in self.invoice.invoice_line_ids:
            pro.append(rec.product_id.id)
            if self.expiry_date and self.current_date:
                if self.expiry_date <= self.current_date:
                    raise ValidationError("Warranty for the product is expired")
        return {'domain': {'product': [('id', 'in', pro),('has_warranty','=' , True)]}}

    @api.model
    def create(self, vals):
        if vals.get('warranty_number', 'New') == 'New':
            vals['warranty_number'] = self.env['ir.sequence'].next_by_code('self.service', ) or 'New'
        result = super(product_warranty, self).create(vals)
        return result

    @api.onchange('product')
    def compute_expiry_date(self):
        if self.invoice_date != False:
            expiration_date = self.invoice.invoice_date + timedelta(days=self.product.warranty_period)
            self.write({'expiry_date': expiration_date})
            if self.expiry_date and self.current_date:
                if self.expiry_date <= self.current_date:
                    raise ValidationError("Warranty for the product is expired")

        # Function for showing warranty expire warning message

    # @api.constrains('expiry_date', 'invoice_date')
    # def check_expiry_date(self):
    #     if self.expiry_date and self.current_date:
    #         if self.expiry_date <= self.current_date:
    #             raise ValidationError("Warranty for the product is expired")
