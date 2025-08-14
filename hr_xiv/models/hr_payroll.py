# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        for record in self:
            res = super(HrPayslip, self).action_payslip_done()
            for line in record.line_ids:
                if line.code == 'XIV-A':
                    record.contract_id.write({'accumulated_xiv_amount': 0.00})
                if line.code == 'XIV-P':
                    xiv_acc = record.contract_id.accumulated_xiv_amount + line.amount
                    record.contract_id.write({'accumulated_xiv_amount': xiv_acc})
            return res
