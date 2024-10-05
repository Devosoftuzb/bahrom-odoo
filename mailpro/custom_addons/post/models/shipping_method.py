from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def _compute_custom_shipping_cost(self, order):
        total_weight = sum(line.product_id.weight * line.product_uom_qty for line in order.order_line if line.product_id.weight)
        total_volume = sum(line.product_id.volume for line in order.order_line if line.product_id.volume)

        if total_volume > 2:
            raise ValidationError("Cargo over 2 cubic meters is not accepted.")

        if total_weight <= 5:
            shipping_cost = 15
        elif total_weight <= 30:
            shipping_cost = 15 + (total_weight - 5) * 1
        else:
            shipping_cost = 15 + (30 - 5) * 1 + (total_weight - 30) * 2

        if total_volume > 1:
            shipping_cost += 3  # Add 30,000 soums

        return shipping_cost

    def rate_shipment(self, order):
        shipping_cost = self._compute_custom_shipping_cost(order)
        return {
            'success': True,
            'price': shipping_cost,
            'carrier_price': shipping_cost,
            'error_message': False,
            'warning_message': False
        }
