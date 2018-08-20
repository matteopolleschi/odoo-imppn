# -*- coding: utf-8 -*-

import base64
import pyimppn

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError


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
                'TRF_NTELE_NUM': invoice.partner_id.phone and invoice.partner_id.phone.replace(' ', ''),
                'TRF_DATA_REGISTRAZIONE': fields.Date.from_string(invoice.date_invoice).strftime('%d%m%Y'),
                'TRF_DATA_DOC': fields.Date.from_string(invoice.date_invoice).strftime('%d%m%Y'),
                'TRF_NDOC': invoice.number and invoice.number.split('/')[-1],
                'TRF-TOT-FATT': invoice.amount_total
            }

            if len(invoice.invoice_line) > 8:
                raise exceptions.ValidationError(_('Max 8 lines allowed'))

            invoice_line_total_tax = 0.0
            for i, line in enumerate(invoice.invoice_line):
                vat_code = 0
                vat_amount = 0.0
                if line.invoice_line_tax_id:
                    vat_code = line.invoice_line_tax_id[0].amount * 100.0

                    taxes = \
                        line.invoice_line_tax_id[0].compute_all(
                            (line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)),
                            line.quantity, line.product_id, invoice.partner_id)['taxes']
                    for tax in taxes:
                        if invoice.type in ('out_invoice', 'in_invoice'):
                            vat_amount = tax['amount'] * line.quantity * tax['base_sign']
                        else:
                            vat_amount = tax['amount'] * line.quantity * tax['ref_base_sign']

                invoice_line_total_tax += vat_amount
                index = str(i + 1) if i != 0 else ''
                values['TRF-IMPONIB' + index] = line.price_subtotal
                values['TRF-ALIQ' + index] = vat_code
                values['TRF-IMPOSTA' + index] = vat_amount
                values['TRF-CONTO-RIC' + index] = line.account_id.code

                assert invoice_line_total_tax == invoice.amount_tax, "That the invoice number %s has unmatched taxes." % invoice.number
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
