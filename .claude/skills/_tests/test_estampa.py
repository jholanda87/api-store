"""Testes das ferramentas da linha Estampada (estampa.py, separar.py, mockup.py)."""

import os
import tempfile
import unittest

from _load import load

estampa = load("estampa-arte-modestino", "estampa")
separar = load("estampa-arte-modestino", "separar")
mockup = load("estampa-arte-modestino", "mockup")

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "estampa-arte-modestino", "exemplo.svg"), encoding="utf-8") as _f:
    EXEMPLO = _f.read()


def svg(corpo, w="60mm", vb="0 0 60 40"):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%s" viewBox="%s">%s</svg>' % (w, vb, corpo)


def niveis(r, nivel):
    return [p["msg"] for p in r["problemas"] if p["nivel"] == nivel]


class Checagem(unittest.TestCase):
    def test_exemplo_pronto(self):
        r = estampa.avaliar(EXEMPLO, posicao="peito")
        self.assertEqual(niveis(r, "ERRO"), [])
        self.assertEqual(r["tamanho_cm"], [9.0, 5.4])
        self.assertEqual(r["tintas"], ["#CBBFAE"])
        self.assertTrue(r["camisetas"]["preto"]["funciona"])
        self.assertTrue(r["camisetas"]["off-white"]["tom_sobre_tom"])
        self.assertTrue(r["camisetas"]["preto"]["base_branca"])

    def test_sem_tamanho_real(self):
        r = estampa.avaliar(svg('<rect width="10" height="10"/>', w="600"))
        self.assertTrue(any("tamanho real" in m for m in niveis(r, "ERRO")))

    def test_tintas_demais_e_heranca(self):
        corpo = ('<g fill="#ECE7DE"><rect width="10" height="10"/></g>'
                 '<rect x="20" width="10" height="10" style="fill:#5b3f30"/>'
                 '<circle cx="50" cy="20" r="5" fill="#22201D"/>')
        r = estampa.avaliar(svg(corpo))
        self.assertEqual(r["tintas"], ["#ECE7DE", "#5B3F30", "#22201D"])
        self.assertTrue(any("3 tintas" in m for m in niveis(r, "ERRO")))
        r = estampa.avaliar(svg(corpo), vazado="#22201D")
        self.assertEqual(niveis(r, "ERRO"), [])

    def test_traco_fino_por_tecnica(self):
        corpo = '<path d="M0 0H60" stroke="#22201D" stroke-width="0.4"/>'
        self.assertTrue(niveis(estampa.avaliar(svg(corpo), "silk"), "ERRO"))
        self.assertEqual(niveis(estampa.avaliar(svg(corpo), "dtf"), "ERRO"), [])

    def test_efeitos_proibidos(self):
        corpo = ('<defs><linearGradient id="g"/></defs><rect width="9" height="9" fill="url(#g)"/>'
                 '<text>oi</text><image href="x.png"/><rect width="9" height="9" opacity="0.5"/>')
        erros = " ".join(niveis(estampa.avaliar(svg(corpo)), "ERRO"))
        for termo in ("Degradê", "<text>", "bitmap", "Transparência"):
            self.assertIn(termo, erros)

    def test_outra_marca_e_cavalheiro(self):
        corpo = '<title>Cavalheiro</title><rect id="insider" width="9" height="9"/>'
        r = estampa.avaliar(svg(corpo), evitar=["Insider"])
        self.assertTrue(any("Insider" in m for m in niveis(r, "ERRO")))
        self.assertTrue(any("vetor oficial" in m for m in niveis(r, "INFO")))
        self.assertFalse(any("Cavalheiro" in m for m in niveis(r, "ERRO")))

    def test_posicao_fora_da_faixa(self):
        r = estampa.avaliar(EXEMPLO, posicao="costas")
        self.assertTrue(any("10 a 32" in m for m in niveis(r, "AVISO")))

    def test_vetores_oficiais_passam(self):
        pasta = os.path.join(HERE, "..", "..", "..", "estampas", "marca")
        if not os.path.isdir(pasta):
            self.skipTest("fora do repositório")
        for nome in os.listdir(pasta):
            r = estampa.avaliar(open(os.path.join(pasta, nome), encoding="utf-8").read(), "dtf")
            self.assertEqual(niveis(r, "ERRO"), [], nome)


class Fotolitos(unittest.TestCase):
    def test_um_por_tinta_com_vazado_e_base(self):
        corpo = ('<rect width="60" height="40" fill="#CBBFAE"/>'
                 '<circle cx="30" cy="20" r="8" fill="#5B3F30"/>'
                 '<circle cx="10" cy="10" r="4" fill="#1E1D1C"/>')
        with tempfile.TemporaryDirectory() as d:
            arqs = separar.separar(svg(corpo), d, vazado="#1E1D1C", base_branca=True, nome="t")
            nomes = sorted(os.path.basename(a) for a in arqs)
            self.assertEqual(nomes, ["t-tinta-0-base-branca.svg", "t-tinta-1-cbbfae.svg",
                                     "t-tinta-2-5b3f30.svg"])
            areia = open(os.path.join(d, "t-tinta-1-cbbfae.svg"), encoding="utf-8").read()
            r = estampa.pinturas(estampa.ET.fromstring(areia))
            cores = [f["fill"] for f in r if f["tag"] in ("rect", "circle") and f["fill"]]
            # fundo branco, retângulo areia imprime, círculo mapple vaza, vazado não imprime
            self.assertEqual(cores[:4], ["#FFFFFF", "#000000", "#FFFFFF", "#FFFFFF"])
            base = open(os.path.join(d, "t-tinta-0-base-branca.svg"), encoding="utf-8").read()
            r = estampa.pinturas(estampa.ET.fromstring(base))
            cores = [f["fill"] for f in r if f["tag"] in ("rect", "circle") and f["fill"]]
            self.assertEqual(cores[:4], ["#FFFFFF", "#000000", "#000000", "#FFFFFF"])
            self.assertIn("Vazado", open(os.path.join(d, "separacoes.md"), encoding="utf-8").read())


class Mockup(unittest.TestCase):
    def test_tres_camisetas_em_escala(self):
        texto = mockup.mockup(EXEMPLO, "peito")
        for nome in ("PRETO", "MAPPLE", "OFF-WHITE"):
            self.assertIn(nome + " · peito · 9.0 × 5.4 cm", texto)
        self.assertIn('width="9"', texto)


if __name__ == "__main__":
    unittest.main()
