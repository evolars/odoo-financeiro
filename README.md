# Evolars Financeiro (Odoo 18)

App **Financeiro** para quem não tem o Enterprise: o "Contabilidade" do Odoo Enterprise
(`account_accountant`) não existe no Community, e o app de faturamento sozinho não dá conta do
controle financeiro. Este módulo junta, num app só, telas prontas da OCA:

| Menu | O que mostra | De onde vem |
| --- | --- | --- |
| A receber / A pagar | Faturas de cliente e de fornecedor em aberto, pelo vencimento, com a **categoria** | `account` |
| Vencimentos | Uma linha por parcela, entradas e saídas, agrupadas pelo mês | `account_due_list` |
| Bancos | Diários de banco e caixa: importar extrato (OFX, CSV/planilha) e conciliar | `account_reconcile_oca`, `account_statement_import_*` |
| Relatórios | Fluxo de caixa, DRE do mês e do ano, balanço, contas em aberto, atrasos e razão | `mis_builder_cash_flow`, `l10n_br_mis_report`, `account_financial_report` |
| Configuração | Categorias, previsões de caixa, contas bancárias e condições de pagamento | |

A **categoria** de uma conta a pagar ou a receber é a conta de resultado da linha (a de maior
valor, se houver várias). Criar uma categoria é criar uma conta de resultado: copie as etiquetas
de uma conta parecida, porque é por elas que o DRE põe a conta na linha certa.

Na instalação, as contas que não têm as etiquetas do plano de contas (bases migradas do 17, ou
com o plano carregado antes de o `l10n_br_coa_generic` trazê-las) recebem as que faltam. Sem
elas o DRE e o balanço saem vazios.

## Quem vê

O app aparece para quem tem **Recursos completos de contabilidade** (`account.group_account_user`,
na ficha do usuário ou na função dele).

## Na imagem

Agregado no `odoo-template` (série 18.0) com as dependências da OCA (`account-reconcile`,
`mis-builder`, `account-financial-reporting`, `bank-statement-import`, `l10n-brazil`) e instalado
em todos os clientes pela base da imagem.
