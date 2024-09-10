from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import timedelta


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
    status = fields.Selection([('new', 'New'), ('received', 'Offer Received'),
                               ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                               ('cancel', 'Cancel')],
                             default='new', string='Status')
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", readonly=True)
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Float(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Float(string="Garden area")
    garden_orientation = fields.Selection([('north', 'North'),
                                           ('south', 'South'),
                                           ('east', 'East'),
                                           ('west', 'West')],
                                          string="Garden Orientation", default="north")
    total_area = fields.Float(string="Total Area(sqm)", compute='_compute_total_area')
    ref = fields.Char(string="Reference")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tags_id = fields.Many2many('estate.property.tag', string="Tags")
    offers_id = fields.One2many("estate.property.offer", "property_id", string="Offers")
    sales_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain=[('is_company', '=', True)])
    phone = fields.Char(string="Phone", related="buyer_id.phone")
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends('offers_id')
    def _compute_best_price(self):
        for rec in self:
            if rec.offers_id:
                rec.best_offer = max(rec.offers_id.mapped('price'))
            else:
                rec.best_offer = 0

    @api.depends('offers_id')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offers_id)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    # @api.onchange('living_area', 'garden_area')
    # def _onchange_total_area(self):
    #     self.total_area = self.living_area + self.garden_area

    def action_sold(self):
        self.status = 'sold'

    def action_cancel(self):
        self.status = 'cancel'


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    _inherit = "mail.thread"
    
    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")


class AbstractOffer(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'Abstract offers'

    partner_email = fields.Char(string='Email')
    partner_phone = fields.Char(string='Phone Number')


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _inherit = ['mail.thread', 'abstract.model.offer']

    name = fields.Char(string="Description", compute='_compute_name')
    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner")
    validity = fields.Integer(string="Validity(days)")
    deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    property_id = fields.Many2one("estate.property", string="Property")
    creation_date = fields.Date(string="Creation Date", default=lambda self: self._set_create_date())

    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price': self.price,
                'status': 'accepted',
            })
            self.property_id.selling_price = self.price
        self.status = 'accepted'

    def _validate_accepted_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])

        if offer_ids:
            raise ValidationError('You have an accepted offer already')

    def action_decline_offer(self):
        self.status = 'refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'status': 'received',
            })

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f'{rec.property_id} - {rec.partner_id}'
            else:
                rec.name = False

    @api.depends('validity', 'creation_date')  # use data from class fields
    @api.depends_context('uid')  # use data from context
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    # @api.audovacuum
    # def _clean_offers(self):
    #     """
    #     CronJob to delete offer when refused
    #     """
    #     self.search(["status", "=", "refused"]).unlink()

    @api.model
    def _set_create_date(self):
        return fields.Date.today()

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if not val.get('creation_date'):
                val['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    @api.constrains("validity")
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline cannot be before creation date"))

    # _sql_constrains = [
    #     ('check_validity', 'check(validity > 0)', 'Deadline cannot be before creation date')
    # ]

    def write(self, vals):
        """
        When data changed this function work
        """
        self.env['res.partner'].browse(1)
        self.env['res.partner'].search([('is_company', '=', True)])  # compare data
        # self.env['res.partner'].search([
        #     ('is_company', '=', True),
        #     ...
        # ], limit=1, order="name desc")
        self.env['res.partner'].search_count([('is_company', '=', True)])
        # self.env['res.partner'].search([('is_company', '=', True)]).unlink()
        # self.env['res.partner'].search_count([('is_company', '=', True)]).mapped('phone')
        # self.env['res.partner'].search_count([('is_company', '=', True)]).filtered(lambda x: x.phone == '(132)-2323-233')
        return super(PropertyOffer, self).write(vals)

    # def unlink(self):
    #     """
    #     Delete method
    #     """
