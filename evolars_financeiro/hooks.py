import csv
import logging

from odoo.tools.misc import file_open

_logger = logging.getLogger(__name__)


def _etiquetas_do_modelo(env, template):
    """Código da conta -> etiquetas, lidas do CSV do plano de contas.

    É pela etiqueta que o DRE e o balanço do l10n_br_mis_report põem a conta na
    linha certa. Bases cujo plano foi carregado sem elas (migradas do 17, ou de
    antes de o l10n_br_coa_generic trazer a coluna) ficam com os relatórios
    vazios. A coluna é lida como ``tag_ids`` ou ``tag_ids:id``.
    """
    module = env["account.chart.template"]._get_chart_template_mapping().get(template, {}).get("module")
    if not module:
        return {}
    path = f"{module}/data/template/account.account-{template}.csv"
    try:
        with file_open(path) as fh:
            rows = list(csv.DictReader(fh))
    except FileNotFoundError:
        return {}
    result = {}
    for row in rows:
        refs = row.get("tag_ids") or row.get("tag_ids:id") or ""
        tags = env["account.account.tag"]
        for ref in filter(None, (r.strip() for r in refs.split(","))):
            tags |= env.ref(ref, raise_if_not_found=False) or tags.browse()
        if tags:
            result[row["code"]] = tags
    return result


def corrigir_etiquetas(env, company):
    """Põe nas contas da empresa as etiquetas do modelo que faltam (nunca tira)."""
    etiquetas = _etiquetas_do_modelo(env, company.chart_template)
    contas = env["account.account"].with_company(company).search(
        [("company_ids", "in", company.id), ("code", "in", list(etiquetas))]
    )
    corrigidas = 0
    for conta in contas:
        faltam = etiquetas[conta.code] - conta.tag_ids
        if faltam:
            conta.tag_ids = [(4, tag.id) for tag in faltam]
            corrigidas += 1
    _logger.info("evolars_financeiro: %s contas de %s receberam etiquetas", corrigidas, company.name)
    return corrigidas


def post_init_hook(env):
    for company in env["res.company"].search([("chart_template", "!=", False)]):
        corrigir_etiquetas(env, company)
