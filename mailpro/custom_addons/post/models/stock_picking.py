from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sender_id = fields.Many2one('res.partner', string='Product Sender')
    receiver_id = fields.Many2one('res.partner', string='Product Receiver')

    promo_code = fields.Char(string='Promo Code', inverse='_check_promo_code')
    carrier_price = fields.Float(string='Shipping Cost', compute='_compute_shipping_cost', store=True)

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
