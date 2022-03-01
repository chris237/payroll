# -*- coding: utf-8 -*-

from odoo import api, fields, models,_, _lt
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang
from dateutil.relativedelta import relativedelta
import datetime
import time
import calendar
from datetime import date
import json
import requests
import itertools
from operator import itemgetter
from itertools import groupby
from json import dumps
from itertools import zip_longest
from hashlib import sha256  
from datetime import date
from datetime import timedelta

from collections import defaultdict
import re
import logging
_logger = logging.getLogger(__name__)


class Hrpaie(models.Model):
    _name = 'hr.paie'
    _inherit = ['portal.mixin', 'mail.thread']
    _description = "paie"
    _order = "id desc, date desc"
    _rec_name ='employe_id'

    def _get_default_date(self):
        return fields.Date.from_string(fields.Date.today())
        
    liste = fields.Many2one('dsn.liste', string = 'Dossier' , tracking=True, ondelete="cascade")
    payslip = fields.Many2one(related = 'liste.payslip', string = 'payslip' , tracking=True, ondelete="cascade")
    
    

    date = fields.Date(readonly=True , index=True, tracking=True, required=True, string='Date', states={'draft': [('readonly', False)]}, default=_get_default_date)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
    ], string='Status', default='draft', index=True, tracking=True, readonly=True)
    siret = fields.Char(related = 'payslip.company_id.siret', string='Siret')
    adresse = fields.Char(related = 'payslip.company_id.street', string='Adresse')
    regime_declaration = fields.Char(related = 'liste.regime', string='Regime Declaration')
    type_declaration = fields.Char(string='Type Declaration', default='Initiale')
    ordre_declaration = fields.Char(string='Ordre Declaration')
    code_ape = fields.Char(related = 'payslip.company_id.ape', string='Code APE')
    employe_id = fields.Many2one(related = 'payslip.employee_id', string='Nom',required=True)
    matricule = fields.Char(related = 'employe_id.registration_number', string='Matricule')
    insee = fields.Char(string='Insee')
    nom_usage = fields.Char(string='Nom usage')
    date_from = fields.Date(string='From', related = 'payslip.date_from')
    date_to = fields.Date(string='To', related = 'payslip.date_to')

    mt_assiette_bp = fields.Float(string='Montant Assiette Brut Plafonée', compute ='_default_get') 
    mt_assiette_bd = fields.Float(string='Montant Assiette Brut Déplafonée', compute = '_default_get')   
    mt_assiette_cac = fields.Float(string='Montant Assiette des Contributions Assurance Chômage', compute ='_default_get')
    mt_base_bf = fields.Float(string='Montant Base brute fiscale', compute = '_default_get')

    mt_smic = fields.Float(string='Montant SMIC retenue pour le calcul des reductions', compute = '_default_mt')
    mt_contribution_patronale = fields.Float(string='Montant contribution patronale', compute = '_default_mt')
    mt_plafond_sec = fields.Float(string='Montant plafond de sécurité sociale', compute = '_default_mt')

    @api.depends('payslip')
    def _default_mt(self):
        for list in self:
            list.mt_smic = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.mt_contribution_patronale = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','TCE')],limit=1).total
            list.mt_plafond_sec = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            
    # Montant
    mt_cotis_all_log = fields.Float(string='Montant cotisation allocation de logement', compute= '_default_mtt')
    mt_cotis_ass_vieil = fields.Float(string='Montant cotisation assurance vieillesse', compute= '_default_mtt')
    mt_exon_cotis_emp = fields.Float(string='Montant exonération de cotisations au titre de lemploi', compute= '_default_mtt')
    mt_red_gen_cotis_ss = fields.Float(string='Montant reduction general des cotisations sécurité sociale', compute= '_default_mtt')
    mt_cotis_acc_travail = fields.Float(string='Montant Cotisation accident de travail', compute= '_default_mtt')
    mt_contrib_sol_aut = fields.Float(string='Montant Contribution solidarité autonome', compute= '_default_mtt')
    mt_cotis_all_fam = fields.Float(string='Montant cotisation allocation familiale', compute= '_default_mtt')
    mt_cotis_ass_mal = fields.Float(string='Montant cotisation assurance maladie', compute= '_default_mtt')
    mt_cotis_ass_vieil1 = fields.Float(string='Montant cotisation assurance maladie', compute= '_default_mtt')
    mt_contrib_financ_ds = fields.Float(string='Montant contribution au financement du dialogue social', compute= '_default_mtt')
    mt_cotis_reg_unif = fields.Float(string='Montant cotisation regime unifié agirc-arrco', compute= '_default_mtt')
    mt_red_gen_cotis_pat = fields.Float(string='Montant reduction generale des cotisations patronales', compute= '_default_mtt')
    mt_exo_cotis_sal = fields.Float(string='Montant exo cotisation salariale', compute= '_default_mtt')
    mt_cotis_ac = fields.Float(string='Montant cotisation AC', compute= '_default_mtt')
    mt_cotis_ags = fields.Float(string='Montant cotisation AGS', compute= '_default_mtt')

    def _default_mtt(self):
        for list in self:
            list.mt_cotis_all_log = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_ass_vieil = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_exon_cotis_emp = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_red_gen_cotis_ss = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_acc_travail = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_contrib_sol_aut = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_all_fam = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_ass_mal = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_ass_vieil1 = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_contrib_financ_ds = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_reg_unif = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_red_gen_cotis_pat = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_exo_cotis_sal = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_ac = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            list.mt_cotis_ags = (list.g_cotis_all_log * list.t_cotis_all_log) / 100
            

    # Gross
    g_cotis_all_log = fields.Float(string='Gross cotisation allocation de logement', compute = '_defaut_m')
    g_cotis_ass_vieil = fields.Float(string='Gross cotisation assurance vieillesse', compute = '_defaut_m')
    g_exon_cotis_emp = fields.Float(string='Gross exonération de cotisations au titre de lemploi', compute = '_defaut_m')
    g_red_gen_cotis_ss = fields.Float(string='Gross reduction general des cotisations sécurité sociale', compute = '_defaut_m')
    g_cotis_acc_travail = fields.Float(string='Gross Cotisation accident de travail', compute = '_defaut_m')
    g_contrib_sol_aut = fields.Float(string='Gross Contribution solidarité autonome', compute = '_defaut_m')
    g_cotis_all_fam = fields.Float(string='Gross cotisation allocation familiale', compute = '_defaut_m')
    g_cotis_ass_mal = fields.Float(string='Gross cotisation assurance maladie', compute = '_defaut_m')
    g_contrib_financ_ds = fields.Float(string='Gross contribution au financement du dialogue social', compute = '_defaut_m')
    g_cotis_reg_unif = fields.Float(string='Gross cotisation regime unifié agirc-arrco', compute = '_defaut_m')
    g_red_gen_cotis_pat = fields.Float(string='Gross reduction generale des cotisations patronales', compute = '_defaut_m')
    g_exo_cotis_sal = fields.Float(string='Gross exo cotisation salariale', compute = '_defaut_m')
    g_cotis_ac = fields.Float(string='Gross cotisation AC', compute = '_defaut_m')
    g_cotis_ags = fields.Float(string='Gross cotisation AGS', compute = '_defaut_m')

    @api.depends('payslip')
    def _defaut_m(self):
        for list in self:
            list.g_cotis_all_log = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_ass_vieil = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_exon_cotis_emp = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_red_gen_cotis_ss = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_acc_travail = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_contrib_sol_aut = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_all_fam = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_ass_mal = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_contrib_financ_ds = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_reg_unif = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_red_gen_cotis_pat = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_exo_cotis_sal = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_ac = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.g_cotis_ags = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            

    # Taux
    t_cotis_all_log = fields.Float(string='Taux cotisation allocation de logement', default=0.1)
    t_cotis_ass_vieil = fields.Float(string='Taux cotisation assurance vieillesse', default = 8.55)
    t_exon_cotis_emp = fields.Float(string='Taux exonération de cotisations au titre de lemploi', default = 0)
    t_red_gen_cotis_ss = fields.Float(string='Taux reduction general des cotisations sécurité sociale', default= 1)
    t_cotis_acc_travail = fields.Float(string='Taux Cotisation accident de travail', default= 0.9)
    t_contrib_sol_aut = fields.Float(string='Taux Contribution solidarité autonome', default=0.3)
    t_cotis_all_fam = fields.Float(string='Taux cotisation allocation familiale', default=3.45)
    t_cotis_ass_mal = fields.Float(string='Taux cotisation assurance maladie', default= 7)
    t_cotis_ass_vieil1 = fields.Float(string='Taux cotisation assurance Vieillesse', default= 1.9)
    t_contrib_financ_ds = fields.Float(string='Taux contribution au financement du dialogue social', default=0.01)
    t_cotis_reg_unif = fields.Float(string='Taux cotisation regime unifié agirc-arrco', default=1)
    t_red_gen_cotis_pat = fields.Float(string='Taux reduction generale des cotisations patronales', default=1)
    t_exo_cotis_sal = fields.Float(string='Taux exo cotisation salariale', default= 0)
    t_cotis_ac = fields.Float(string='Taux cotisation AC', default=4.05)
    t_cotis_ags = fields.Float(string='Taux cotisation AGS', default= 0.15)

    

    @api.depends('payslip')
    def _default_get(self):
        for list in self:
            list.mt_assiette_bp = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.mt_assiette_bd = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.mt_assiette_cac = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
            list.mt_base_bf = self.env['hr.payslip.line'].search([('slip_id','=',list.payslip.id),('code','=','SB')],limit=1).total
           