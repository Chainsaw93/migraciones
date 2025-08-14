from odoo import fields, models, api
from odoo.exceptions import UserError


class HrContract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Extend Contract Form for XIV'

    accumulate_xiv = fields.Boolean('Accumulate XIV')
    accumulated_xiv_amount = fields.Float('XIV Acumulado',
                                          help='XIV Provisionado desde ingreso o desde inicio período hasta la fecha.'
                                               ' Editar manual solo para establecer valores iniciales.')

    @api.model
    def month_xiv_amount(self):
        sbu = self.env['hr.sbu.table'].search([('state', '=', 'in_effect')], limit=1) and \
              self.env['hr.sbu.table'].search([('state', '=', 'in_effect')], limit=1).rmu or 0.0
        xiv = round(float(sbu / 360) * 30, 2) if sbu else 0.0
        return xiv

    @api.model
    def get_current_sbu(self):
        sbu = self.env['hr.sbu.table'].search([('state', '=', 'in_effect')], limit=1) and \
              self.env['hr.sbu.table'].search([('state', '=', 'in_effect')], limit=1).rmu or 0.0
        return sbu

    @api.model
    def acc_xiv_amount(self):
        for record in self:
            num_months = (fields.Date.today().year - record.date_start.year) * 12 + (
                    fields.Date.today().month - record.date_start.month)
            if num_months >= 11:
                sbu = self.env['hr.sbu.table'].search([('state', '=', 'in_effect')], limit=1) and \
                      self.env['hr.sbu.table'].search([('state', '=', 'in_effect')], limit=1).rmu or 0.0
                xiv = sbu
            else:
                xiv = record.accumulated_xiv_amount
            return xiv

    @api.model
    def get_xiv_period(self):
        for record in self:
            regime = record.regime  # Configured in contract
            xiv_config = self.env['hr.xiv.config'].search([('regime', '=', regime)], limit=1)
            if not xiv_config:
                raise UserError('Configure XIV period on Payroll Application')
            return xiv_config.init_date_xiv, xiv_config.end_date_xiv
        pass

    def get_xiv_pay_date(self):
        for record in self:
            regime = record.regime  # Configured in contract
            xiv_config = self.env['hr.xiv.config'].search([('regime', '=', regime)], limit=1)
            if not xiv_config:
                raise UserError('Configure XIV period on Payroll Application')
            return xiv_config.pay_date_xiv
        pass
