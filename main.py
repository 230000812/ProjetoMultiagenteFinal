# ============================================================
# SISTEMA MULTIAGENTE
# GERADOR AUTOMÁTICO DE TESTES E CARTÕES DE ESTUDO
# ============================================================

# A main importa apenas as funções necessárias de cada agente.
# A lógica interna de cada agente permanece no seu próprio ficheiro.

from agente_extrator import extrair_conceitos
from agente_perguntas import criar_perguntas
from agente_revisor import rever_perguntas


# ============================================================
# FUNÇÃO RECURSIVA PARA RECEBER O MATERIAL
# ============================================================

def receber_material(linhas=None):

    # Na primeira chamada, criamos uma lista vazia.
    if linhas is None:
        linhas = []

    # Pedimos uma nova linha de material ao utilizador.
    linha = input()

    # Caso base da recursividade: quando o utilizador escreve FIM.
    if linha.strip().upper() == "FIM":
        return "\n".join(linhas)

    # Caso recursivo: adicionamos a linha e pedimos a seguinte.
    linhas.append(linha)
    return receber_material(linhas)


# ============================================================
# PREPARAR O TEXTO PARA O AGENTE 1
# ============================================================

def preparar_material(texto):
    """
    O Agente 1 original divide o material por pontuação.
    Esta função permite também que o utilizador escreva uma
    afirmação por linha, sem alterar a estrutura do Agente 1.
    """

    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    return ". ".join(linhas)


# ============================================================
# FUNÇÃO PARA APRESENTAR UMA LISTA
# ============================================================

def apresentar_lista(lista, numero=0):

    # Caso base: já percorremos todos os elementos.
    if numero >= len(lista):
        return

    print(f"{numero + 1}. {lista[numero]}")

    # Chamada recursiva para apresentar o elemento seguinte.
    apresentar_lista(lista, numero + 1)


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("GERADOR AUTOMÁTICO DE TESTES E CARTÕES DE ESTUDO")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. RECEBER O MATERIAL CORRETO E O MATERIAL INCORRETO
    # --------------------------------------------------------

    print("\nMATERIAL CORRETO")
    print("Introduza apenas afirmações que considera corretas.")
    print("Pode escrever uma afirmação por linha.")
    print("Quando terminar, escreva FIM numa linha isolada.\n")

    texto_material_correto = receber_material()

    if not texto_material_correto.strip():
        print("\nERRO: Não foi introduzido material correto.")
        return

    print("\nMATERIAL INCORRETO")
    print("Introduza apenas afirmações que considera incorretas.")
    print("Estas afirmações serão usadas como opções erradas.")
    print("Pode escrever uma afirmação por linha.")
    print("Quando terminar, escreva FIM numa linha isolada.\n")

    texto_material_incorreto = receber_material()

    if not texto_material_incorreto.strip():
        print("\nAVISO: Não foi introduzido material incorreto.")
        print("Não será possível criar perguntas de escolha múltipla.")

    print("\nMateriais recebidos. A classificação foi definida por si.")

    # --------------------------------------------------------
    # AGENTE 1 - EXTRATOR DE CONCEITOS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("AGENTE 1 - EXTRATOR DE CONCEITOS")
    print("=" * 60)

    try:
        # O mesmo Agente 1 é chamado separadamente para cada material.
        # A função do Agente 1 mantém a sua assinatura original.
        conceitos_corretos = extrair_conceitos(
            preparar_material(texto_material_correto)
        )

        conceitos_incorretos = extrair_conceitos(
            preparar_material(texto_material_incorreto)
        )

        print("\nConceitos extraídos do material correto:")
        apresentar_lista(conceitos_corretos)

        print("\nConceitos extraídos do material incorreto:")
        if conceitos_incorretos:
            apresentar_lista(conceitos_incorretos)
        else:
            print("Não foram identificadas afirmações incorretas.")

        if not conceitos_corretos:
            print("\nERRO: Não foram extraídos conceitos corretos.")
            return

        print("\n[COMUNICAÇÃO]")
        print("Agente 1 -> Agente 2")
        print("As duas listas foram enviadas separadamente.")

    except Exception as erro:
        print("\nERRO no Agente 1:")
        print(erro)
        return

    # --------------------------------------------------------
    # AGENTE 2 - CRIADOR DE PERGUNTAS E FLASHCARDS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("AGENTE 2 - CRIADOR DE PERGUNTAS")
    print("=" * 60)

    try:
        # O Agente 2 recebe as duas listas que o utilizador classificou:
        # - conceitos_corretos: fornece a única opção correta;
        # - conceitos_incorretos: fornece as três opções erradas.
        resultado_agente2 = criar_perguntas(
            conceitos_corretos,
            conceitos_incorretos,
        )

        perguntas_mcq = resultado_agente2.get("perguntas_mcq", [])
        flashcards = resultado_agente2.get("flashcards", [])

        for aviso in resultado_agente2.get("avisos", []):
            print("\nAVISO:", aviso)

        print("\nPerguntas de escolha múltipla geradas:", len(perguntas_mcq))
        print("Flashcards gerados:", len(flashcards))

        print("\n[COMUNICAÇÃO]")
        print("Agente 2 -> Agente 3")
        print("Perguntas e flashcards enviados para revisão.")

    except Exception as erro:
        print("\nERRO no Agente 2:")
        print(erro)
        return

    # --------------------------------------------------------
    # AGENTE 3 - REVISOR PEDAGÓGICO
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("AGENTE 3 - REVISOR PEDAGÓGICO")
    print("=" * 60)

    try:
        # O Agente 3 mantém a assinatura original.
        # Valida os materiais gerados usando o material correto.
        resultado_agente3 = rever_perguntas(
            perguntas_mcq,
            flashcards,
            texto_material_correto,
        )

        perguntas_validas = resultado_agente3.get("perguntas_validas", [])
        perguntas_rejeitadas = resultado_agente3.get("perguntas_rejeitadas", [])
        flashcards_validos = resultado_agente3.get("flashcards_validos", [])
        flashcards_rejeitados = resultado_agente3.get("flashcards_rejeitados", [])

        # ----------------------------------------------------
        # APRESENTAR PERGUNTAS VÁLIDAS
        # ----------------------------------------------------

        print("\n===== PERGUNTAS VÁLIDAS =====")

        if not perguntas_validas:
            print("Não existem perguntas aprovadas pelo revisor.")

        for numero, pergunta in enumerate(perguntas_validas, start=1):
            print(f"\nPergunta {numero}:")
            print(pergunta.get("pergunta", ""))

            for letra, opcao in pergunta.get("opcoes", {}).items():
                print(f"{letra}) {opcao}")

            print("Resposta correta:", pergunta.get("resposta_correta", ""))
            print("Revisão:", pergunta.get("revisao", ""))

        # ----------------------------------------------------
        # APRESENTAR PERGUNTAS REJEITADAS
        # ----------------------------------------------------

        print("\n===== PERGUNTAS REJEITADAS =====")

        if not perguntas_rejeitadas:
            print("Não foram encontradas perguntas rejeitadas.")

        for numero, pergunta in enumerate(perguntas_rejeitadas, start=1):
            print(f"\nPergunta rejeitada {numero}:")
            print(pergunta.get("pergunta", ""))
            print("Problemas:")

            for problema in pergunta.get("problemas", []):
                print("-", problema)

        # ----------------------------------------------------
        # APRESENTAR FLASHCARDS VÁLIDOS E REJEITADOS
        # ----------------------------------------------------

        print("\n===== FLASHCARDS VÁLIDOS =====")

        if not flashcards_validos:
            print("Não existem flashcards aprovados pelo revisor.")

        for numero, flashcard in enumerate(flashcards_validos, start=1):
            print(f"\nFlashcard {numero}:")
            print("Pergunta:", flashcard.get("pergunta", ""))
            print("Resposta:", flashcard.get("resposta", ""))
            print("Revisão:", flashcard.get("revisao", ""))

        print("\n===== FLASHCARDS REJEITADOS =====")

        if not flashcards_rejeitados:
            print("Não foram encontrados flashcards rejeitados.")

        for numero, flashcard in enumerate(flashcards_rejeitados, start=1):
            print(f"\nFlashcard rejeitado {numero}:")
            print("Pergunta:", flashcard.get("pergunta", ""))

            for problema in flashcard.get("problemas", []):
                print("-", problema)

        print("\n[COMUNICAÇÃO]")
        print("Agente 3 -> Main")
        print("Resultados da revisão devolvidos à main.")

    except Exception as erro:
        print("\nERRO no Agente 3:")
        print(erro)
        return

    # --------------------------------------------------------
    # RESUMO FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("RESUMO FINAL DO SISTEMA")
    print("=" * 60)
    print("Conceitos corretos extraídos:", len(conceitos_corretos))
    print("Conceitos incorretos extraídos:", len(conceitos_incorretos))
    print("Perguntas geradas:", len(perguntas_mcq))
    print("Perguntas válidas:", len(perguntas_validas))
    print("Perguntas rejeitadas:", len(perguntas_rejeitadas))
    print("Flashcards gerados:", len(flashcards))
    print("Flashcards válidos:", len(flashcards_validos))
    print("Flashcards rejeitados:", len(flashcards_rejeitados))
    print("\n" + "=" * 60)
    print("SISTEMA MULTIAGENTE CONCLUÍDO")
    print("=" * 60)


# ============================================================
# EXECUÇÃO DO PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()
