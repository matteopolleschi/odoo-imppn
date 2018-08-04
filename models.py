# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime

import pytz

from openerp import models, fields, api, _, tools
from openerp.exceptions import Warning
from openerp.osv import osv, fields, orm

from pyimppn import imppn_line
import psycopg2
import os

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

    
    @api.one
    def test(self):
    	q = open('IMPPN_tests.txt', "a+")
        q.write('test test')
        q.close()


    @api.one
    def alter_table_res_company(self):
        postgresql1 = "ALTER TABLE res_company ADD COLUMN x_teamsystem_id integer;"
        postgresql2 = "UPDATE res_company SET x_teamsystem_id = 5030 WHERE id = 1;"
        cnx_g = None
        try:
            # Connecting python postgresql database
            cnx = psycopg2.connect(host="localhost", port=5432, user="odoo", password="odoo", dbname="db")
            # Creating a cursor object to interact with postgresql db and assign it to a variable cursor
            cur = cnx.cursor()
            # Execute statement or query on db
            cur.execute(postgresql1)
            # committing changes to the table
            cnx.commit()
            # Creating a cursor object to interact with mysql db and assign it to a variable cursor
            cur = cnx.cursor()
            # Execute statement or query on db
            cur.execute(postgresql2)
            # committing changes to the table
            cnx.commit()
            # close communication with the database
            cur.close()
            return true
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if cnx_g is not None:
                cnx_g.close()


    @api.one
    def select_form_account_invoice(self):
        postgresql = "SELECT res_company.teamsystem_id, res_partner.name FROM res_company, account_invoice, res_partner " \
               " WHERE res_partner.id = account_invoice.partner_id AND res_company.id = 1 ;"
        cnx_g = None
        try:
            # Connecting python postgresql database
            cnx = psycopg2.connect(host="localhost", port=5432, user="odoo", password="odoo", dbname="db")
            # Creating a cursor object to interact with mysql db and assign it to a variable cursor
            cur = cnx.cursor()
            # Execute statement or query on db
            cur.execute(postgresql)
            # Fetch all rows of the query executed
            results = cur.fetchall()
            # close communication with the database
            cur.close()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
           if cnx_g is not None:
                cnx_g.close()


	@api.one
    def import_accounting(self):
        result = odooimppn.select_form_account_invoice()
        for i in range(len(result)):
            result_string = imppn_line(
                TRF_DITTA=str(result[i][0]),
                TRF_VERSIONE="3",
                TRF_TARC="0",
                TRF_COD_CLIFOR="",
                TRF_RASO=str(result[i][1]),
                TRF_IND="Via Roma, 44",
                TRF_CAP="19100",
                TRF_CITTA="La Spezia",
                TRF_PROV="SP",
                TRF_COFI="",
                TRF_PIVA="00468990015",
                TRF_PF="N",
                TRF_DIVIDE="",
                TRF_PAESE="",
                TRF_PIVA_ESTERO="",
                TRF_COFI_ESTERO="",
                TRF_SESSO="",
                TRF_DTNAS="",
                TRF_COMNA="",
                TRF_PRVNA="",
                TRF_PREF="",
                TRF_NTELE_NUM="",
                TRF_FAX_PREF="",
                TRF_FAX_NUM="",
                TRF_CFCONTO="",
                TRF_CFCODPAG="",
                TRF_CFBANCA="",
                TRF_CFAGENZIA="",
                TRF_CFINTERM="",
                TRF_CAUSALE="001",
                TRF_CAU_DES="Causale",
                TRF_CAU_AGG="di prova",
                TRF_CAU_AGG_1="",
                TRF_CAU_AGG_2="",
                TRF_DATA_REGISTRAZIONE="15012016",
                TRF_DATA_DOC="15012016",
                TRF_NUM_DOC_FOR="",
                TRF_NDOC="12",
                TRF_SERIE="",
                TRF_EC_PARTITA="",
                TRF_EC_PARTITA_ANNO="",
                TRF_EC_COD_VAL="",
                TRF_EC_CAMBIO="",
                TRF_EC_DATA_CAMBIO="",
                TRF_EC_TOT_DOC_VAL="",
                TRF_EC_TOT_IVA_VAL="",
                TRF_PLAFOND="",
                TRF_IMPONIB="100000",
                TRF_ALIQ="22",
                TRF_ALIQ_AGRICOLA="",
                TRF_IVA11="",
                TRF_IMPOSTA="22000",
                TRF_IMPONIB2="",
                TRF_ALIQ2="",
                TRF_ALIQ_AGRICOLA2="",
                TRF_IVA112="",
                TRF_IMPOSTA2="",
                TRF_IMPONIB3="",
                TRF_ALIQ3="",
                TRF_ALIQ_AGRICOLA3="",
                TRF_IVA113="",
                TRF_IMPOSTA3="",
                TRF_IMPONIB4="",
                TRF_ALIQ24="",
                TRF_ALIQ_AGRICOLA4="",
                TRF_IVA114="",
                TRF_IMPOSTA4="",
                TRF_IMPONIB5="",
                TRF_ALIQ5="",
                TRF_ALIQ_AGRICOLA5="",
                TRF_IVA115="",
                TRF_IMPOSTA5="",
                TRF_IMPONIB6="",
                TRF_ALIQ6="",
                TRF_ALIQ_AGRICOLA6="",
                TRF_IVA116="",
                TRF_IMPOSTA6="",
                TRF_IMPONIB7="",
                TRF_ALIQ7="",
                TRF_ALIQ_AGRICOLA7="",
                TRF_IVA117="",
                TRF_IMPOSTA7="",
                TRF_IMPONIB8="",
                TRF_ALIQ8="",
                TRF_ALIQ_AGRICOLA8="",
                TRF_IVA118="",
                TRF_IMPOSTA8="",
                TRF_TOT_FATT="122000",
                TRF_CONTO_RIC="5805507",
                TRF_IMP_RIC="100000",
                TRF_CAU_PAGAM="",
                TRF_CAU_DES_PAGAM="",
                TRF_CAU_AGG_1_PAGAM="",
                TRF_CAU_AGG_2_PAGAM="",
                TRF_CONTO="",
                TRF_DA="",
                TRF_IMPORTO="",
                TRF_CAU_AGGIUNT="",
                TRF_EC_PARTITA_PAG="",
                TRF_EC_PARTITA_ANNO_PAG="",
                TRF_EC_IMP_VAL="",
                TRF_RIFER_TAB="",
                TRF_IND_RIGA="",
                TRF_DT_INI="",
                TRF_DT_FIN="",
                TRF_DOC6="",
                TRF_AN_OMONIMI="",
                TRF_AN_TIPO_SOGG="",
                TRF_EC_PARTITA_SEZ_PAG="",
                TRF_NUM_DOC_PAG_PROF="",
                TRF_DATA_DOC_PAG_PROF="",
                TRF_RIT_ACC="",
                TRF_RIT_PREV="",
                TRF_RIT_1="",
                TRF_RIT_2="",
                TRF_RIT_3="",
                TRF_RIT_4="",
                TRF_UNITA_RICAVI="",
                TRF_UNITA_PAGAM="",
                TRF_FAX_PREF_1="",
                TRF_FAX_NUM_1="",
                TRF_SOLO_CLIFOR="",
                TRF_80_SEGUENTE="",
                TRF_CONTO_RIT_ACC="",
                TRF_CONTO_RIT_PREV="",
                TRF_CONTO_RIT_1="",
                TRF_CONTO_RIT_2="",
                TRF_CONTO_RIT_3="",
                TRF_CONTO_RIT_4="",
                TRF_DIFFERIMENTO_IVA="",
                TRF_STORICO="",
                TRF_STORICO_DATA="",
                TRF_CAUS_ORI="",
                TRF_PREV_TIPOMOV="",
                TRF_PREV_RATRIS="",
                TRF_PREV_DTCOMP_INI="",
                TRF_PREV_DTCOMP_FIN="",
                TRF_PREV_FLAG_CONT="",
                TRF_RIFERIMENTO="",
                TRF_CAUS_PREST_ANA="",
                TRF_EC_TIPO_PAGA="",
                TRF_CONTO_IVA_VEN_ACQ="",
                TRF_PIVA_VECCHIA="",
                TRF_PIVA_ESTERO_VECCHIA="",
                TRF_RISERVATO="",
                TRF_DATA_IVA_AGVIAGGI="",
                TRF_DATI_AGG_ANA_REC4="",
                TRF_RIF_IVA_NOTE_CRED="",
                TRF_RIF_IVA_ANNO_PREC="",
                TRF_NATURA_GIURIDICA="",
                TRF_STAMPA_ELENCO="",
                TRF_PERC_FORF="",
                TRF_SOLO_MOV_IVA="",
                TRF_COFI_VECCHIO="",
                TRF_USA_PIVA_VECCHIA="",
                TRF_USA_PIVA_EST_VECCHIA="",
                TRF_USA_COFI_VECCHIO="",
                TRF_ESIGIBILITA_IVA="",
                TRF_TIPO_MOV_RISCONTI="",
                TRF_AGGIORNA_EC="",
                TRF_BLACKLIST_ANAG="",
                TRF_BLACKLIST_IVA="",
                TRF_BLACKLIST_IVA_ANA="",
                TRF_CONTEA_ESTERO="",
                TRF_ART21_ANAG="",
                TRF_ART21_IVA="",
                TRF_RIF_FATTURA="",
                TRF_RISERVATO_B=""
            )
			# test number 1 
            # good = open(os.path.join(os.path.dirname(__file__), 'IMPPN_tests.txt'), 'r+').readlines()[0] 
            # self.assertEquals(result_string.rstrip('\r\n'), good)
            # test number 2 
            f = open('IMPPN_tests.txt', "a+")
            f.write(result_string)
            f.close()
            
# if __name__ == '__main__':
odooimppn.test()
#  	if odooimppn.alter_table_res_company() == true : odooimppn.import_accounting()
#	else : print "altering table res_company wasn't succesfull ..."