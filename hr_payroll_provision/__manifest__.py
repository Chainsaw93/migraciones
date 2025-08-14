# -*- coding: utf-8 -*-
{
    'name': "Hr Payroll Provision Management",
    'description': """
        Hr Payroll Provision Management for XIII and XIV
    """,

    'author': "Yen Martinez <yenykm@gmail.com>",
    'website': "http://www.ateneolab.com",
    'category': 'Human Resources',
    'version': '14.0.1.0.0',
    'depends': ['base', 'hr_contract', "hr_work_entry_contract", "hr_xiv", "hr_xiii"],
    'data': [
        'data/ir_sequence_data.xml',
        'view/hr_provision_view.xml',
        'view/hr_contract_ext_view.xml',
        "security/ir.model.access.csv",
    ],
}
