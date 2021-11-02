
from odoo import fields, models, api


class PaypalConfiguration(models.Model):
    _name = "paypal.configuration"
    _description = "paypal configuration table"

    access_key = fields.Char()
    secret_key = fields.Char()