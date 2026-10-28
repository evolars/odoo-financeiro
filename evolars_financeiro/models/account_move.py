from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # A "categoria" da planilha do financeiro é a conta de resultado da linha.
    # Com várias linhas, vale a de maior valor: é o que a pessoa diria que a
    # conta "é".
    evolars_category_id = fields.Many2one(
        "account.account",
        string="Categoria",
        compute="_compute_evolars_category_id",
        store=True,
        index=True,
    )

    @api.depends("invoice_line_ids.account_id", "invoice_line_ids.price_subtotal")
    def _compute_evolars_category_id(self):
        for move in self:
            lines = move.invoice_line_ids.filtered(
                lambda line: line.display_type == "product" and line.account_id
            )
            top = max(lines, key=lambda line: abs(line.price_subtotal), default=None)
            move.evolars_category_id = top.account_id if top else False
