import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from agente_extrator import extrair_conceitos
from agente_perguntas import criar_perguntas
from agente_revisor import rever_perguntas
from main import main, preparar_material


MATERIAL_CORRETO = """O protocolo HTTP permite a transferência de recursos na Web.
O DNS traduz nomes de domínio em endereços IP.
O endereço IPv4 possui 32 bits.
O endereço IPv6 possui 128 bits.
Um router encaminha pacotes entre redes diferentes.
O modelo OSI é constituído por sete camadas.
O protocolo TCP estabelece uma ligação orientada à conexão.
A máscara de sub-rede identifica a parte de rede e a parte de host."""

MATERIAL_INCORRETO = """O protocolo HTTP é utilizado exclusivamente para alimentar baterias.
O DNS converte endereços IP em temperaturas do processador.
O endereço IPv4 possui 512 bits.
O endereço IPv6 possui apenas 8 bits.
Um router serve para imprimir documentos em papel.
O modelo OSI é constituído por duas camadas.
O protocolo TCP não permite qualquer tipo de comunicação.
A máscara de sub-rede identifica apenas a marca do computador."""


class TestesProjeto(unittest.TestCase):

    def setUp(self):
        # O extrator original divide por pontuação. A função auxiliar
        # da main também garante que cada linha é tratada como afirmação.
        self.conceitos_corretos = extrair_conceitos(
            preparar_material(MATERIAL_CORRETO)
        )
        self.conceitos_incorretos = extrair_conceitos(
            preparar_material(MATERIAL_INCORRETO)
        )

    def test_extrator_recebe_separadamente_os_dois_materiais(self):
        self.assertEqual(len(self.conceitos_corretos), 8)
        self.assertEqual(len(self.conceitos_incorretos), 8)

    def test_agente2_cria_cinco_perguntas_e_tres_flashcards(self):
        resultado = criar_perguntas(
            self.conceitos_corretos,
            self.conceitos_incorretos,
        )
        self.assertEqual(len(resultado["perguntas_mcq"]), 5)
        self.assertEqual(len(resultado["flashcards"]), 3)

    def test_cada_pergunta_tem_uma_correta_e_tres_incorretas(self):
        resultado = criar_perguntas(
            self.conceitos_corretos,
            self.conceitos_incorretos,
        )

        corretos = {c.casefold() for c in self.conceitos_corretos}
        incorretos = {c.casefold() for c in self.conceitos_incorretos}

        for pergunta in resultado["perguntas_mcq"]:
            opcoes = list(pergunta["opcoes"].values())
            self.assertEqual(len(opcoes), 4)
            self.assertEqual(len({x.casefold() for x in opcoes}), 4)

            resposta = pergunta["opcoes"][pergunta["resposta_correta"]]
            self.assertIn(resposta.casefold(), corretos)
            self.assertEqual(sum(x.casefold() in corretos for x in opcoes), 1)
            self.assertEqual(sum(x.casefold() in incorretos for x in opcoes), 3)

    def test_flashcards_usam_apenas_material_correto(self):
        resultado = criar_perguntas(
            self.conceitos_corretos,
            self.conceitos_incorretos,
        )
        corretos = {c.casefold() for c in self.conceitos_corretos}
        for flashcard in resultado["flashcards"]:
            self.assertIn(flashcard["resposta"].casefold(), corretos)

    def test_sem_tres_afirmacoes_incorretas_nao_inventa_distratores(self):
        resultado = criar_perguntas(self.conceitos_corretos, self.conceitos_incorretos[:2])
        self.assertEqual(resultado["perguntas_mcq"], [])
        self.assertEqual(len(resultado["flashcards"]), 3)
        self.assertTrue(resultado["avisos"])

    def test_sem_material_incorreto_nao_cria_perguntas(self):
        resultado = criar_perguntas(self.conceitos_corretos, [])
        self.assertEqual(resultado["perguntas_mcq"], [])
        self.assertEqual(len(resultado["flashcards"]), 3)

    def test_agente3_original_valida_as_perguntas_e_flashcards(self):
        resultado_agente2 = criar_perguntas(
            self.conceitos_corretos,
            self.conceitos_incorretos,
        )
        revisao = rever_perguntas(
            resultado_agente2["perguntas_mcq"],
            resultado_agente2["flashcards"],
            MATERIAL_CORRETO,
        )
        self.assertEqual(len(revisao["perguntas_validas"]), 5)
        self.assertEqual(len(revisao["perguntas_rejeitadas"]), 0)
        self.assertEqual(len(revisao["flashcards_validos"]), 3)

    def test_main_pede_os_dois_materiais_e_executa_pipeline(self):
        linhas = (
            MATERIAL_CORRETO.splitlines()
            + ["FIM"]
            + MATERIAL_INCORRETO.splitlines()
            + ["FIM"]
        )
        saida = io.StringIO()
        with patch("builtins.input", side_effect=linhas):
            with redirect_stdout(saida):
                main()
        texto = saida.getvalue()
        self.assertIn("MATERIAL CORRETO", texto)
        self.assertIn("MATERIAL INCORRETO", texto)
        self.assertIn("Perguntas válidas: 5", texto)
        self.assertIn("Flashcards válidos: 3", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
