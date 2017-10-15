# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    'name': 'Record automatically a negation for products on (update) in a sale',
    'description': '''Records automatically a negation (product_negation) for a
    product that is intended to be sold but has no stock. Extends the method
    button_dummy of the model sale.order to record automatically a negation
    (product_rejected) for products without stock.
    This method is executed when clicking on button (update) in sale orders.''',
    'version': '9.0.1.0.0',
    'category': 'Sales',
    'author': 'Humanytek',
    'website': "http://www.humanytek.com",
    'license': 'AGPL-3',
    'depends': [
        'sale_stock',
        'sale_order_lines_date_next_reception_on_update',
        'product_rejected'],
    'data': [
    ],
    'installable': True,
    'auto_install': False
}
