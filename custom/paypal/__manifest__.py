{
    'name': "Paypal",
    'version': '1.0',
    'depends': ['base','payment'],
    'author': "JK",
    'category': 'App',

    'data': [
        'views/paypal_configuration_views.xml',
        'views/paypal_transaction_views.xml',
        'views/paypal_menus.xml',
        'security/ir.model.access.csv',
        'wizard/paypal_fetch_transaction_wizard_views.xml'
      ],
}