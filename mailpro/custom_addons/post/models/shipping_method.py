from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    promo_code = fields.Char()

    def _compute_custom_shipping_cost(self, order):
        """
        Calculate shipping cost based on the following rules:
        - $15 for up to 5kg
        - $1 per kg from 5kg to 30kg
        - $2 per kg for weight beyond 30kg
        - No additional charge for cargo up to 1 cubic meter
        - An additional 30,000 soums for cargo over 1 cubic meter
        - Cargo over 2 cubic meters is not accepted
        """
        # Calculate total weight
        total_weight = sum(line.product_id.weight * line.product_uom_qty for line in order.order_line)

        # Calculate total volume (cubic meters)
        total_volume = sum((line.product_id.volume or (
                    line.product_id.length * line.product_id.width * line.product_id.height / 1000000)) * line.product_uom_qty
                           for line in order.order_line)

        # Check if cargo exceeds 2 cubic meters
        if total_volume > 2:
            raise ValidationError("Cargo over 2 cubic meters is not accepted.")

        # Base shipping cost based on weight
        if total_weight <= 5:
            shipping_cost = 15
        elif total_weight <= 30:
            shipping_cost = 15 + (total_weight - 5) * 1
        else:
            shipping_cost = 15 + (30 - 5) * 1 + (total_weight - 30) * 2

        # Add additional charge for cargo over 1 cubic meter
        if total_volume > 1:
            shipping_cost += 30000  # Add 30,000 soums

        return shipping_cost

    def rate_shipment(self, order):
        """
        Override the rate_shipment method to include custom shipping cost logic.
        """
        shipping_cost = self._compute_custom_shipping_cost(order)
        return {
            'success': True,
            'price': shipping_cost,
            'error_message': False,
            'warning_message': False
        }
