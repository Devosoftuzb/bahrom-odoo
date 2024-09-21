from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Invoice(models.Model):
    _name = 'eduhub.invoice'
    _description = 'Invoicing for EduHUB'
    _inherit = 'mail.thread'

    number = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                         default=lambda self: self.env['ir.sequence'].next_by_code('eduhub.invoice.sequence'))
    student_id = fields.Many2one('res.partner', string='Choose Student')
    courses_ids = fields.Many2many('eduhub.course', string='Choose Course')
    amount_due = fields.Float()
    amount_paid = fields.Float()
    payment_method_id = fields.One2many('eduhub.invoice.payment', 'invoice_id')
    status = fields.Selection([('paid', 'Paid'), ('pending', 'Pending'),
                               ('overdue', 'Overdue'), ('partially_paid', 'Partially Paid')], default='pending')
    notes = fields.Text()


class PaymentMethods(models.Model):
    _name = 'eduhub.invoice.payment'
    _description = 'Invoicing payment methods'

    name = fields.Char(string='Payment Method Name', required=True)
    invoice_id = fields.Many2one('eduhub.invoice')
    amount = fields.Float()
    transaction_id = fields.Char(string='Transaction ID')
