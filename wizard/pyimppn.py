# -*- coding: utf-8 -*
#
#    Copyright 2018 Matteo Polleschi <yes@daphne-solutions.com>
#    Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
#    Copyright 2018 Odoo Italia Associazione <https://odoo-italia.org/>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#-
'''
The ImppnLine class definition.
'''
from openerp import fields
from unidecode import unidecode
from fixedwidth.fixedwidth import FixedWidth


TRX_TTYPE = {
  'TRF_RASO': 'TRUNC',
  'TRF_IND': 'TRUNC',
  'TRF_CITTA': 'TRUNC',
  'TRF_PIVA': 'VAT',
  'TRF_NTELE_NUM': 'PHONE',
  'TRF_DATA_REGISTRAZIONE': 'DATE',
  'TRF_DATA_DOC': 'DATE',
  'TRF_NDOC': 'NUMB',
  'TRF-TOT-FATT': 'FLOAT3',
}
for i in range(8):
    index = str(i + 1) if i != 0 else ''
    TRX_TTYPE['TRF-IMPONIB' + index] = 'FLOAT0'
    TRX_TTYPE['TRF-IMPOSTA' + index] = 'FLOAT0'


IMPPN_CONFIG = {
  'TRF_DITTA': { 'padding':'0', 'alignment':'right', 'length':5, 'type':'string', 'start_pos':1, 'end_pos':5, 'required':False},
  'TRF_VERSIONE': { 'padding':' ', 'alignment':'right', 'length':1, 'type':'string', 'start_pos':6, 'end_pos':6, 'required':False},
  'TRF_TARC': { 'padding':'0', 'alignment':'right', 'length':1, 'type':'string', 'start_pos':7, 'end_pos':7, 'required':False},
  'TRF_COD_CLIFOR': { 'padding':' ', 'alignment':'right', 'length':5, 'type':'string', 'start_pos':8, 'end_pos':12, 'required':False},
  'TRF_RASO': { 'padding':' ', 'alignment':'left', 'length':32, 'type':'string', 'start_pos':13, 'end_pos':44, 'required':False},
  'TRF_IND': { 'padding':' ', 'alignment':'left', 'length':30, 'type':'string', 'start_pos':45, 'end_pos':74, 'required':False},
  'TRF_CAP': { 'padding':' ', 'alignment':'right', 'length':5, 'type':'string', 'start_pos':75, 'end_pos':79, 'required':False},
  'TRF_CITTA': { 'padding':' ', 'alignment':'left', 'length':25, 'type':'string', 'start_pos':80, 'end_pos':104, 'required':False},
  'TRF_PROV': { 'padding':' ', 'alignment':'left', 'length':2, 'type':'string', 'start_pos':105, 'end_pos':106, 'required':False},
  'TRF_COFI': { 'padding':' ', 'alignment':'left', 'length':16, 'type':'string', 'start_pos':107, 'end_pos':122, 'required':False},
  'TRF_PIVA': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':123, 'end_pos':133, 'required':False},
  'TRF_PF': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':134, 'end_pos':134, 'required':False},
  'TRF_DIVIDE': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':135, 'end_pos':136, 'required':False},
  'TRF_PAESE': { 'padding':' ', 'alignment':'right', 'length':4, 'type':'string', 'start_pos':137, 'end_pos':140, 'required':False},
  'TRF_PIVA_ESTERO': { 'padding':' ', 'alignment':'left', 'length':12, 'type':'string', 'start_pos':141, 'end_pos':152, 'required':False},
  'TRF_COFI_ESTERO': { 'padding':' ', 'alignment':'left', 'length':20, 'type':'string', 'start_pos':153, 'end_pos':172, 'required':False},
  'TRF_SESSO': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':173, 'end_pos':173, 'required':False},
  'TRF_DTNAS': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':174, 'end_pos':181, 'required':False},
  'TRF_COMNA': { 'padding':' ', 'alignment':'left', 'length':25, 'type':'string', 'start_pos':182, 'end_pos':206, 'required':False},
  'TRF_PRVNA': { 'padding':' ', 'alignment':'left', 'length':2, 'type':'string', 'start_pos':207, 'end_pos':208, 'required':False},
  'TRF_PREF': { 'padding':' ', 'alignment':'left', 'length':4, 'type':'string', 'start_pos':209, 'end_pos':212, 'required':False},
  'TRF_NTELE_NUM': { 'padding':' ', 'alignment':'left', 'length':20, 'type':'string', 'start_pos':213, 'end_pos':232, 'required':False},
  'TRF_FAX_PREF': { 'padding':' ', 'alignment':'left', 'length':4, 'type':'string', 'start_pos':233, 'end_pos':236, 'required':False},
  'TRF_FAX_NUM': { 'padding':' ', 'alignment':'left', 'length':9, 'type':'string', 'start_pos':237, 'end_pos':245, 'required':False},
  'TRF_CFCONTO': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':246, 'end_pos':252, 'required':False},
  'TRF_CFCODPAG': { 'padding':' ', 'alignment':'right', 'length':4, 'type':'string', 'start_pos':253, 'end_pos':256, 'required':False},
  'TRF_CFBANCA': { 'padding':' ', 'alignment':'right', 'length':5, 'type':'string', 'start_pos':257, 'end_pos':261, 'required':False},
  'TRF_CFAGENZIA': { 'padding':' ', 'alignment':'right', 'length':5, 'type':'string', 'start_pos':262, 'end_pos':266, 'required':False},
  'TRF_CFINTERM': { 'padding':' ', 'alignment':'right', 'length':1, 'type':'string', 'start_pos':267, 'end_pos':267, 'required':False},
  'TRF_CAUSALE': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':268, 'end_pos':270, 'required':False},
  'TRF_CAU_DES': { 'padding':' ', 'alignment':'left', 'length':15, 'type':'string', 'start_pos':271, 'end_pos':285, 'required':False},
  'TRF_CAU_AGG': { 'padding':' ', 'alignment':'left', 'length':18, 'type':'string', 'start_pos':286, 'end_pos':303, 'required':False},
  'TRF_CAU_AGG_1': { 'padding':' ', 'alignment':'left', 'length':34, 'type':'string', 'start_pos':304, 'end_pos':337, 'required':False},
  'TRF_CAU_AGG_2': { 'padding':' ', 'alignment':'left', 'length':34, 'type':'string', 'start_pos':338, 'end_pos':371, 'required':False},
  'TRF_DATA_REGISTRAZIONE': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':372, 'end_pos':379, 'required':False},
  'TRF_DATA_DOC': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':380, 'end_pos':387, 'required':False},
  'TRF_NUM_DOC_FOR': { 'padding':'0', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':388, 'end_pos':395, 'required':False},
  'TRF_NDOC': { 'padding':'0', 'alignment':'right', 'length':5, 'type':'string', 'start_pos':396, 'end_pos':400, 'required':False},
  'TRF_SERIE': { 'padding':'0', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':401, 'end_pos':402, 'required':False},
  'TRF_EC_PARTITA': { 'padding':'0', 'alignment':'right', 'length':6, 'type':'string', 'start_pos':403, 'end_pos':408, 'required':False},
  'TRF_EC_PARTITA_ANNO': { 'padding':' ', 'alignment':'right', 'length':4, 'type':'string', 'start_pos':409, 'end_pos':412, 'required':False},
  'TRF_EC_COD_VAL': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':413, 'end_pos':415, 'required':False},
  'TRF_EC_CAMBIO': { 'padding':' ', 'alignment':'right', 'length':13, 'type':'string', 'start_pos':416, 'end_pos':428, 'required':False},
  'TRF_EC_DATA_CAMBIO': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':429, 'end_pos':436, 'required':False},
  'TRF_EC_TOT_DOC_VAL': { 'padding':' ', 'alignment':'right', 'length':16, 'type':'string', 'start_pos':437, 'end_pos':452, 'required':False},
  'TRF_EC_TOT_IVA_VAL': { 'padding':' ', 'alignment':'right', 'length':16, 'type':'string', 'start_pos':453, 'end_pos':468, 'required':False},
  'TRF_PLAFOND': { 'padding':' ', 'alignment':'right', 'length':6, 'type':'string', 'start_pos':469, 'end_pos':474, 'required':False},
  'TRF_IMPONIB': { 'padding':'0', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':475, 'end_pos':486, 'required':False},
  'TRF_ALIQ': { 'padding':'0', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':487, 'end_pos':489, 'required':False},
  'TRF_ALIQ_AGRICOLA': { 'padding':'0', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':490, 'end_pos':492, 'required':False},
  'TRF_IVA11': { 'padding':'0', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':493, 'end_pos':494, 'required':False},
  'TRF_IMPOSTA': { 'padding':'0', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':495, 'end_pos':505, 'required':False},
  'TRF_IMPONIB2': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':506, 'end_pos':517, 'required':False},
  'TRF_ALIQ2': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':518, 'end_pos':520, 'required':False},
  'TRF_ALIQ_AGRICOLA2': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':521, 'end_pos':523, 'required':False},
  'TRF_IVA112': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':524, 'end_pos':525, 'required':False},
  'TRF_IMPOSTA2': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':526, 'end_pos':536, 'required':False},
  'TRF_IMPONIB3': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':537, 'end_pos':548, 'required':False},
  'TRF_ALIQ3': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':549, 'end_pos':551, 'required':False},
  'TRF_ALIQ_AGRICOLA3': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':552, 'end_pos':554, 'required':False},
  'TRF_IVA113': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':555, 'end_pos':556, 'required':False},
  'TRF_IMPOSTA3': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':557, 'end_pos':567, 'required':False},
  'TRF_IMPONIB4': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':568, 'end_pos':579, 'required':False},
  'TRF_ALIQ24': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':580, 'end_pos':582, 'required':False},
  'TRF_ALIQ_AGRICOLA4': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':583, 'end_pos':585, 'required':False},
  'TRF_IVA114': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':586, 'end_pos':587, 'required':False},
  'TRF_IMPOSTA4': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':588, 'end_pos':598, 'required':False},
  'TRF_IMPONIB5': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':599, 'end_pos':610, 'required':False},
  'TRF_ALIQ5': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':611, 'end_pos':613, 'required':False},
  'TRF_ALIQ_AGRICOLA5': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':614, 'end_pos':616, 'required':False},
  'TRF_IVA115': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':617, 'end_pos':618, 'required':False},
  'TRF_IMPOSTA5': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':619, 'end_pos':629, 'required':False},
  'TRF_IMPONIB6': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':630, 'end_pos':641, 'required':False},
  'TRF_ALIQ6': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':642, 'end_pos':644, 'required':False},
  'TRF_ALIQ_AGRICOLA6': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':645, 'end_pos':647, 'required':False},
  'TRF_IVA116': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':648, 'end_pos':649, 'required':False},
  'TRF_IMPOSTA6': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':650, 'end_pos':660, 'required':False},
  'TRF_IMPONIB7': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':661, 'end_pos':672, 'required':False},
  'TRF_ALIQ7': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':673, 'end_pos':675, 'required':False},
  'TRF_ALIQ_AGRICOLA7': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':676, 'end_pos':678, 'required':False},
  'TRF_IVA117': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':679, 'end_pos':680, 'required':False},
  'TRF_IMPOSTA7': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':681, 'end_pos':691, 'required':False},
  'TRF_IMPONIB8': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':692, 'end_pos':703, 'required':False},
  'TRF_ALIQ8': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':704, 'end_pos':706, 'required':False},
  'TRF_ALIQ_AGRICOLA8': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':707, 'end_pos':709, 'required':False},
  'TRF_IVA118': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':710, 'end_pos':711, 'required':False},
  'TRF_IMPOSTA8': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':712, 'end_pos':722, 'required':False},
  'TRF_TOT_FATT': { 'padding':'0', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':723, 'end_pos':734, 'required':False},
  'TRF_CONTO_RIC': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':735, 'end_pos':741, 'required':False},
  'TRF_IMP_RIC': { 'padding':'0', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':742, 'end_pos':753, 'required':False},
  'EMPTY1': { 'padding':' ', 'alignment':'right', 'length':133, 'type':'string', 'start_pos':754, 'end_pos':886, 'required':False},
  'TRF_CAU_PAGAM': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':887, 'end_pos':889, 'required':False},
  'TRF_CAU_DES_PAGAM': { 'padding':' ', 'alignment':'left', 'length':15, 'type':'string', 'start_pos':890, 'end_pos':904, 'required':False},
  'TRF_CAU_AGG_1_PAGAM': { 'padding':' ', 'alignment':'left', 'length':34, 'type':'string', 'start_pos':905, 'end_pos':938, 'required':False},
  'TRF_CAU_AGG_2_PAGAM': { 'padding':' ', 'alignment':'left', 'length':34, 'type':'string', 'start_pos':939, 'end_pos':972, 'required':False},
  'TRF_CONTO': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':973, 'end_pos':979, 'required':False},
  'TRF_DA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':980, 'end_pos':980, 'required':False},
  'TRF_IMPORTO': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':981, 'end_pos':992, 'required':False},
  'TRF_CAU_AGGIUNT': { 'padding':' ', 'alignment':'left', 'length':18, 'type':'string', 'start_pos':993, 'end_pos':1010, 'required':False},
  'TRF_EC_PARTITA_PAG': { 'padding':' ', 'alignment':'right', 'length':6, 'type':'string', 'start_pos':1011, 'end_pos':1016, 'required':False},
  'TRF_EC_PARTITA_ANNO_PAG': { 'padding':' ', 'alignment':'right', 'length':4, 'type':'string', 'start_pos':1017, 'end_pos':1020, 'required':False},
  'TRF_EC_IMP_VAL': { 'padding':' ', 'alignment':'right', 'length':16, 'type':'string', 'start_pos':1021, 'end_pos':1036, 'required':False},
  'EMPTY2': { 'padding':' ', 'alignment':'left', 'length':5056, 'type':'string', 'start_pos':1037, 'end_pos':6092, 'required':False},
  'TRF_RIFER_TAB': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6093, 'end_pos':6093, 'required':False},
  'TRF_IND_RIGA': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':6094, 'end_pos':6095, 'required':False},
  'TRF_DT_INI': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6096, 'end_pos':6103, 'required':False},
  'TRF_DT_FIN': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6104, 'end_pos':6111, 'required':False},
  'EMPTY3': { 'padding':' ', 'alignment':'right', 'length':171, 'type':'string', 'start_pos':6112, 'end_pos':6282, 'required':False},
  'TRF_DOC6': { 'padding':' ', 'alignment':'right', 'length':6, 'type':'string', 'start_pos':6283, 'end_pos':6288, 'required':False},
  'TRF_AN_OMONIMI': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6289, 'end_pos':6289, 'required':False},
  'TRF_AN_TIPO_SOGG': { 'padding':'0', 'alignment':'right', 'length':1, 'type':'string', 'start_pos':6290, 'end_pos':6290, 'required':False},
  'TRF_EC_PARTITA_SEZ_PAG': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':6291, 'end_pos':6292, 'required':False},
  'EMPTY4': { 'padding':' ', 'alignment':'right', 'length':158, 'type':'string', 'start_pos':6293, 'end_pos':6450, 'required':False},
  'TRF_NUM_DOC_PAG_PROF': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6451, 'end_pos':6457, 'required':False},
  'TRF_DATA_DOC_PAG_PROF': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6458, 'end_pos':6465, 'required':False},
  'TRF_RIT_ACC': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':6466, 'end_pos':6477, 'required':False},
  'TRF_RIT_PREV': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':6478, 'end_pos':6489, 'required':False},
  'TRF_RIT_1': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':6490, 'end_pos':6501, 'required':False},
  'TRF_RIT_2': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':6502, 'end_pos':6513, 'required':False},
  'TRF_RIT_3': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':6514, 'end_pos':6525, 'required':False},
  'TRF_RIT_4': { 'padding':' ', 'alignment':'right', 'length':12, 'type':'string', 'start_pos':6526, 'end_pos':6537, 'required':False},
  'TRF_UNITA_RICAVI': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':6538, 'end_pos':6539, 'required':False},
  'EMPTY5': { 'padding':' ', 'alignment':'right', 'length':14, 'type':'string', 'start_pos':6540, 'end_pos':6553, 'required':False},
  'TRF_UNITA_PAGAM': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':6554, 'end_pos':6555, 'required':False},
  'EMPTY6': { 'padding':' ', 'alignment':'left', 'length':158, 'type':'string', 'start_pos':6556, 'end_pos':6713, 'required':False},
  'TRF_FAX_PREF_1': { 'padding':' ', 'alignment':'left', 'length':4, 'type':'string', 'start_pos':6714, 'end_pos':6717, 'required':False},
  'TRF_FAX_NUM_1': { 'padding':' ', 'alignment':'left', 'length':20, 'type':'string', 'start_pos':6718, 'end_pos':6737, 'required':False},
  'TRF_SOLO_CLIFOR': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6738, 'end_pos':6738, 'required':False},
  'TRF_80_SEGUENTE': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6739, 'end_pos':6739, 'required':False},
  'TRF_CONTO_RIT_ACC': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6740, 'end_pos':6746, 'required':False},
  'TRF_CONTO_RIT_PREV': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6747, 'end_pos':6753, 'required':False},
  'TRF_CONTO_RIT_1': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6754, 'end_pos':6760, 'required':False},
  'TRF_CONTO_RIT_2': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6761, 'end_pos':6767, 'required':False},
  'TRF_CONTO_RIT_3': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6768, 'end_pos':6774, 'required':False},
  'TRF_CONTO_RIT_4': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6775, 'end_pos':6781, 'required':False},
  'TRF_DIFFERIMENTO_IVA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6782, 'end_pos':6782, 'required':False},
  'TRF_STORICO': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6783, 'end_pos':6783, 'required':False},
  'TRF_STORICO_DATA': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6784, 'end_pos':6791, 'required':False},
  'TRF_CAUS_ORI': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':6792, 'end_pos':6794, 'required':False},
  'TRF_PREV_TIPOMOV': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6795, 'end_pos':6795, 'required':False},
  'TRF_PREV_RATRIS': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6796, 'end_pos':6796, 'required':False},
  'TRF_PREV_DTCOMP_INI': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6797, 'end_pos':6804, 'required':False},
  'TRF_PREV_DTCOMP_FIN': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6805, 'end_pos':6812, 'required':False},
  'TRF_PREV_FLAG_CONT': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6813, 'end_pos':6813, 'required':False},
  'TRF_RIFERIMENTO': { 'padding':' ', 'alignment':'left', 'length':20, 'type':'string', 'start_pos':6814, 'end_pos':6833, 'required':False},
  'TRF_CAUS_PREST_ANA': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':6834, 'end_pos':6835, 'required':False},
  'TRF_EC_TIPO_PAGA': { 'padding':' ', 'alignment':'right', 'length':1, 'type':'string', 'start_pos':6836, 'end_pos':6836, 'required':False},
  'TRF_CONTO_IVA_VEN_ACQ': { 'padding':' ', 'alignment':'right', 'length':7, 'type':'string', 'start_pos':6837, 'end_pos':6843, 'required':False},
  'TRF_PIVA_VECCHIA': { 'padding':' ', 'alignment':'right', 'length':11, 'type':'string', 'start_pos':6844, 'end_pos':6854, 'required':False},
  'TRF_PIVA_ESTERO_VECCHIA': { 'padding':' ', 'alignment':'left', 'length':12, 'type':'string', 'start_pos':6855, 'end_pos':6866, 'required':False},
  'TRF_RISERVATO': { 'padding':' ', 'alignment':'left', 'length':32, 'type':'string', 'start_pos':6867, 'end_pos':6898, 'required':False},
  'TRF_DATA_IVA_AGVIAGGI': { 'padding':' ', 'alignment':'right', 'length':8, 'type':'string', 'start_pos':6899, 'end_pos':6906, 'required':False},
  'TRF_DATI_AGG_ANA_REC4': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6907, 'end_pos':6907, 'required':False},
  'TRF_RIF_IVA_NOTE_CRED': { 'padding':' ', 'alignment':'right', 'length':6, 'type':'string', 'start_pos':6908, 'end_pos':6913, 'required':False},
  'TRF_RIF_IVA_ANNO_PREC': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6914, 'end_pos':6914, 'required':False},
  'TRF_NATURA_GIURIDICA': { 'padding':' ', 'alignment':'right', 'length':2, 'type':'string', 'start_pos':6915, 'end_pos':6916, 'required':False},
  'TRF_STAMPA_ELENCO': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6917, 'end_pos':6917, 'required':False},
  'TRF_PERC_FORF': { 'padding':' ', 'alignment':'right', 'length':3, 'type':'string', 'start_pos':6918, 'end_pos':6920, 'required':False},
  'EMPTY7': { 'padding':' ', 'alignment':'left', 'length':21, 'type':'string', 'start_pos':6921, 'end_pos':6941, 'required':False},
  'TRF_SOLO_MOV_IVA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6942, 'end_pos':6942, 'required':False},
  'TRF_COFI_VECCHIO': { 'padding':' ', 'alignment':'left', 'length':16, 'type':'string', 'start_pos':6943, 'end_pos':6958, 'required':False},
  'TRF_USA_PIVA_VECCHIA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6959, 'end_pos':6959, 'required':False},
  'TRF_USA_PIVA_EST_VECCHIA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6960, 'end_pos':6960, 'required':False},
  'TRF_USA_COFI_VECCHIO': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6961, 'end_pos':6961, 'required':False},
  'TRF_ESIGIBILITA_IVA': { 'padding':' ', 'alignment':'right', 'length':1, 'type':'string', 'start_pos':6962, 'end_pos':6962, 'required':False},
  'TRF_TIPO_MOV_RISCONTI': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6963, 'end_pos':6963, 'required':False},
  'TRF_AGGIORNA_EC': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6964, 'end_pos':6964, 'required':False},
  'TRF_BLACKLIST_ANAG': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6965, 'end_pos':6965, 'required':False},
  'TRF_BLACKLIST_IVA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6966, 'end_pos':6966, 'required':False},
  'TRF_BLACKLIST_IVA_ANA': { 'padding':' ', 'alignment':'right', 'length':6, 'type':'string', 'start_pos':6967, 'end_pos':6972, 'required':False},
  'TRF_CONTEA_ESTERO': { 'padding':' ', 'alignment':'left', 'length':20, 'type':'string', 'start_pos':6973, 'end_pos':6992, 'required':False},
  'TRF_ART21_ANAG': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6993, 'end_pos':6993, 'required':False},
  'TRF_ART21_IVA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6994, 'end_pos':6994, 'required':False},
  'TRF_RIF_FATTURA': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6995, 'end_pos':6995, 'required':False},
  'TRF_RISERVATO_B': { 'padding':' ', 'alignment':'left', 'length':1, 'type':'string', 'start_pos':6996, 'end_pos':6996, 'required':False},
  'FILLER1': { 'padding':' ', 'alignment':'left', 'length':3, 'type':'string', 'start_pos':6997, 'end_pos':6999, 'required':False},
  'FILLER2': { 'padding':' ', 'alignment':'left', 'length':2, 'type':'string', 'start_pos':7000, 'end_pos':7001, 'required':False}
}


def totxt(value, maxlen=None, ttype=None):
    maxlen = maxlen or 999
    if ttype == 'VAT':
        if value and value[0:2].upper() == 'IT':
            text = unidecode(unicode(value))[2:]
        else:
            text = ''
    elif ttype == 'PHONE':
        if value:
            value = unidecode(unicode(value.replace('+', '00')))
            text = ''
            for x in value:
                if x.isdigit():
                    text += x
            text = text[- maxlen:]
        else:
            text = ''
    elif ttype == 'DATE':
        if value:
            text = fields.Date.from_string(value).strftime('%d%m%Y')
        else:
            text = '00000000'
    elif ttype == 'NUMB':
        if value:
            text = ''
            for x in value:
                if x.isdigit():
                    text += x
            text = unidecode(unicode(text))[- maxlen:]
        else:
            text = ''
    elif ttype and ttype[0:5] == 'FLOAT':
        if value < 0:
            fmt = '%%20.%sf-' % ttype[5]
            text = fmt % abs(value)
        else:
            fmt = '%%20.%sf' % ttype[5]
            text = fmt % value
        x = text.find('.')
        if x >=0:
            text = text[0:x] + text[x + 1:]
        text = text[- maxlen:]
    elif isinstance(value, basestring):
        text = unidecode(unicode(value))[0:maxlen]
    elif isinstance(value, (int, long, float)):
        text = str(value)[- maxlen:]
    elif value:
        text = str(value)
    else:
        text = ''
    return text


def imppn_line(**kwargs):
    '''
    Get any list of arguments and transform them in the IMPPN v. 2013 notation
    '''
    dict = {}
    for arg in kwargs:
        if arg in IMPPN_CONFIG:
            maxlen = IMPPN_CONFIG[arg]['length']
        else:
            maxlen = False
        if arg in TRX_TTYPE:
            dict[arg] = totxt(kwargs[arg], maxlen=maxlen, ttype=TRX_TTYPE[arg])
        else:
            dict[arg] = totxt(kwargs[arg], maxlen=maxlen)
    imppn_obj = FixedWidth(IMPPN_CONFIG)
    imppn_obj.update(**dict)
    return imppn_obj.line

if __name__ == '__main__':
    print 'Quick test\n', imppn_line(TRF_DITTA='7')
