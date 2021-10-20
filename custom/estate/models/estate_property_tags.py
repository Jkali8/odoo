from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate property tags table"
    _order = "name "

    name = fields.Char(required=True)
    color = fields.Integer(default=1)

    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'The tag name should be unique.')]
