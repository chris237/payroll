from dataclasses import field
from email.policy import default
from odoo import fields, api, models, tools, _
from datetime import date
import datetime
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from calendar import monthrange
from operator import itemgetter
from odoo.tools.safe_eval import safe_eval

class Dsn_liste(models.Model):
    _name = 'dsn.liste'
    _description = 'DSN LISTE'
    _inherit = ['portal.mixin', 'mail.thread']
    _order = "id desc, create_date desc"
    _rec_name = "code"

    payslip = fields.Many2one('hr.payslip', string = 'payslip' , tracking=True, ondelete="cascade")
    
    code = fields.Char(string ='code', tracking=True, default='New')
    rais = fields.Char(string ='Raison Sociale', tracking=True, compute='_default_get')
    siret = fields.Char(string ='N SIRET', tracking=True, compute='_default_get')
    employee = fields.Char(string ='employee', tracking=True, compute='_default_get')
    regime = fields.Char(string ='Regime', tracking=True, default='Général')

    @api.depends('payslip')
    def _default_get(self):
        for list in self:
            list.siret = list.payslip.company_id.siret
            list.rais = list.payslip.company_id.name
            list.employee = list.payslip.employee_id.name