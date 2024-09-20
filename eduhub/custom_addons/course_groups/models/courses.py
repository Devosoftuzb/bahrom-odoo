from odoo import fields, models, api


class Course(models.Model):
    _name = 'eduhub.course'
    _description = 'Description'

    name = fields.Char()
    description = fields.Text()
    duration = fields.Date()
    instructor = fields.Many2many('hr.employee')
    price = fields.Float()
    image = fields.Binary(attachment=True)
    tags_ids = fields.Many2many('eduhub.course.tag')


class Tag(models.Model):
    _name = 'eduhub.course.tag'
    _description = 'EduHUB Courses` Tags'

    name = fields.Char()
