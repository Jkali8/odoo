from odoo import fields, models, api

class resUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'salesperson_id', string = 'property',
                                   domain = ['|', ('state', '=', 'N'),('state','=','OR')])