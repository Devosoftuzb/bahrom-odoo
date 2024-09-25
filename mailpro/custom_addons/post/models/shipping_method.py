from odoo import models


class ShippingMethod(models.Model):
    _inherit = 'delivery.carrier'

    def get_price(self, weight):
        # Default price for cargo up to 1 kg
        base_price = 15000

        if weight <= 1:
            return base_price
        elif weight <= 5:
            return base_price
        elif weight <= 30:
            # Calculate additional cost for weights over 5 kg
            additional_weight = weight - 5
            return base_price + (additional_weight * 1000)
        else:
            # Calculate additional cost for weights over 30 kg
            additional_weight = weight - 30
            return base_price + (5 * 1000) + (additional_weight * 2000)
