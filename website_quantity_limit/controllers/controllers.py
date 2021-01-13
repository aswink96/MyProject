from odoo import http, fields
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from openerp.exceptions import ValidationError


class SaleQuantityLimit(WebsiteSale):
    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        max_qty = request.env['product.product'].sudo().search([('id', '=', product_id)])
        min_qty = request.env['product.product'].sudo().search([('id', '=', product_id)])
        print(product_id)
        print(set_qty)
        print(max_qty.max_quantity_limit)
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            return {}

        value = order._cart_update(product_id=product_id, line_id=line_id, add_qty=add_qty, set_qty=set_qty)

        if not order.cart_quantity:
            request.website.sale_reset()
            return value
        # if(set_qty > max_qty.max_quantity_limit):
        #     raise ValidationError("Warranty for the product is expired")


        order = request.website.sale_get_order()
        value['cart_quantity'] = order.cart_quantity
        value['max_qty1'] = max_qty.max_quantity_limit
        value['min_qty1'] = min_qty.min_quantity_limit
        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories(),



        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template(
            "website_sale.short_cart_summary", {
                'website_sale_order': order,
            })
        return value



    # def checkout_redirection(self, order, ):
    #     # must have a draft sales order with lines at this point, otherwise re
    #
    #     if not order or order.state != 'draft':
    #         request.session['sale_order_id'] = None
    #         request.session['sale_transaction_id'] = None
    #
    #         return request.redirect('/shop')
    #     # max_qty = request.env['product.product'].sudo().search([('id', '=', product_id)])
    #
    #     if order and not order.order_line:
    #         return request.redirect('/shop/cart')
    #     # max_qty2  = request.env.context.get('max_qty.max_quantity_limit')
    #     # max_qty = request.env['product.product'].sudo().search([('id', '=', product_id)])
    #     print("max2",max_qty.max_quantity_limit)
    #     if order.cart_quantity > 10:
    #         return request.redirect('/shop/cart')
    #
    #     # if transaction pending / done: redirect to confirmation
    #     tx = request.env.context.get('website_sale_transaction')
    #     if tx and tx.state != 'draft':
    #         return request.redirect('/shop/payment/confirmation/%s' % order.id)


