# -*- coding: utf-8 -*-

from openerp import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'

    teamsystem_id = fields.Integer('Team System ID')
