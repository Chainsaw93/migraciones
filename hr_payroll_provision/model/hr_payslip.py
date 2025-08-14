from odoo import fields, models, api, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        for record in self:
            res = super(HrPayslip, self).action_payslip_done()
            for line in record.line_ids:
                if line.code == 'XIV-A':
                    record.contract_id.get_pending_provision_xiv().write({"state":"paid"})
                if line.code == 'XIV-P':
                    record.contract_id.create_provision_xiv(line.amount, record.date_to, record.name)
                if line.code == 'XIII-A':
                    xiii = record.contract_id.get_pending_provision_xiii().write({"state":"paid"})
                if line.code == 'XIII-P':
                    record.contract_id.create_provision_xiii(line.amount, record.date_to, record.name)
        return res