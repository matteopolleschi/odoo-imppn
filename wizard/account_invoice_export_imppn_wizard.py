# -*- coding: utf-8 -*
#
#    Copyright 2018 Matteo Polleschi <yes@daphne-solutions.com>
#    Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#    Copyright 2018 Odoo Italia Associazione <https://odoo-italia.org/>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#-
import base64
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import openerp.release as release
from pyimppn import imppn_line


class account_invoice_export_imppn(models.TransientModel):
    _name = 'account.invoice.export.imppn'

    company_id = fields.Many2one('res.company', 'company')
    start = fields.Date('Start')
    end = fields.Date('End')
    data = fields.Binary()
    filename = fields.Char()

    @api.multi
    def build_vat_struct(self, invoice):
        # Code extracted from VAT communication
        account_tax_model = self.env['account.tax']
        inv_line = {}
        sum_amounts = {}
        for f in ('total', 'taxable', 'tax', 'discarded'):
            sum_amounts[f] = 0.0
        for invoice_tax in invoice.tax_line:
            tax_nature = False
            tax_payability = 'I'
            tax_rate = 0.0
            tax_nodet_rate = 0.0
            tax_type = ''
            if invoice_tax.tax_code_id:
                if invoice_tax.tax_code_id.notprintable:
                    continue
                if invoice_tax.tax_code_id.exclude_from_registries:
                    continue
                taxcode_base_id = invoice_tax.tax_code_id.id
                taxcode_vat_id = False
                where = [('tax_code_id', '=', taxcode_base_id)]
            else:
                if invoice_tax.base_code_id.notprintable:
                    continue
                if invoice_tax.base_code_id.exclude_from_registries:
                    continue
                taxcode_base_id = invoice_tax.base_code_id.id
                taxcode_vat_id = invoice_tax.tax_code_id.id
                where = [('base_code_id', '=', taxcode_base_id)]
            # for tax in invoice_tax.tax_code_id.tax_ids:
            for tax_id in account_tax_model.search(where):
                tax = account_tax_model.browse(tax_id.id)
                if tax and not tax.parent_id:
                    if tax.amount > tax_rate:
                        tax_rate = tax.amount
                    if tax.non_taxable_nature:
                        tax_nature = tax.non_taxable_nature
                    if tax.payability:
                        tax_payability = tax.payability
                    if tax.type_tax_use:
                        tax_type = tax.type_tax_use
                else:
                    if release.major_version == '6.1':
                        tax_rate = 0
                        for child in account_tax_model.browse(
                                tax.parent_id.id).child_ids:
                            if child.type == 'percent':
                                tax_rate += child.amount
                        tax_nodet_rate = 1 - (tax.amount / tax_rate)
                    else:
                        if tax.type == 'percent' and \
                                tax.amount > tax_nodet_rate:
                            tax_nodet_rate = tax.amount
                        tax = account_tax_model.browse(
                            tax.parent_id.id)
                        taxcode_base_id = invoice_tax.tax_code_id.id
                        if tax.amount > tax_rate:
                            tax_rate = tax.amount
            if tax_nature == 'FC' or (tax_nature == 'N2' and
                                      not invoice.partner_id.vat):
                if invoice.type[-7:] == '_refund':
                    sum_amounts['discarded'] -= round(
                        invoice_tax.base + invoice_tax.amount, 2)
                else:
                    sum_amounts['discarded'] += round(
                        invoice_tax.base + invoice_tax.amount, 2)
                continue
            if taxcode_base_id not in inv_line:
                inv_line[taxcode_base_id] = {}
                inv_line[taxcode_base_id]['amount_taxable'] = 0.0
                inv_line[taxcode_base_id]['amount_tax'] = 0.0
                inv_line[taxcode_base_id]['amount_total'] = 0.0
                inv_line[taxcode_base_id]['tax_vat_id'] = taxcode_vat_id
                inv_line[taxcode_base_id]['tax_rate'] = tax_rate
                inv_line[taxcode_base_id][
                    'tax_nodet_rate'] = tax_nodet_rate
                inv_line[taxcode_base_id]['tax_nature'] = tax_nature
                inv_line[taxcode_base_id][
                    'tax_payability'] = tax_payability
            if tax_rate and not inv_line[taxcode_base_id]['tax_rate']:
                inv_line[taxcode_base_id]['tax_rate'] = tax_rate
            if tax_nodet_rate and not inv_line[taxcode_base_id][
                    'tax_nodet_rate']:
                inv_line[taxcode_base_id][
                    'tax_nodet_rate'] = tax_nodet_rate
            if tax_payability and not inv_line[taxcode_base_id][
                    'tax_payability']:
                inv_line[taxcode_base_id][
                    'tax_payability'] = tax_payability
            inv_line[taxcode_base_id]['amount_taxable'] += invoice_tax.base
            inv_line[taxcode_base_id]['amount_tax'] += invoice_tax.amount
            inv_line[taxcode_base_id]['amount_total'] += round(
                invoice_tax.base + invoice_tax.amount, 2)
            if invoice.type[-7:] == '_refund':
                sum_amounts['taxable'] -= invoice_tax.base
                sum_amounts['tax'] -= invoice_tax.amount
                sum_amounts['total'] -= round(
                    invoice_tax.base + invoice_tax.amount, 2)
            else:
                sum_amounts['taxable'] += invoice_tax.base
                sum_amounts['tax'] += invoice_tax.amount
                sum_amounts['total'] += round(
                    invoice_tax.base + invoice_tax.amount, 2)
        # End extraction
        return inv_line, sum_amounts

    @api.multi
    def download(self):
        rows = ''
        for invoice in self.env['account.invoice'].search(
                [('date_invoice', '>=', self.start),
                 ('date_invoice', '<=', self.end),
                 ('company_id', '=', self.company_id.id),
                 ('state', 'not in', ('cancel', 'draft'))]):
            street = ''
            if invoice.partner_id.street:
                street += invoice.partner_id.street
            if invoice.partner_id.street2:
                street += '\n' + invoice.partner_id.street2

            values = {
                'TRF_RASO': invoice.partner_id.name,
                'TRF_IND': invoice.partner_id.street,
                'TRF_CAP': invoice.partner_id.zip,
                'TRF_CITTA': invoice.partner_id.city,
                'TRF_PROV': invoice.partner_id.state_id.code,
                'TRF_PIVA': invoice.partner_id.vat,
                'TRF_PF': 'N' if invoice.partner_id.is_company else 'S',
                'TRF_NTELE_NUM': invoice.partner_id.phone, 
                'TRF_DATA_REGISTRAZIONE': invoice.registration_date,
                'TRF_DATA_DOC': invoice.date_invoice,
                'TRF_NDOC': invoice.number,
                'TRF-TOT-FATT': invoice.amount_total,
            }

            if len(invoice.invoice_line) > 8:
                raise Warning(_('Max 8 lines allowed'))
            inv_line, sum_amounts = self.build_vat_struct(invoice)
            for i in inv_line:
                index = str(i + 1) if i != 0 else ''
                values['TRF-IMPONIB' + index] = inv_line[i]['amount_taxable']
                values['TRF-ALIQ' + index] = inv_line[i]['tax_rate']
                values['TRF-IMPOSTA' + index] = inv_line[i]['amount_tax']
                # FIX: account_id.code
                values['TRF-CONTO-RIC' + index] = inv_line[i]['tax_rate']
            row = imppn_line(**values)
            rows += row

        self.data = base64.b64encode(rows)
        self.filename = '%s_%s.txt' % (
            fields.Date.from_string(self.start).strftime('%d%m%Y'),
            fields.Date.from_string(self.end).strftime('%d%m%Y'))
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/web/binary/saveas?model=%s&field=%s&id=%s&filename_field=%s' % (
                self._name, 'data', self.id, 'filename'),
        }
