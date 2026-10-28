from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.evolars_financeiro.hooks import _etiquetas_do_modelo, corrigir_etiquetas


@tagged("post_install", "-at_install")
class TestCategoria(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Fornecedor Teste"})
        expense = cls.env["account.account"].search(
            [("account_type", "=", "expense"), ("company_ids", "in", cls.env.company.id)],
            limit=2,
        )
        cls.acc_a, cls.acc_b = expense[0], expense[1]

    def _bill(self, lines):
        return self.env["account.move"].create(
            {
                "move_type": "in_invoice",
                "partner_id": self.partner.id,
                "invoice_date": "2026-10-01",
                "invoice_line_ids": [
                    (0, 0, {"name": "x", "price_unit": price, "account_id": acc.id, "tax_ids": []})
                    for acc, price in lines
                ],
            }
        )

    def test_categoria_e_a_linha_de_maior_valor(self):
        bill = self._bill([(self.acc_a, 100), (self.acc_b, 900)])
        self.assertEqual(bill.evolars_category_id, self.acc_b)

    def test_linha_a_pagar_herda_categoria(self):
        bill = self._bill([(self.acc_a, 250)])
        bill.action_post()
        payable = bill.line_ids.filtered(lambda l: l.account_id.account_type == "liability_payable")
        self.assertEqual(payable.evolars_category_id, self.acc_a)

    def test_conta_sem_etiqueta_recebe_a_do_modelo(self):
        company = self.env.company
        etiquetas = _etiquetas_do_modelo(self.env, company.chart_template)
        if not etiquetas:
            self.skipTest("plano de contas sem etiquetas no modelo")
        conta = self.env["account.account"].search(
            [("code", "in", list(etiquetas)), ("company_ids", "in", company.id)], limit=1
        )
        conta.tag_ids = [(5, 0, 0)]
        self.assertTrue(corrigir_etiquetas(self.env, company))
        self.assertEqual(conta.tag_ids, etiquetas[conta.code])
        self.assertFalse(corrigir_etiquetas(self.env, company), "segunda rodada não tem o que corrigir")
