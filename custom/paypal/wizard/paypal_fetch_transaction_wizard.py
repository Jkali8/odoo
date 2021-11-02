import paypalrestsdk
import werkzeug
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api


PAYPAL_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S+0000'


class PaypalFetchTransactionWizard(models.TransientModel):

    _name = "paypal.fetch.transaction.wizard"

    paypal_configuration_id = fields.Many2one("paypal.configuration", string='Configuration')
    date_from = fields.Datetime(default=lambda self: fields.Datetime.now())
    date_to = fields.Datetime(default=lambda self: fields.Datetime.now() + relativedelta(days=+ 30))

    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AXgjUNvQotCZGPAyMwzPFE0trEm375xavEaeLS-nvfLSm-HOAaVk0hjjGfoUJcBZtQKAJCZ9MmWNQLo9",
        "client_secret": "ELDvE_-03aIrehmKkYJlgRVPSlDzCAAf-APBKFRxdR_C6rWLU4m9-Rx-TBXHOCRiQpntibqpeulpdSJ3"})

    def _create_transaction(self,vals):
            api_client = paypalrestsdk.Api({
                'mode': 'sandbox',
                'client_id': self.paypal_configuration_id.access_key,
                'client_secret': self.paypal_configuration_id.secret_key
            })
            fragment = {
                'start_date': self.date_from.strftime(PAYPAL_DATETIME_FORMAT),
                'end_date': self.date_to.strftime(PAYPAL_DATETIME_FORMAT),
                'fields': 'all',
                'transaction_status': 'S',
                'balance_affecting_records_only': 'Y',
                'page_size': 1,

            }
            request_url = 'v1/reporting/transactions?' + werkzeug.urls.url_encode(fragment)
            transaction_response = api_client.get(request_url)
            if 'error' in transaction_response.keys():
                print(transaction_response['error']['message'])
            else:
                transactions = transaction_response['transaction_details']
                return transactions
