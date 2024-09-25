from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _compute_shipping_cost(self):
        for order in self:
            total_weight = sum(product.weight * product.qty for product in order.order_line)
            shipping_cost = self.env['delivery.carrier'].get_price(total_weight)
            order.shipping_cost = shipping_cost
