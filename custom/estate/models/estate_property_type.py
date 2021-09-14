import odoo.fields
from odoo import fields, models

class estate_property_type_window(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type table"

    name = fields.Char(required = True)

