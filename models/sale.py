# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import datetime

from openerp import api, models, registry


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _create_product_negation(self, line, product_qty):
        """Record a negation for product of line of sale order"""

        ProductRejected = self.env['product.rejected']
        partner_id = line.order_id.partner_id.id \
            if line.order_id.partner_id \
            else False

        with api.Environment.manage():
            with registry(self.env.cr.dbname).cursor() as new_cr:
                new_env = api.Environment(
                    new_cr, self.env.uid, self.env.context)
                ProductRejected.with_env(new_env).create({
                    'product_tmpl_id': line.product_id.product_tmpl_id.id,
                    'product_id': line.product_id.id,
                    'partner_id': partner_id,
                    'qty': product_qty,
                    'company_id': self.env.user.company_id.id,
                    })
                new_env.cr.commit()

        return

    @api.multi
    def button_dummy(self):

        for line in self.order_line:
            if line.product_id.type == 'product':
                product_qty = self.env['product.uom']._compute_qty_obj(
                    line.product_uom,
                    line.product_uom_qty,
                    line.product_id.uom_id)

                if product_qty > (line.product_id.qty_available -
                    line.product_id.outgoing_qty) and product_qty > 0:

                    if self.partner_id:

                        limit_hours = \
                            self.env.user.company_id.product_rejected_limit_hours
                        if limit_hours > 0:

                            ProductRejected = self.env['product.rejected']
                            last_product_negation = ProductRejected.search([
                                ('product_id', '=', line.product_id.id),
                                ('partner_id', '=', self.partner_id.id),
                                ('company_id', '=', self.env.user.company_id.id),
                                ], order='date')

                            if last_product_negation:

                                last_product_negation_date = last_product_negation[-1].date
                                last_product_negation_datetime = datetime.strptime(
                                    last_product_negation_date, '%Y-%m-%d %H:%M:%S')
                                now = datetime.now()
                                diff = now - last_product_negation_datetime
                                hours_diff = (diff.seconds / 60.0) / 60
                                if hours_diff > limit_hours:
                                    self._create_product_negation(
                                        line, product_qty)

                            else:
                                self._create_product_negation(line, product_qty)

                        else:
                            self._create_product_negation(line, product_qty)

                    else:
                        self._create_product_negation(line, product_qty)

        return super(SaleOrder, self).button_dummy()
