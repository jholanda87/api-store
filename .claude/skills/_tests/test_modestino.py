"""Testes das ferramentas da Modestino (estoque.py e vitrine.py)."""

import json
import os
import tempfile
import unittest

from _load import load

estoque = load("catalogo-modestino", "estoque")
vitrine = load("loja-lancamento-modestino", "vitrine")

STATE = {
    "stock": {"lots": [{"id": "L1", "qty": {"preta": {"P": 2, "M": 10}, "off": {"G": 1}}}]},
    "sales": [
        {"lines": [{"color": "preta", "size": "P", "qty": 1}]},
        {"custom": True, "lines": [{"color": "preta", "size": "M", "qty": 9}]},
        {"lines": []},
    ],
    "moves": [{"type": "brinde", "lines": [{"color": "off", "size": "G", "qty": 1}]}],
}


class Estoque(unittest.TestCase):
    def test_disponivel_e_situacao(self):
        r = {(x["color"], x["size"]): x for x in estoque.compute(STATE)["rows"]}
        self.assertEqual(r[("preta", "P")]["available"], 1)
        self.assertEqual(r[("preta", "P")]["status"], "últimas peças")
        self.assertEqual(r[("preta", "M")]["available"], 10)  # encomenda não sai
        self.assertEqual(r[("off", "G")]["status"], "esgotada")

    def test_reposicao_e_negativo(self):
        res = estoque.compute(STATE)
        self.assertTrue(res["reorder"])
        bad = dict(STATE, moves=[{"lines": [{"color": "off", "size": "G", "qty": 3}]}])
        self.assertEqual(len(estoque.compute(bad)["negative"]), 1)

    def test_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "e.csv")
            estoque.write_csv(estoque.compute(STATE), p)
            text = open(p, encoding="utf-8").read()
        self.assertIn("MOD-CAM-PRETA-P", text)


class Vitrine(unittest.TestCase):
    def levels(self, ad, avoid=None):
        return vitrine.lint({"avoid": avoid or [], "anuncios": [ad]})

    def test_exemplo_passa(self):
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, "..", "loja-lancamento-modestino", "vitrine.exemplo.json")
        data = json.load(open(path, encoding="utf-8"))
        self.assertEqual(vitrine.lint(data), [])

    def test_limite_e_marca(self):
        issues = self.levels({"canal": "mercado_livre", "titulo": "x" * 61 + " Insider",
                              "descricao": "ok"}, ["Insider"])
        msgs = " ".join(i["mensagem"] for i in issues if i["level"] == "error")
        self.assertIn("limite é 60", msgs)
        self.assertIn("Insider", msgs)

    def test_regras_da_casa(self):
        issues = self.levels({"canal": "loja", "titulo": "Camiseta 100% modal",
                              "descricao": "Do treino ao jantar sem trocar. Não desbota."})
        errs = [i for i in issues if i["level"] == "error"]
        warns = [i for i in issues if i["level"] == "warn"]
        self.assertEqual(len(errs), 2)
        self.assertTrue(any("testada" in w["mensagem"] for w in warns))

    def test_sem_logo_nao_dispara(self):
        self.assertEqual(self.levels({"canal": "loja", "titulo": "Camiseta lisa",
                                      "descricao": "Sem logo na frente."}), [])

    def test_preco_fora_da_tabela(self):
        issues = self.levels({"canal": "loja", "titulo": "Camiseta", "descricao": "R$ 59",
                              "preco": 59})
        self.assertTrue(any(i["campo"] == "preco" and i["level"] == "error" for i in issues))
        self.assertTrue(any("59" in i["mensagem"] and i["level"] == "warn" for i in issues))


if __name__ == "__main__":
    unittest.main()
