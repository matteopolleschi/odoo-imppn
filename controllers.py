# -*- coding: utf-8 -*-
from openerp import http

# class Odooimppn(http.Controller):
#     @http.route('/odoo-imppn/odoo-imppn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-imppn/odoo-imppn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-imppn.listing', {
#             'root': '/odoo-imppn/odoo-imppn',
#             'objects': http.request.env['odooimppn.odooimppn'].search([]),
#         })

#     @http.route('/odoo-imppn/odoo-imppn/objects/<model("odooimppn.odooimppn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-imppn.object', {
#             'object': obj
#         })