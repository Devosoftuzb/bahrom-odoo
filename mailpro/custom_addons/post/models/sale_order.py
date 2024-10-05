from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def write(self, vals):
        for record in self:
            if (record.company_id.id != self.env.user.company_id.id and
                record.user_id.id != record.env.user.id):
                raise ValidationError('You only can edit branch of yours.')
        return super().write(vals)
