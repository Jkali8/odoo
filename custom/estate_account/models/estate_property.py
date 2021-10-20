from odoo import fields, models, api


class InheritedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        values = {
            "partner_id": self.buyer_id.id,
            "move_type": 'out_invoice',
            "journal_id": self.env['account.move'].with_context(
                default_move_type='out_invoice')._get_default_journal().id,
            "invoice_line_ids":
                [
                    (0,
                     0,
                     {
                         "name": "administrative fees",
                         "quantity": 1,
                         "price_unit": 100
                     }

                     ),
                    (0,
                     0,
                     {
                         "name": "Commission",
                         "quantity": 1,
                         "price_unit": round(self.selling_price * 0.06, 2)
                     }

                     )
                ]
        }
        self.env["account.move"].create(values)
        return super().action_sold()
