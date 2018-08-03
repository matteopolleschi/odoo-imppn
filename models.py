# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime

import pytz

from openerp import models, fields, api, _, tools
from openerp.exceptions import Warning
from openerp.osv import osv, fields, orm

import logging
_logger = logging.getLogger(__name__)

class view(osv.osv):
    _inherit = ['ir.ui.view']

    def __init__(self, pool, cr):
        super(view, self).__init__(pool, cr)
        super(view, self)._columns['type'].selection.append(('odooimppnview','OdooimppnView'))

class companyimppn(models.Model):
    _inherit = ['res.company']

    x_teamsystem_id = fields.Integer(string="Teamsystem id")

class odooimppn(models.Model):
    _name = 'odoo_imppn.content'
    _description = 'Odoo imppn content'