

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class estate_property_offer_window(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers table"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('A','Accepted'),('R','Refused')],copy= False)
    partner_id = fields.Many2one("res.partner", string="Partner", required = True)
    property_id = fields.Many2one("estate.property",string= "Property", required = True)

    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = "_compute_date_deadline",inverse = "_inverse_date_deadline")
    crate_date = fields.Date(default=lambda self: fields.Datetime.now())
    checker = False

    _sql_constraints = [
                           ('check_price', 'CHECK(price >= 0 )',
                            'The  price should only be positive.'),
        ]

    @api.depends("crate_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.crate_date + relativedelta(days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.date_deadline = record.date_deadline
            record.validity = (record.date_deadline - record.crate_date).days


    def action_accepted(self):
        for record in self:
                record.status = 'A'
                record.property_id.state = 'OA'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id.name = record.partner_id.name

    def action_refused(self):
        for record in self:
            if record.status != 'A':
                record.status = 'R'


    @api.model
    def create(self, vals):
        # Do some business logic, modify vals...
        property =  self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < property.best_price:
            raise ValidationError(('the offer must be higher than %s' %property.best_price ))
        # Then call super to execute the parent method
        else:
            property.state = 'OR'
            return super().create(vals)


