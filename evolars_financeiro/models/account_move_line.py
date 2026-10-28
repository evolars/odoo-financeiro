from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    evolars_category_id = fields.Many2one(
        related="move_id.evolars_category_id", store=True, string="Categoria"
    )
