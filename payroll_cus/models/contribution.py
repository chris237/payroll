from dataclasses import field
from odoo import fields, api, models, tools, _
from datetime import date
import datetime
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from calendar import monthrange
from operator import itemgetter
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)

class Cnps(models.Model):
    _name = 'contribution.cnps'
    _description = 'Contribution CNPS'
    _inherit = ['portal.mixin', 'mail.thread']
    _order = "id desc, create_date desc"
    _rec_name ='name_sub'
    
    number = fields.Char(string='Reference', readonly=True, index=True, tracking=True)
    name_sub = fields.Many2one('hr.payslip.run', string = 'Name' , tracking=True, ondelete="cascade")
    start_date = fields.Date(string ='Date From', tracking=True)
    cnps_e = fields.Monetary(string = ' Contribution Employee', compute='_total_summary', currency_field='company_currency_id')
    cnps_p = fields.Monetary(string = ' Contribution Employeur', compute='_total_summary', currency_field='company_currency_id')
    end_date = fields.Date(string='Date To', tracking=True)
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('closed', 'Closed')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    line_ids = fields.One2many('contribution.cnps.line', 'cnps_id', 
                               string='CNPS Line',
                               copy=False, readonly=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one(related='create_uid.company_id', store=True, readonly=True, default = 1)
    company_currency_id = fields.Many2one(related='company_id.currency_id', string='Company Currency',
        readonly=True, store=True,
        help='Utility field to express amount currency')

    @api.depends('line_ids.basic','line_ids.cnps_e','line_ids.cnps_p')
    def _total_summary(self):
        for move in self:
            basic = cnps_e = cnps_p = 0.0
            for line in move.line_ids:
                basic += line.basic
                cnps_e += line.cnps_e
                cnps_p += line.cnps_p
                basic = round(basic, 2)
                cnps_e = round(cnps_e, 2)
                cnps_p = round(cnps_p, 2)
            move.basic = basic
            move.cnps_e = cnps_e
            move.cnps_p = cnps_p

    def cancel(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    def post(self):
        for contribution in self:
            date_cnps = contribution.end_date
            cnps_year = date_cnps.strftime('%m') + '-' + date_cnps.strftime('%Y')
            number = self.env['ir.sequence'].next_by_code('contribution.cnps')
            contribution.write(
                {
                    'number': 'CNPS NO' + '-' + cnps_year + '-' + number,
                    'state': 'posted',
                })

class Cnpsline(models.Model):
    _name = 'contribution.cnps.line'
    _description = 'Contribution CNPS line'
    _inherit = ['portal.mixin', 'mail.thread']
    
    cnps_id = fields.Many2one('contribution.cnps', string='CNPS', auto_join=True, ondelete="cascade")
    names = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    code = fields.Char(string = ' STAFF NUMBER', tracking=True) 
    basic = fields.Monetary(string = ' BASIC', currency_field='company_currency_id', tracking=True)
    cnps_e = fields.Monetary(string = ' Part employee', currency_field='company_currency_id', tracking=True)
    cnps_p = fields.Monetary(string = ' Part Patronal', currency_field='company_currency_id', tracking=True)
    company_id = fields.Many2one(related='names.company_id', store=True, readonly=True)
    company_currency_id = fields.Many2one(related='company_id.currency_id', string='Company Currency',
        readonly=True, store=True,
        help='Utility field to express amount currency')

class payroll_contribution_cnps(models.AbstractModel):
    _name = 'report.payroll_cus.cnps_summary'
    _description = "Report Contributions CNPS"
    
    def get_detail(self, line_ids):
        result = []
        for l in line_ids:
            res = {}
            res.update({
                    'code': l.code,
                    'names': l.names.name,
                    'basic': l.basic,
                    'cnps_e': l.cnps_e,
                    'cnps_p': l.cnps_p,
                    })
            result.append(res)
        result = sorted(result, key=itemgetter('names'))
        return result
    
    @api.model
    def _get_report_values(self, docids, data=None):
        summary = self.env['contribution.cnps'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'contribution.cnps',
            'data': data,
            'docs': summary,
            'get_detail': self.get_detail,
        }

class HrPayslipRunbcd(models.Model):
    _name = 'hr.payslip.run'
    _inherit = ['hr.payslip.run', 'mail.thread', 'mail.activity.mixin']
    _description = 'Payslip Batches'

    cnps = fields.Boolean(string ='is CNPS', default=False)
    cnps_count = fields.Integer(compute='_compute_cnps_count')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Verify'),
        ('close', 'Done'),
        ('close1', 'Done'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
    
    def action_open_cnps(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "contribution.cnps",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [['name_sub', 'in', self.id]],
            "name": "CNPS",
        }

    def _compute_cnps_count(self):
        for payslip_run in self:
            cnps = self.env['contribution.cnps'].search([('name_sub', '=', payslip_run.id)])
            payslip_run.cnps_count = len(cnps)

    def create_cnps(self):
        for run in self:
            if run.cnps:
                raise UserError(_("un bordereau de CNPS a deja ete genere pour le lot  %s.") % (run.name,))
            company = self.env.company
            cnps = self.env['contribution.cnps'].create({
                        'name_sub': run.id,
                        'company_id': company.id,
                        'start_date': run.date_start,
                        'end_date': run.date_end
                    })
            for slip in run.slip_ids:
                # TODO is it necessary to interleave the calls ?
                # slip.action_payslip_done()
                # if not slip.employee_id.bank_account_id or not slip.employee_id.bank_account_id.acc_number:
                #     raise UserError(_('Please define bank account for the %s employee') % (slip.employee_id.name))
                cnps_e = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', '=', 'CNPSS')], limit=1)
                cnps_p = self.env['hr.payslip.line'].search([('slip_id', '=', slip.id), ('code', '=', 'CNPSP')], limit=1)
                if cnps_e or cnps_p:
                    self.env['contribution.cnps.line'].create({
                        'cnps_id': cnps.id,
                        'names': slip.employee_id.id,
                        'code': slip.employee_id.barcode,
                        'bysal': cnps_e.total,
                        'bysal': cnps_p.total
                    })        
        self.write({'cnps': True})
