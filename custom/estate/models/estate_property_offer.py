from odoo import fields, models

class estate_property_offer_window(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers table"

    price = fields.Float()
    status = fields.Selection([('A','Accepted'),('R','Refused')],copy= False)
    partner_id = fields.Many2one("res.partner", string="Partner", required = True)
    property_id = fields.Many2one("estate.property",string= "Property", required = True)

