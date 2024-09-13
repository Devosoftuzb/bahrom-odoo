from odoo import http
from odoo.http import request
from odoo.tools import image_data_uri

import io
import xlsxwriter


class ProductController(http.Controller):
    @http.route(['/shop/products/list/excel'], type='http', auth="public", website=True)
    def download_in_excel(self, **kwargs):
        products = request.env['product.template'].search([])

        # Create an in-memory Excel file
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Products')

        # Add headers to the Excel file
        headers = ['Product Name', 'Product Price', 'Image URL']
        worksheet.write_row(0, 0, headers)

        # Add product data to the Excel file
        row = 1
        for product in products:
            # Get product image URL
            image_url = '/web/image/product.product/%s/image_1920' % product.id
            worksheet.write(row, 0, product.name)  # Product Name
            worksheet.write(row, 1, product.list_price)  # Product Price
            worksheet.write(row, 2, image_url)  # Image URL
            row += 1

        # Close the workbook
        workbook.close()

        # Set up the HTTP headers for the response
        output.seek(0)
        response = request.make_response(output.read(), [
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename=product_list.xlsx;')
        ])

        return response
