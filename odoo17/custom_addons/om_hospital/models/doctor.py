from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = "mail.thread"
    _description = "Doctor Records"
    _rec_name = "ref"

    name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=True)
    ref = fields.Char(string="Reference", default=lambda self: _('New'))
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.doctor')

        return super(HospitalDoctor, self).create(vals_list)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, f"{rec.ref} - {rec.name}"))
        return res
