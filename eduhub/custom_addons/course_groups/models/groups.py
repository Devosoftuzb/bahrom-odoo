from odoo import fields, models, api


class Group(models.Model):
    _name = 'eduhub.group'
    _description = 'Description'

    name = fields.Char()
    description = fields.Text()
    course = fields.Many2one('eduhub.course')
    students = fields.Many2many('res.partner')
    start_time = fields.Char()
    week_days = fields.Selection([('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
                                  ('thursday', 'Thursday'), ('friday', 'Friday'), ('sunday', 'Sunday'),
                                  ('saturday', 'Saturday')])
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')])
