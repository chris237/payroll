# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from datetime import datetime, date


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'
    _description = 'Salary Structure'


    @api.model
    def _get_default_rule_ids(self):
        if self.env.company.country_code == 'CM':   
            # CM
            return [
                (0, 0, {
                    'name': 'Basic Salary',
                    'sequence': 1,
                    'code': 'BASIC',
                    'category_id': self.env.ref('hr_payroll.BASIC').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = payslip.paid_amount',
                }),
                (0, 0, {
                    'name': "Prime d'ancienneté",
                    'sequence': 2,
                    'code': 'PA',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '12',
                }),
                (0, 0, {
                    'name': "Indemnité de representation",
                    'sequence': 2,
                    'code': 'IR',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '12500',
                }),
                (0, 0, {
                    'name': "Indemnité de logement",
                    'sequence': 2,
                    'code': 'IL',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '40',
                }),
                (0, 0, {
                    'name': "Prime de Risque",
                    'sequence': 2,
                    'code': 'PR',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '15000',
                }),
                (0, 0, {
                    'name': "Avantage En Nature Vehicule",
                    'sequence': 2,
                    'code': 'ANV',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '100000',
                }),
                (0, 0, {
                    'name': "Total Brut",
                    'sequence': 5,
                    'code': 'ALW',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = BASIC + PA + IR + IL + PR + ANV',
                }),
                (0, 0, {
                    'name': "Taxe sur Developpement Local S",
                    'sequence': 6,
                    'code': 'TDLS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '2520',
                }),
                (0, 0, {
                    'name': "Credit Foncier Salarial S",
                    'sequence': 6,
                    'code': 'CFSS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '1',
                }),
                (0, 0, {
                    'name': "Retenu CNPS S",
                    'sequence': 6,
                    'code': 'CNPSS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '4.2',
                }),
                (0, 0, {
                    'name': "Redevance Audio-Visuel S",
                    'sequence': 6,
                    'code': 'RAVS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '8450',
                }),
                (0, 0, {
                    'name': "Retenue IRRP S",
                    'sequence': 6,
                    'code': 'RIS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '64337',
                }),
                (0, 0, {
                    'name': "CAC IRPP S",
                    'sequence': 6,
                    'code': 'CACS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '10',
                }),
                (0, 0, {
                    'name': "Accident de Travail S",
                    'sequence': 6,
                    'code': 'ATS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Allocation Familiale S",
                    'sequence': 6,
                    'code': 'AFS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Credit Foncier Patronal S",
                    'sequence': 6,
                    'code': 'CFPS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Fond National de l'Emploi S",
                    'sequence': 6,
                    'code': 'FNES',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': 'Total Cotisation S',
                    'sequence': 10,
                    'code': 'TCS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = TDLS + CFSS + CNPSS + RAVS+ RIS + CACS + ATS + AFS + CFPS + FNES',
                }),
                (0, 0, {
                    'name': "Taxe sur Developpement Local P",
                    'sequence': 6,
                    'code': 'TDLP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '0',
                }),
                (0, 0, {
                    'name': "Retenue Mutuelle",
                    'sequence': 6,
                    'code': 'RM',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '7000',
                }),
                (0, 0, {
                    'name': "Credit Foncier Salarial P",
                    'sequence': 6,
                    'code': 'CFSP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Retenu CNPS P",
                    'sequence': 6,
                    'code': 'CNPSP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '4.2',
                }),
                (0, 0, {
                    'name': "Redevance Audio-Visuel P",
                    'sequence': 6,
                    'code': 'RAVP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '0',
                }),
                (0, 0, {
                    'name': "Retenue IRRP P",
                    'sequence': 6,
                    'code': 'RIP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'fix',
                    'quantity': '1.0',
                    'amount_fix': '0',
                }),
                (0, 0, {
                    'name': "CAC IRPP P",
                    'sequence': 6,
                    'code': 'CACP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Accident de Travail P",
                    'sequence': 6,
                    'code': 'ATP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '1.75',
                }),
                (0, 0, {
                    'name': "Allocation Familiale P",
                    'sequence': 6,
                    'code': 'AFP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '7',
                }),
                (0, 0, {
                    'name': "Credit Foncier Patronal P",
                    'sequence': 6,
                    'code': 'CFPP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '1.5',
                }),
                (0, 0, {
                    'name': "Fond National de l'Emploi P",
                    'sequence': 6,
                    'code': 'FNEP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'BASIC',
                    'quantity': '1.0',
                    'amount_percentage': '1',
                }),
                (0, 0, {
                    'name': 'Total Cotisation P',
                    'sequence': 10,
                    'code': 'TCP',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = TDLP + CFSP + CNPSP + RAVP+ RIP + CACP + ATP + AFP + CFPP + FNEP',
                }),
                (0, 0, {
                    'name': 'Gross',
                    'sequence': 100,
                    'code': 'GROSS',
                    'category_id': self.env.ref('hr_payroll.GROSS').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = categories.BASIC + categories.ALW',
                }),
                (0, 0, {
                    'name': 'Net Salary',
                    'sequence': 200,
                    'code': 'NET',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = ALW - TCS',
                })
        ]
        if self.env.company.country_code == 'FR': 
            # FR
            return [
                (0, 0, {
                    'name': 'Basic Salary',
                    'sequence': 1,
                    'code': 'BASIC',
                    'category_id': self.env.ref('hr_payroll.BASIC').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = payslip.paid_amount',
                }),
                (0, 0, {
                    'name': 'HEURES ABSENCES ENTREE/SORTIE ',
                    'sequence': 1,
                    'code': 'HAES',
                    'category_id': self.env.ref('hr_payroll.BASIC').id, 
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'if worked_days.LEAVE90:result = 4.41 *(worked_days.LEAVE90.number_of_hours) else:result = 0 ',
                }),
                (0, 0, {  
                    'name': 'Basic Brut',
                    'sequence': 2,
                    'code': 'SB',
                    'category_id': self.env.ref('hr_payroll.GROSS').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = BASIC - HAES',
                }),
                (0, 0, {
                    'name': "Sécurité  sociale-Maladie Maternité Invalidité Décès E",
                    'sequence': 6,
                    'code': 'SSMMIDE',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Sécurité  sociale-Maladie Maternité Invalidité Décès P",
                    'sequence': 6,
                    'code': 'SSMMIDP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '7',
                }),
                (0, 0, {
                    'name': "Complément Incapacité Invalidité Décès TA E",
                    'sequence': 6,
                    'code': 'CIIDTE',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '0.55304',
                }),
                (0, 0, {
                    'name': "Complément Incapacité Invalidité Décès TA P",
                    'sequence': 6,
                    'code': 'CIIDTP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '0.55304',
                }),
                (0, 0, {
                    'name': "ACCIDENTS DU TRAVAIL & MAL. PROFESSIONNELLES",
                    'sequence': 6,
                    'code': 'ATMP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '0.9',
                }),
                (0, 0, {
                    'name': "Sécurité Sociale plafonnée E",
                    'sequence': 6,
                    'code': 'SSPE',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '100.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Sécurité Sociale plafonnée P",
                    'sequence': 6,
                    'code': 'SSPP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1.0',
                    'amount_percentage': '8.5',
                }),
                (0, 0, {
                    'name': "Sécurité Sociale déplafonnée E",
                    'sequence': 6,
                    'code': 'SSDE',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Sécurité Sociale déplafonnée P",
                    'sequence': 6,
                    'code': 'SSDP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '1.9',
                }),
                (0, 0, {
                    'name': "Complémentaire Tranche 1 E",
                    'sequence': 6,
                    'code': 'CTE',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Complémentaire Tranche 1 P",
                    'sequence': 6,
                    'code': 'CTP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '6.1',
                }),
                (0, 0, {
                    'name': "FAMILLE E",
                    'sequence': 6,
                    'code': 'FAME',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "FAMILLE P",
                    'sequence': 6,
                    'code': 'FAMP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '3.5',
                }),
                (0, 0, {
                    'name': "Chomage E",
                    'sequence': 6,
                    'code': 'CHOME',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1.0',
                    'amount_percentage': '0',
                }),
                (0, 0, {
                    'name': "Chomage P",
                    'sequence': 6,
                    'code': 'CHOMP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '4.05',
                }),
                (0, 0, {
                    'name': "AUTRES CONTRIBUTIONS DUES PAR L'EMPLOYEUR",
                    'sequence': 6,
                    'code': 'ACDP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '4.2',
                }),
                (0, 0, {
                    'name': "Exonérations de cotisations et contributions",
                    'sequence': 6,
                    'code': 'ECC',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'SB',
                    'quantity': '1',
                    'amount_percentage': '-32.05',
                }),
                (0, 0, {
                    'name': "Total Cotisations E",
                    'sequence': 6,
                    'code': 'TCE',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = SSMMIDE + CIIDTE + SSPE + SSDE + CTE + FAME + CHOME',
                }),
                (0, 0, {
                    'name': "Total Contributions P",
                    'sequence': 6,
                    'code': 'TCP',
                    'category_id': self.env.ref('hr_payroll.COMP').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = SSMMIDP + CIIDTP + ATMP + SSPP + SSDP + CTP + FAMP + CHOMP + ACDP + ECC',
                }),
                (0, 0, {
                    'name': "NET IMPOSABLE",
                    'sequence': 6,
                    'code': 'NETI',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = SB - TCE',
                }),
                (0, 0, {
                    'name': "INDEMNITE REPAS",
                    'sequence': 6,
                    'code': 'IREPAS',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'worked_days.WORK100.number_of_days',
                    'quantity': '4',
                    'amount_percentage': '100',
                }),
                (0, 0, {
                    'name': 'Net Salary',
                    'sequence': 200,
                    'code': 'NET',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = SSMMIDP + CIIDTP + ATMP + SSPP + SSDP + CTP + FAMP + CHOMP + ACDP + ECC',
                }),

                (0, 0, {
                    'name': 'Allègement de cotisations + part réduite cotisation Allocation familiales',
                    'sequence': 200,
                    'code': 'ACRCAF',
                    'category_id': self.env.ref('hr_payroll.ALW').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = 0.39862 * SB',
                }),
                (0, 0, {
                    'name': 'Total versé par l employeur (Super brut)',
                    'sequence': 200,
                    'code': 'TVESB',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = SB + TCP',
                }),
                (0, 0, {
                    'name': 'Net à payer avant impôt sur le revenu',
                    'sequence': 200,
                    'code': 'NETAPAISR',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = IREPAS + NETI',
                }),
                (0, 0, {
                    'name': 'Impôt sur le revenu prélevé à la source',
                    'sequence': 200,
                    'code': 'IRPS',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'percentage',
                    'amount_percentage_base': 'NETAPAISR',
                    'quantity': '1',
                    'amount_percentage': '1.5',
                }),
                (0, 0, {
                    'name': 'Net a payer',
                    'sequence': 200,
                    'code': 'NETAP',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = NETAPAISR - IRPS',
                }),
                (0, 0, {
                    'name': 'Plafond mensuels de sécurité sociale',
                    'sequence': 200,
                    'code': 'PPMS',
                    'category_id': self.env.ref('hr_payroll.NET').id,
                    'condition_select': 'none',
                    'amount_select': 'code',
                    'amount_python_compute': 'result = 3428',
                })]


    rule_ids = fields.One2many(
        'hr.salary.rule', 'struct_id',
        string='Salary Rules', default=_get_default_rule_ids)

class HrEmployeeA(models.Model):
    _inherit = 'hr.employee'
    indice = fields.Char('Indice')
    level = fields.Integer('Level')
    numsec = fields.Char('NumSec')
    msa = fields.Char('Urssaf/Msa')
    insee = fields.Char('N° INSEE')
    coef = fields.Char('Coefficient')


class HrCompany(models.Model):
    _inherit = 'res.company'

    convention = fields.Char('Convention collective')
    ppms = fields.Integer('ppms')
# class HrPayslip(models.Model):
#     _inherit = 'hr.payslip'
#     qualification = fields.Char(string='Qualification')

class HrcontractA(models.Model):
    _inherit = 'hr.contract'
    
    anc = fields.Char(string='Anciennete', compute='_calculate_age')

    # qualif = fields.Char(string='Qualification')
    category = fields.Char(string='Catégorie')
    status_pro = fields.Char(string='Statut professionnel')


    def findAge(self, current_date, current_month, current_year,
                birth_date, birth_month, birth_year):

        # if birth date is greater then current birth_month
        # then donot count this month and add 30 to the date so
        # as to subtract the date and get the remaining days
        
        month =[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (birth_date > current_date):
            current_month = current_month - 1
            current_date = current_date + month[birth_month-1]
            
            
        # if birth month exceeds current month, then
        # donot count this year and add 12 to the
        # month so that we can subtract and find out
        # the difference
        if (birth_month > current_month):		
            current_year = current_year - 1;
            current_month = current_month + 12;
            
        # calculate date, month, year
        calculated_date = current_date - birth_date;
        calculated_month = current_month - birth_month;
        calculated_year = current_year - birth_year;
        
        # print present age
        # print("Present Age")
        # print("Years:", calculated_year, "Months:",
        #    calculated_month, "Days:", calculated_date)
        if calculated_year < 1 :
            if calculated_month < 1:
                age = str(calculated_date) + ' jours '
            else:
                age = str(calculated_month) + ' mois ' + str(calculated_date) + ' jours '
        else:
            age = str(calculated_year) + ' ans ' + str(calculated_month) + ' mois ' + str(calculated_date) + ' jours '
        return age

    # print("Your date of birth (dd mm yyyy)")
    # date_of_birth = datetime.strptime(input("--->"), "%d %m %Y")

    @api.depends('date_start') 
    def _calculate_age(self):
       
        for line in self:
            start_date = line.date_start
            today = date.today()
            # line.anc = today.year - start_date.year - ((today.month, today.day) < (start_date.month, start_date.day))
            line.anc = self.findAge(today.day, today.month, today.year, start_date.day, start_date.month, start_date.year)

class HrPayslipbcd(models.Model):
    _inherit = 'hr.payslip'
    _description = 'Payslip Pay'
    state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('done1', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft',
        help="""* When the payslip is created the status is \'Draft\'
                \n* If the payslip is under verification, the status is \'Waiting\'.
                \n* If the payslip is confirmed then status is set to \'Done\'.
                \n* When user cancel payslip the status is \'Rejected\'.""")