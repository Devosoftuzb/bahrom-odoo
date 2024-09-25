from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sender_id = fields.Many2one('res.partner', string='Product Sender')
    receiver_id = fields.Many2one('res.partner', string='Product Receiver')

    promo_code = fields.Char(string='Promo Code', inverse='_check_promo_code')

    carrier_price = fields.Float(string='Shipping Cost')

    def _check_promo_code(self):
        for rec in self:
            promo_code = self.env['post.promo.code'].search([('code', '=', rec.promo_code)], limit=1)
            if promo_code:
                if promo_code.type == 'fixed':
                    rec.carrier_price -= promo_code.fixed_price
                elif promo_code.type == 'percentage':
                    rec.carrier_price *= (1 - (promo_code.percentage / 100))
            else:
                raise ValidationError('Promo Code is not available!')

    @api.depends('weight')
    def _onchange_order_weight(self):
        for order in self:
            if order.weight:
                shipping_cost = self._calculate_shipping_cost(order.weight)
                order.carrier_price = shipping_cost

    def _calculate_shipping_cost(self, weight):
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
