from odoo import models, fields


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    fragile = fields.Boolean(default=False)
