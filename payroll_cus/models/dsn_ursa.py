from dataclasses import field
from email.policy import default
from odoo import fields, api, models, tools, _
from datetime import date
import datetime
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from calendar import monthrange
from operator import itemgetter
from odoo.tools.safe_eval import safe_eval

class dsn_ursa(models.Model):
    _name = 'dsn.ursa'
    _description = 'DSN URSAF'
    _inherit = ['portal.mixin', 'mail.thread']
    _order = "id desc, create_date desc"
    _rec_name = "employee"

    @api.depends('payslip')
    def _default_get1(self):
        for list in self:
            list.siret = list.payslip.company_id.siret
            list.employee = list.payslip.employee_id
            list.adress = list.payslip.company_id.street
            list.regime = list.liste.regime


    payslip = fields.Many2one('hr.payslip', string = 'payslip' , tracking=True, ondelete="cascade")
    liste = fields.Many2one('dsn.liste', string = 'Dossier' , tracking=True, ondelete="cascade")
    
    type_decla = fields.Char(string ='Type de la déclaration', tracking=True, default='Initiale')
    number = fields.Char(string ="N° d'ordre de la déclaration", tracking=True)


    numero = fields.Char(string ="Numéro cotisant", tracking=True, default='117000001567462542')

    rais = fields.Char(string ='Raison Sociale', tracking=True)
    # rais = fields.Char(related = 'employee.company_id.name',string ='Raison Sociale', tracking=True)
    siret = fields.Char(related = 'payslip.company_id.siret', string ='N SIRET', tracking=True)
    # siret_dest = fields.Char(string ='Destinatteur N SIRET', tracking=True)
    employee = fields.Many2one(related = 'payslip.employee_id', string ='employee', tracking=True)
    regime = fields.Char(related = 'liste.regime', string ='Regime', tracking=True)
    adress = fields.Char(related = 'payslip.company_id.street', string ='Adresse', tracking=True)
    ape = fields.Char(related = 'payslip.company_id.ape', string ='Adresse', tracking=True)
    date = fields.Date(string ='Date', tracking=True)
    type_decla = fields.Char(string ='Type de la déclaration', tracking=True, default='Initiale')

    # ursaf
    desti = fields.Many2one('res.partner', string ='Destinataire', tracking=True, compute='_default_dest')
    siret_dest = fields.Char(related = 'desti.siret', string ='Destinatteur N SIRET', tracking=True)
    
    #humanis
    desti_hum = fields.Many2one('res.partner', string ='Destinataire', tracking=True, compute='_default_huma')
    siret_hum = fields.Char(related = 'desti_hum.siret', string ='Humanis N SIRET', tracking=True)
    
    #AG2R
    desti_ag2r = fields.Many2one('res.partner', string ='Destinataire', tracking=True, compute='_default_ag2r')
    siret_ag2r = fields.Char(related = 'desti_ag2r.siret', string ='AG@R N SIRET', tracking=True)
    total_ag2r = fields.Monetary(string='Total des cotisations', store =True, default=0, currency_field='company_currency_id')

    period = fields.Char(string ='Period', tracking=True, compute='_default_get')
    
    gross = fields.Monetary(string='Gross', store =True, currency_field='company_currency_id')
    c027 = fields.Monetary(string='027 - CONTRIBUTION AU DIALOGUE SOCIAL', store =True, compute='_ursaf', currency_field='company_currency_id')
    c322 = fields.Monetary(string='332 - FNAL CAS GENERAL < 20 SALARIES', store =True, compute='_ursaf', currency_field='company_currency_id')
    c423 = fields.Monetary(string='423 - CONTRIBUTION CHOMAGE APPRENTIS LOI 87 ', store =True, compute='_ursaf', currency_field='company_currency_id')
    c668 = fields.Monetary(string='668 - REDUCTION GENERALE', store =True, currency_field='company_currency_id')
    c726 = fields.Monetary(string='726 - APPRENTIS SECT PRIVE INF SEUIL', store =True, compute='_ursaf', currency_field='company_currency_id')
    c727 = fields.Monetary(string='726 - APPRENTIS SECT PRIVE INF SEUIL', store =True, compute='_ursaf', currency_field='company_currency_id')
    c937 = fields.Monetary(string='937 - COTISATION AGS CAS GENERAL', store =True, compute='_ursaf', currency_field='company_currency_id')
    total_c1 = fields.Monetary(string='Total des cotisations', store =True, compute='_ursaf', currency_field='company_currency_id')
    
    t027 = fields.Float(string='t027', default='0.016')
    t322 = fields.Float(string='t322', default='0.10')
    t423 = fields.Float(string='t423', default='4.05')
    t668 = fields.Float(string='t668', default='1')
    t726 = fields.Float(string='t726', default='12.65')
    t726_1 = fields.Float(string='t726', default='0.9')
    t727 = fields.Float(string='t727', default='8.55')
    t937 = fields.Float(string='t937', default='0.15')
    
    ceg_s = fields.Monetary(string='CEG_NC01.ISA CONTRIB. EQUILIBRE GENERAL NON CADRE T1 ', store =True, compute='_default_get', currency_field='company_currency_id')
    ceg_p = fields.Monetary(string='CEG_NC01.ISA CONTRIB. EQUILIBRE GENERAL NON CADRE T1 ', store =True, compute='_default_get', currency_field='company_currency_id')
    fil_s = fields.Monetary(string='FILLON25.ISA REDUCTION DE CHARGES RETRAITE NON CADRE ', store =True, compute='_default_get', currency_field='company_currency_id')
    fil_p = fields.Monetary(string='FILLON25.ISA REDUCTION DE CHARGES RETRAITE NON CADRE ', store =True, compute='_default_get', currency_field='company_currency_id')
    ret_s = fields.Monetary(string='RETRAITE01.ISA RETRAITE TA/T1  ', store =True, compute='_default_get', currency_field='company_currency_id')
    ret_p = fields.Monetary(string='RETRAITE01.ISA RETRAITE TA/T1  ', store =True, compute='_default_get', currency_field='company_currency_id')
    mot_1 = fields.Monetary(string='Montant', store =True, compute='_huma1', currency_field='company_currency_id')
    mot_2 = fields.Monetary(string='Montant', store =True, compute='_huma1', currency_field='company_currency_id')
    mot_3 = fields.Monetary(string='Montant', store =True, compute='_huma1', currency_field='company_currency_id')
    total_huma = fields.Monetary(string='TOTAL À PAYER', store =True, compute='_huma1', currency_field='company_currency_id')


    company_id = fields.Many2one(related='employee.company_id', store=True, readonly=True)
    company_currency_id = fields.Many2one(related='company_id.currency_id', string='Company Currency',
        readonly=True, store=True,
        help='Utility field to express amount currency')

    def _huma1(self):
        for huma in self:
            huma.mot_1 = huma.ceg_s + huma.ceg_p
            huma.mot_2 = huma.fil_s + huma.fil_p
            huma.mot_3 = huma.ret_s + huma.ret_p
            huma.total_huma = huma.mot_1 + huma.mot_2 + huma.mot_3

    @api.depends('gross')
    def _ursaf(self):
        for usr in self:
            usr.c027 = round((usr.gross * usr.t027)/100)
            usr.c322 = round((usr.gross * usr.t322)/100)
            usr.c423 = round((usr.gross * usr.t423)/100)
            usr.c668 = self.env['hr.payslip.line'].search([('slip_id','=',usr.payslip.id),('code','=','ECC')],limit=1).total
            usr.c726 = round((usr.gross * (usr.t027 + usr.t726_1))/100)
            usr.c727 = round((usr.gross * usr.t727)/100)
            usr.c937 = round((usr.gross * usr.t937)/100)
            usr.total_c1 = usr.c027 + usr.c322 + usr.c423 + usr.c668 + usr.c726 + usr.c727 + usr.c937

    @api.depends('payslip')
    def _default_get(self):
        for list in self:
            list.rais = str(list.payslip.company_id.name) + '('+ str(list.liste.code) + ')'
            list.period = str(list.payslip.date_from) + ' au ' + str(list.payslip.date_to)
            list.date = datetime.datetime.now().date()
            list.gross = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.ceg_s = 0
            list.ceg_p = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.fil_s = 0
            list.fil_p = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.ret_s = 0
            list.ret_p = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total

    def _default_dest(self):
        for usrsa1 in self:
            nom = "RSSAF D'ILE DE FRANCE"
            dest = self.env['res.partner'].search([('name','=',nom)],limit=1)
            if len(dest) == 1:
                usrsa1.desti = dest.id
                usrsa1.siret_dest = dest.siret
            else:
                dest  = self.env['res.partner'].create([
                    {
                        'name' : "RSSAF D'ILE DE FRANCE",
                        'customer_rank' : 0, 
                        'supplier_rank': 1,
                        'siret':'8861779300013'
                    }
                    ])
                usrsa1.desti = dest.id

    def _default_huma(self):
        for huma in self:
            nom = "HUMANIS Retraite"
            dest = self.env['res.partner'].search([('name','=',nom)],limit=1)
            if len(dest) == 1:
                huma.desti_hum = dest.id
            else:
                dest  = self.env['res.partner'].create([
                    {
                        'name' : nom,
                        'customer_rank' : 0, 
                        'supplier_rank': 1,
                        'siret':'75320126800012'
                    }
                    ])
                huma.desti_hum = dest.id

    def _default_ag2r(self):
        for ag2r in self:
            nom = " AG2R PREVOYANCE"
            dest = self.env['res.partner'].search([('name','=',nom)],limit=1)
            if len(dest) == 1:
                ag2r.desti_ag2r = dest.id
            else:
                dest  = self.env['res.partner'].create([
                    {
                        'name' : nom,
                        'customer_rank' : 0, 
                        'supplier_rank': 1,
                        'siret':'33323227000012'
                    }
                    ])
                ag2r.desti_ag2r = dest.id
