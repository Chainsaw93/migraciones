from odoo import fields, models, api
import datetime
from odoo.exceptions import UserError


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Extend Contract Form for XIII'

    @api.depends('employee_id.payslip_count')
    def _compute_xiii(self):
        for record in self:
            init, end = self.get_xiii_period()
            proll = self.env['hr.payslip'].search(
                [('employee_id', '=', self.employee_id.id), ('date_from', '>=', init), ('date_from', '<=', end),
                 ('state', '=', 'done')])
            amount = 0
            for pr in proll:
                for ln in pr.line_ids:
                    if ln.code == 'BASIC':
                        amount += ln.amount
            record.accumulated_xiii_amount = amount
            # Todo: Comprobar que el empleado lleva mas de un anio trabajando o considerar los meses desde contratacion
            record.monthly_xiii_amount = round(float(amount / 12), 2)

    accumulate_xiii = fields.Boolean('Accumulate XIII')
    is_monthly_xiii = fields.Boolean('XIII by Month', default=True)
    monthly_xiii_amount = fields.Float('XIII Month', compute='_compute_xiii')
    accumulated_xiii_amount = fields.Float('XIII Accumulated', compute='_compute_xiii')

    @api.model
    def accumulated_xiii_amount(self, employee_id):
        # payslip_hist = self.env["hr.payslip.historic"]
        # payslip_hist_obj = payslip_hist.search(
        #     [("employee_id", "=", employee_id), ("date", ">=", from_date), ("date", "<=", to_date)])
        # result = sum(payslip_hist_obj.mapped(
        #     lambda o: o.total_amount))
        # return result / 12 if payslip_hist_obj else 0.0
        for record in self:
            year = fields.Date.today().year
            from_date, to_date = self.get_xiii_period()
            worker_months = 0
            contract_date = record.date_start
            if contract_date:
                if contract_date < datetime.date(year, 1, 1):
                    worker_months = fields.Date.today().month
                else:
                    worker_months = fields.Date.today().month - contract_date.month

            self.env['hr.payslip'].flush(['credit_note', 'employee_id', 'state', 'date_from', 'date_to'])
            self.env['hr.payslip.line'].flush(['total', 'slip_id', 'category_id'])
            self.env['hr.salary.rule.category'].flush(['code'])

            self.env.cr.execute("""SELECT sum(case when hp.credit_note is not True then (pl.total) else (-pl.total) end)
                                       FROM hr_payslip as hp, hr_payslip_line as pl, hr_salary_rule_category as rc
                                       WHERE hp.employee_id = %s AND hp.state = 'done'
                                       AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id
                                       AND rc.id = pl.category_id AND rc.code = %s""",
                                (employee_id, from_date, to_date, 'BASIC'))
            res = self.env.cr.fetchone()
            amount_xiii = round(res[0] / worker_months, 2) if res and res[0] and worker_months > 0 else 0.0
            record.accumulated_xiii_amount = amount_xiii
            return amount_xiii


    @api.model
    def month_xiii_amount(self, employee_id):
        for record in self:
            year = fields.Date.today().year
            from_date, to_date = self.get_xiii_period()
            worker_months = 0
            contract_date = record.date_start
            if contract_date:
                if contract_date < datetime.date(year, 1, 1):
                    worker_months = fields.Date.today().month
                else:
                    worker_months = fields.Date.today().month - contract_date.month

            self.env['hr.payslip'].flush(['credit_note', 'employee_id', 'state', 'date_from', 'date_to'])
            self.env['hr.payslip.line'].flush(['total', 'slip_id', 'category_id'])
            self.env['hr.salary.rule.category'].flush(['code'])

            self.env.cr.execute("""SELECT sum(case when hp.credit_note is not True then (pl.total) else (-pl.total) end)
                                FROM hr_payslip as hp, hr_payslip_line as pl, hr_salary_rule_category as rc
                                WHERE hp.employee_id = %s AND hp.state = 'done'
                                AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id
                                AND rc.id = pl.category_id AND rc.code = %s""",
                                (employee_id, from_date, to_date, 'BASIC'))
            res = self.env.cr.fetchone()
            amount_xiii = round(res[0] / worker_months, 2) if res and res[0] and worker_months > 0 else 0.0
            record.accumulated_xiii_amount = amount_xiii
            return amount_xiii

    @api.model
    def get_xiii_period(self):
        for record in self:
            #regime = record.regime
            xiii_config = self.env['hr.xiii.config'].search([], limit=1) or False
            if not xiii_config:
                raise UserError('Configure XIII period on Payroll Application')
            return xiii_config.init_date_xiii, xiii_config.end_date_xiii

    def get_xiii_pay_date(self):
        for record in self:
            #regime = record.regime  # Configured in contract
            xiii_config = self.env['hr.xiii.config'].search([], limit=1)
            if not xiii_config:
                raise UserError('Configure XIII period on Payroll Application')
            return xiii_config.pay_date_xiii
        pass
