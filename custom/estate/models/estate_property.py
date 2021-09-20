from dateutil.relativedelta import relativedelta

import odoo.fields
from odoo import fields, models, api


class estate_property_window(models.Model):
    _name = "estate.property"
    _description = "Estate property table"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False,default=lambda self: fields.Datetime.now() + relativedelta(months=+3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default= 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = odoo.fields.Boolean(default = True)
    state = odoo.fields.Selection([('N','New'),('OR','Offer recieved'),('OA','Offer accepted'),('S','Sold'),('C','Canceled')],
                                  required = True, copy= False, default = 'N')
    property_type_id = fields.Many2one("estate.property.type", string ="Type")
    salesperson_id = fields.Many2one("res.partner", string ="Salesman")
    buyer_id = fields.Many2one("res.users", string = "Buyer",default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute = "_compute_total_area")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            S



