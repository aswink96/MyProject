from odoo import models, fields, api
# import base64
# import string
# import random
# import hashlib
#
#
# from Crypto.Cipher import AES
# from odoo.exceptions import ValidationError
# from odoo import api, fields, models
# from datetime import datetime
# from werkzeug import urls
# import hashlib
# import json
import logging
# import requests
# from paytrail import common
#
# from odoo import api, fields, models, _
# from odoo.tools.float_utils import float_compare, float_repr, float_round
# from odoo.addons.payment.models.payment_acquirer import ValidationError
# from datetime import datetime

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('mondido', 'Mondido')], ondelete={'mondido': 'set '
                                                                                            'default'})
    mondido_key_id = fields.Char(string='Merchant ID', required_if_provider='mondido', groups='base.group_user')

    mondido_key_secret = fields.Char(string='Merchant Key', required_if_provider='mondido', groups='base.group_user')