from dataclasses import field
from email.policy import default
from odoo import fields, api, models, tools, _
from datetime import date
import datetime
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from calendar import monthrange
from operator import itemgetter
from odoo.tools.safe_eval import safe_eval

class Dsn_recp(models.Model):
    _name = 'dsn.recap'
    _description = 'DSN Recap'
    _inherit = ['portal.mixin', 'mail.thread']
    _order = "id desc, create_date desc"

    payslip = fields.Many2one('hr.payslip', string = 'payslip' , tracking=True, ondelete="cascade")
    liste = fields.Many2one('dsn.liste', string = 'Dossier' , tracking=True, ondelete="cascade")
    company_id = fields.Char(string ='Entreprise', tracking=True, compute='_default_get')
    siret = fields.Char(string ='N SIRET', tracking=True, compute='_default_get')
    employee = fields.Char(string ='employee', tracking=True, compute='_default_get')

    ape = fields.Many2one('dsn.liste', string = 'Dossier' , tracking=True, ondelete="cascade")

    @api.depends('payslip')
    def _default_get(self):
        for lis in self:
            list.siret = list.payslip.company_id.siret
            list.company_id = list.payslip.company_id.name
            list.employee = list.payslip.employee_id
