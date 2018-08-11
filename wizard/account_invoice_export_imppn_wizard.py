# -*- coding: utf-8 -*-

# import os
import base64

from openerp import models, fields, api, _
from pyimppn import imppn_line


class account_invoice_export_imppn(models.TransientModel):
    _name = 'account.invoice.export.imppn'

    start = fields.Date('Start')
    end = fields.Date('End')
    data = fields.Binary()
    filename = fields.Char()

    @api.multi
    def download(self):
        rows = ''
        for invoice in self.env['account.invoice'].search(
                ['&', ('date_invoice', '>=', self.start), ('date_invoice', '<=', self.end)]):
            street = ''
            if invoice.partner_id.street:
                street += invoice.partner_id.street
            if invoice.partner_id.street2:
                street += '\n' + invoice.partner_id.street2

            values = {
                'TRF_RASO': invoice.partner_id.name,
                'TRF_IND': street,
                'TRF_CAP': invoice.partner_id.zip or '',
                'TRF_CITTA': invoice.partner_id.city or '',
                'TRF_PROV': invoice.partner_id.state_id.id or '',
                'TRF_PIVA': invoice.partner_id.vat or '',
                'TRF_PF': 'N' if invoice.partner_id.is_company else 'S',
                'TRF_NTELE_NUM': invoice.partner_id.phone.replace(' ', ''),
                'TRF_DATA_REGISTRAZIONE': fields.Date.from_string(invoice.date_invoice).strftime('%d%m%Y'),
                'TRF_DATA_DOC': fields.Date.from_string(invoice.date_invoice).strftime('%d%m%Y'),
                'TRF_NDOC': invoice.number.split('/')[-1],
                'TRF-TOT-FATT': invoice.amount_total
            }

            if len(invoice.invoice_line) > 8:
                raise Warning(_('Max 8 lines allowed'))

            for i, line in enumerate(invoice.invoice_line):
                index = str(i + 1) if i != 0 else ''
                values['TRF-IMPONIB' + index] = line.price_subtotal
                values['TRF-ALIQ' + index] = ''
                values['TRF-IMPOSTA' + index] = ''
            row = imppn_line(**values)
            rows += row

        self.data = base64.b64encode(rows)
        self.filename = fields.Date.from_string(self.start).strftime('%d%m%Y') + '_' + \
                        fields.Date.from_string(self.end).strftime('%d%m%Y') + '.txt'
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/web/binary/saveas?model=%s&field=%s&id=%s&filename_field=%s' % (
                self._name, 'data', self.id, 'filename'),
        }
