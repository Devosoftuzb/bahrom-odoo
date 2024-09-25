from odoo import models, fields


class PromoCode(models.Model):
    _name = 'post.promo.code'
    _description = 'Promo Codes'

    code = fields.Char('Promo code', required=True)
    availability = fields.Datetime('Available to the', required=True)
    type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], default='fixed')
    fixed_price = fields.Float('Fixed Price')
    percentage = fields.Float('Percentage')
    notes = fields.Text()
