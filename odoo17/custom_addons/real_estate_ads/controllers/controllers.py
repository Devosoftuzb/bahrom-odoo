from odoo import http


class EstateController(http.Controller):

    @http.route("/estate/", auth="public", website=True)
    def estate(self, **kwargs):
        return "Hello World"
