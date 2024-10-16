from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Task(models.Model):
    _name = 'todo.task'
    _description = 'ToOo Task'
    _inherit = 'mail.thread'

    name = fields.Char(string='Task name', required=True)
    status = fields.Selection([('not_completed', 'Not Completed'),
                               ('completed', 'Completed')], string='Status of task', default='not_completed')
    start_date = fields.Datetime(string='Start date (optional)')
    end_date = fields.Datetime(string='End date (optional)')
    notes = fields.Text(string='Task notes')
    tags_ids = fields.Many2many('todo.tag', string='Tags')
    categories_ids = fields.Many2one('todo.category', string='Categories')
    color = fields.Char(string='Color', default="#ffffff")

    location_latitude = fields.Float(string='Latitude', track_visibility='onchange')
    location_longitude = fields.Float(string='Longitude', track_visibility='onchange')

    assignment_members_ids = fields.Many2many('res.partner', string='Assignment Members')

    def action_completed(self):
        self._validate_status() # validate action
        self.status = 'completed'

    def action_not_completed(self):
        self._validate_status()  # validate action
        self.status = 'not_completed'

    def _validate_status(self):
        for task in self:
            if self.env.user.id not in task.assignment_members_ids.ids:
                if task.create_uid.id != self.env.user.id:
                    raise ValidationError("You are not assignment to perform this action for task: %s" % task.name)

    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError('End date cannot be before start date')


class AbstractLabel(models.AbstractModel):
    _name = 'abstract.model.label'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    color = fields.Integer(string="Color")


class Category(models.Model):
    _name = 'todo.category'
    _description = 'TODO tasks categories'
    _inherit = 'abstract.model.label'


class Tag(models.Model):
    _name = 'todo.tag'
    _description = 'TODO tasks` tags'
    _inherit = 'abstract.model.label'
