from odoo import models, fields, api


class Brand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Name')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    brand_id = fields.Many2one('product.brand', string='Brand')

    def has_bought_product(self, product_id):
        self.ensure_one()

        purchase_orders = self.env['sale.order'].search([
            ('partner_id', '=', self.id),
            ('order_line.product_id.product_tmpl_id', '=', product_id),
            ('state', '=', 'sale')  # Make sure the order is confirmed
        ])

        return bool(purchase_orders)

    def my_product_reviews(self, product_id):
        self.ensure_one()

        reviews = self.env['product.review'].search([
            ('product_id', '=', product_id),
            ('partner_id', '=', self.id),
        ])

        return reviews


class ProductReview(models.Model):
    _name = 'product.review'
    _description = 'Review model for products'

    product_id = fields.Many2one('product.template', string='Product', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    rating = fields.Integer(string='Rating', required=True)
    comment = fields.Text(string='Comment')
    purchase_order_id = fields.Many2one('sale.order', string='Purchase Order')

    @api.model
    def create(self, vals):
        purchase_orders = self.env['sale.order'].search([
            ('partner_id', '=', vals['partner_id']),
            ('order_line.product_id.product_tmpl_id', '=', vals['product_id']),
            ('state', '=', 'sale')
        ])
        if not purchase_orders:
            raise ValueError("You can only review products you have purchased.")

        vals['purchase_order_id'] = purchase_orders[0].id
        return super(ProductReview, self).create(vals)
