from odoo import fields, models, api


class HrEmployeeInherit(models.Model):
    _name = 'hr.employee'

    name = fields.Char()
