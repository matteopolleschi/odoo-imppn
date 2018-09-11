# -*- coding: utf-8 -*
#
#    Copyright 2018 Matteo Polleschi <yes@daphne-solutions.com>
#    Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#    Copyright 2018 Odoo Italia Associazione <https://odoo-italia.org/>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#-
from openerp import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'

    teamsystem_id = fields.Integer('Team System ID')
