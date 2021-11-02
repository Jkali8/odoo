from datetime import datetime

import paypalrestsdk
import werkzeug.urls
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PaypalTransaction(models.Model):
    _name = "paypal.transaction"
    _description = "paypal transaction table"

    transaction_id = fields.Char()
    transaction_amount = fields.Float()
    date = fields.Datetime()
    email_client = fields.Char()
    # values_ids = fields.One2many("paypal.fetch.transaction.wizard", "values_id", string="Values")





