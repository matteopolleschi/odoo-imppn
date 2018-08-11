# -*- coding: utf-8 -*-
from openerp import http

# class Odoo_imppn3(http.Controller):
#     @http.route('/odoo_imppn/odoo_imppn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_imppn/odoo_imppn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_imppn.listing', {
#             'root': '/odoo_imppn/odoo_imppn',
#             'objects': http.request.env['odoo_imppn.odoo_imppn'].search([]),
#         })

#     @http.route('/odoo_imppn/odoo_imppn/objects/<model("odoo_imppn.odoo_imppn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_imppn.object', {
#             'object': obj
#         })
