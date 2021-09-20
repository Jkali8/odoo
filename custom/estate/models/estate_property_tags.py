from odoo import fields, models

class estate_property_tags_window(models.Model):
    _name = "estate.property.tags"
    _description = "Estate property tags table"

    name = fields.Char(required = True)