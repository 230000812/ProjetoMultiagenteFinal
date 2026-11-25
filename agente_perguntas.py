# ============================================================
# AGENTE 2 - CRIADOR DE PERGUNTAS
# ============================================================

# Importamos sample para selecionar elementos aleatórios sem repetir
# elementos dentro da mesma seleção.
from random import sample
import re


# Quantidades de materiais a criar.
NUMERO_PERGUNTAS = 5
NUMERO_FLASHCARDS = 3


def _limpar_conceitos(conceitos):
    """Remove entradas vazias e duplicadas, mantendo a ordem original."""

    conceitos_limpos = []
    conceitos_existentes = set()

    if not isinstance(conceitos, (list, tuple)):
        return conceitos_limpos

    for conceito in conceitos:
        if not isinstance(conceito, str):
            continue

        # Normalizamos espaços sem alterar o conteúdo da afirmação.
        conceito = re.sub(r"\s+", " ", conceito).strip()

        if not conceito:
            continue

        chave = conceito.casefold()

        if chave not in conceitos_existentes:
            conceitos_limpos.append(conceito)
            conceitos_existentes.add(chave)

    return conceitos_limpos


def criar_perguntas(conceitos_corretos, conceitos_incorretos):
    """
    Recebe duas listas distintas preparadas pelo Agente 1:

        conceitos_corretos:
            Afirmações que o utilizador identificou como corretas.

        conceitos_incorretos:
            Afirmações que o utilizador identificou como incorretas.

    Para cada pergunta de escolha múltipla, o Agente 2 seleciona:
        - uma afirmação da lista de conceitos corretos;
        - três afirmações da lista de conceitos incorretos.

    Não classifica nem inventa afirmações. A classificação é feita
    previamente pelo utilizador, ao introduzir os dois materiais
    separadamente na main.

    Os flashcards são criados apenas a partir dos conceitos corretos.
    """

    # --------------------------------------------------------
    # 1. PREPARAR AS DUAS LISTAS RECEBIDAS
    # --------------------------------------------------------

    conceitos_corretos = _limpar_conceitos(conceitos_corretos)
    conceitos_incorretos = _limpar_conceitos(conceitos_incorretos)

    # Evitamos que uma afirmação exatamente igual seja usada como
    # correta e incorreta ao mesmo tempo.
    corretos_normalizados = {
        conceito.casefold() for conceito in conceitos_corretos
    }

    conceitos_incorretos = [
        conceito
        for conceito in conceitos_incorretos
        if conceito.casefold() not in corretos_normalizados
    ]

    # Listas onde serão guardados os resultados.
    perguntas_mcq = []
    flashcards = []
    avisos = []

    if not conceitos_corretos:
        return {
            "perguntas_mcq": [],
            "flashcards": [],
            "avisos": [
                "Não existem afirmações no material classificado como correto."
            ],
        }

    # --------------------------------------------------------
    # 2. CRIAR AS PERGUNTAS DE ESCOLHA MÚLTIPLA
    # --------------------------------------------------------

    # São necessárias três afirmações incorretas diferentes para
    # completar as opções de cada pergunta sem inventar conteúdo.
    if len(conceitos_incorretos) < 3:
        avisos.append(
            "Não foram criadas perguntas de escolha múltipla. São necessárias "
            "pelo menos três afirmações distintas no material classificado "
            "como incorreto."
        )
    else:
        # Cada pergunta utiliza uma afirmação correta diferente.
        quantidade_perguntas = min(
            NUMERO_PERGUNTAS,
            len(conceitos_corretos),
        )

        conceitos_escolhidos = sample(
            conceitos_corretos,
            quantidade_perguntas,
        )

        enunciados = [
            "Qual das seguintes afirmações está correta?",
            "Seleciona a afirmação verdadeira de acordo com o material fornecido.",
            "Qual destas opções apresenta informação correta?",
            "Identifica a opção que corresponde ao material classificado como correto.",
            "Com base nos apontamentos, qual é a afirmação correta?",
        ]

        for indice, conceito_correto in enumerate(conceitos_escolhidos):

            # Selecionamos obrigatoriamente três afirmações da lista
            # que o utilizador classificou como incorreta.
            tres_incorretos = sample(conceitos_incorretos, 3)

            # Criamos os quatro elementos da pergunta.
            opcoes_temporarias = [
                {"texto": conceito_correto, "tipo": "correta"}
            ]

            for conceito_incorreto in tres_incorretos:
                opcoes_temporarias.append({
                    "texto": conceito_incorreto,
                    "tipo": "incorreta",
                })

            # Baralhamos para a opção correta não ficar sempre na mesma letra.
            opcoes_temporarias = sample(
                opcoes_temporarias,
                len(opcoes_temporarias),
            )

            opcoes = {}
            resposta_correta = ""

            letras = ["A", "B", "C", "D"]

            for letra, opcao in zip(letras, opcoes_temporarias):
                opcoes[letra] = opcao["texto"]

                if opcao["tipo"] == "correta":
                    resposta_correta = letra

            # Guardamos a pergunta no formato utilizado pelo Agente 3.
            pergunta = {
                "pergunta": enunciados[indice % len(enunciados)],
                "opcoes": opcoes,
                "resposta_correta": resposta_correta,
                "conceito_original": conceito_correto,
            }

            perguntas_mcq.append(pergunta)

        if quantidade_perguntas < NUMERO_PERGUNTAS:
            avisos.append(
                f"Foram criadas {quantidade_perguntas} perguntas em vez de 5, "
                "porque não existem cinco afirmações corretas distintas."
            )

    # --------------------------------------------------------
    # 3. CRIAR OS FLASHCARDS
    # --------------------------------------------------------

    # Os flashcards utilizam apenas afirmações do material correto.
    quantidade_flashcards = min(
        NUMERO_FLASHCARDS,
        len(conceitos_corretos),
    )

    conceitos_flashcards = sample(
        conceitos_corretos,
        quantidade_flashcards,
    )

    for indice, conceito in enumerate(conceitos_flashcards, start=1):
        flashcard = {
            "pergunta": f"Flashcard {indice}: o que deves recordar sobre este conteúdo?",
            "resposta": conceito,
            "conceito_original": conceito,
        }

        flashcards.append(flashcard)

    if quantidade_flashcards < NUMERO_FLASHCARDS:
        avisos.append(
            f"Foram criados {quantidade_flashcards} flashcards em vez de 3, "
            "porque não existem três afirmações corretas distintas."
        )

    # --------------------------------------------------------
    # 4. DEVOLVER OS RESULTADOS À MAIN
    # --------------------------------------------------------

    return {
        "perguntas_mcq": perguntas_mcq,
        "flashcards": flashcards,
        "avisos": avisos,
    }
