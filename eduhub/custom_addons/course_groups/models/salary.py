from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Salary(models.Model):
    _name = 'eduhub.salary'
    _description = 'Salary of teachers'

    price = fields.Float(string='Salary', required=True)
    teacher_id = fields.Many2one('hr.employee', string='Teacher', required=True)
    notes = fields.Text()
