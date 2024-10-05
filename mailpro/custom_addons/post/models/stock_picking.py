from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sender_id = fields.Many2one('res.partner', string='Product Sender')
    receiver_id = fields.Many2one('res.partner', string='Product Receiver')
    sender_branch_id = fields.Many2one('res.company', string='Sender branch', readonly=True, compute='_select_sender_branch')

    state = fields.Selection([('draft', 'Draft'),
                              ('waiting', 'In Store'),
                              ('confirmed', 'Confirmed'),
                              ('assigned', 'In Delivery'),
                              ('done', 'Delivered'),
                              ('cancel', 'Canceled')])

    @api.constrains('sender_branch_id')
    def _select_sender_branch(self):
        for rec in self:
            if self.env.user.company_id:
                rec.sender_branch_id = self.env.user.company_id.id
            else:
                raise ValidationError('You don`t have company')

    def write(self, vals):
        for record in self:
            if record.sender_branch_id.id != self.env.user.company_id.id:
                raise ValidationError('You only can edit branch of yours.')
        return super().write(vals)
