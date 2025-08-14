{
    'name': 'XIV for Payroll',
    'version': '14.1.0.0',
    'summary': 'XIV for payroll',
    'description': 'XIV for payroll',
    'category': 'Human Resources',
    'author': 'Yen Martinez <yenykm@gmail.com>',
    'website': 'http://www.ateneolab.com',
    'sequence': '1',
    'depends': ['hr_payroll', 'hr_sbu_table', 'hr_payroll_ext', 'hr_reserve_fund', 'hr_job_regime_base'],
    'data': [
        'data/payroll_rule_data.xml',
        'views/contract_ext.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
