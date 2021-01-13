import logging
import pprint
from odoo import http
import werkzeug
from odoo.http import request
# from odoo.http import request


_logger = logging.getLogger(__name__)

class Checkouts(http.Controller):
    @http.route(['/payment/checkout/'], website=True, auth='user', csrf=False)
    def index(self, **kwargs):
        return request.render("checkouts.checkout_form", {})

    @http.route(['/payment/checkout/redirect/'], type='http', auth='none', methods=['POST'], csrf=False)
    def test_redirect(self, **post):
        print("Redirected")
        return werkzeug.utils.redirect('/payment/checkout/')

    @http.route(['/mondido/checkout'], type="http", auth="user", method=['post'], csrf=False)
    def checkout_response(self, **kwargs):
        print(kwargs, request.httprequest.__dict__)


    @http.route(['/payment/checkout/process'], type="json", auth='public', methods=['POST'], csrf=False)
    def _get_checkout_urls(self, **post):

        return {
            'checkout_form_url': 'https://api.mondido.com/v1/transactions'
        }
