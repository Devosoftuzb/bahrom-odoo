from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Task(models.Model):
    _name = 'todo.task'
    _description = 'ToOo Task'
    _inherit = 'mail.thread'

    name = fields.Char(string='Task name', required=True)
    status = fields.Selection([('not_completed', 'Not Completed'),
                               ('completed', 'Completed')], string='Status of task', default='not_completed')
    start_date = fields.Datetime(string='Start date')
    end_date = fields.Datetime(string='End date')
    notes = fields.Text(string='Task notes')
    color = fields.Char(string='Color')

    assignment_members_ids = fields.Many2many('res.partner', string='Assignment Members')

    def action_completed(self):
        self.status = 'completed'

    def action_not_completed(self):
        self.status = 'not_completed'

    def _validate_status(self):
        user_ids = self.env['todo.task'].search([
            ('assignment_members_ids', 'in', [self.env.user.id])
        ])

        if not user_ids:
            raise ValidationError('You are not assignment to this task')

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError('End date cannot be before start date')


class Tag(models.Model):
    _name = 'todo.tag'
    _description = 'TODO tasks` tags'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    color = fields.Integer(string="Color")
