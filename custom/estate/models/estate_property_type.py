import odoo.fields
from odoo import fields, models

class estate_property_type_window(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type table"
    _order = "sequence , name "

    name = fields.Char(required = True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order names. Lower is better.")

    _sql_constraints = [
         ('name_unique', 'unique(name)',
             'The type should be unique.')]