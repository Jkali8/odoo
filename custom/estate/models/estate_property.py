from dateutil.relativedelta import relativedelta

import odoo.fields, datetime
from odoo.exceptions import UserError,Warning, ValidationError
from odoo import fields, models, api
from odoo.osv.osv import osv
from odoo.tools import float_compare


class estate_property_window(models.Model):
    _name = "estate.property"
    _description = "Estate property table"
    _order = "property_type_id desc"

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
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = odoo.fields.Boolean(default = True)
    state = odoo.fields.Selection([('N','New'),('OR','Offer recieved'),('OA','Offer accepted'),('S','Sold'),('C','Canceled')],
                                  required = True, copy= False, default = 'N')
    property_type_id = fields.Many2one("estate.property.type", string ="Type",)
    salesperson_id = fields.Many2one("res.users", string = "Salesman", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string ="Buyer")
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float(compute = "_compute_total_area")
    best_price = fields.Float(compute = "_compute_best_offer" )

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0 )',
         'The expected price should only be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price must be postive.')
    ]

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price", "expected_price")
    def _compute_best_offer(self):
        for record in self:
                if record.offer_ids.mapped("price"):
                    record.best_price = max(record.offer_ids.mapped("price"))
                else:
                    record.best_price = 0
    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden == True):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancel(self):
        for record in self:
            if record.state != "S":
                record.state = "C"
            else:
                raise  odoo.exceptions.UserError("Sold property can not be canceled!")
        return True

    def action_sold(self):
        for record in self:
            if record.state != "C":
                record.state = "S"
                #print("lol")
            else:
                raise odoo.exceptions.UserError("Canceled property can not be sold!")
        return True

    @api.constrains('expected_price', 'selling_price','state')
    def _check_percent(self):
        for record in self:
            if  record.selling_price != 0:
                if float_compare(record.selling_price, record.expected_price*0.9, precision_digits=3)<0 :
                    raise ValidationError(('The selling price cant be lower than 90 procent of expected price'))

    def unlink(self):
        for record in self:
           if record.state == 'N' or record.state == 'C':
               return super().unlink()
           else:
               raise ValidationError(('The property cannot be deleted only NEW or CANCELED porperties can be deleted'))
