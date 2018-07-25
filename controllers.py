# -*- coding: utf-8 -*-
from openerp import http

# class Odoo-imppn(http.Controller):
#     @http.route('/odoo-imppn/odoo-imppn/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-imppn/odoo-imppn/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-imppn.listing', {
#             'root': '/odoo-imppn/odoo-imppn',
#             'objects': http.request.env['odoo-imppn.odoo-imppn'].search([]),
#         })

#     @http.route('/odoo-imppn/odoo-imppn/objects/<model("odoo-imppn.odoo-imppn"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-imppn.object', {
#             'object': obj
#         })