{
    "name": "Evolars Financeiro",
    "summary": "App Financeiro: contas a pagar e a receber por categoria, vencimentos, "
    "bancos (extrato e conciliação), fluxo de caixa, DRE e balanço",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Evolars LTDA",
    "website": "https://github.com/evolars/odoo-financeiro",
    "category": "Accounting",
    # Tudo o que o app mostra vem de módulos prontos da OCA; este módulo junta as
    # telas num lugar só e acrescenta a categoria (conta de resultado) nas listas.
    "depends": [
        "account",
        "account_due_list",
        "account_financial_report",
        "account_reconcile_oca",
        "account_statement_import_file_reconcile_oca",
        "account_statement_import_ofx",
        "account_statement_import_sheet_file",
        "l10n_br_mis_report",
        "mis_builder_cash_flow",
    ],
    "data": [
        "views/account_move_views.xml",
        "views/account_move_line_views.xml",
        "views/actions.xml",
        "views/menus.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": True,
}
