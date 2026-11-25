
# ============================================================
# AGENTE 3 - REVISOR PEDAGÓGICO
# ============================================================

def rever_perguntas(perguntas_mcq, flashcards, texto_original):
    """
    Recebe as perguntas MCQ, os flashcards e o material original.

    O agente verifica:
        - Estrutura das perguntas;
        - Existência das quatro opções;
        - Validade da resposta correta;
        - Presença do conceito no material original;
        - Estrutura dos flashcards;
        - Existência da pergunta e resposta dos flashcards.

    Retorna:
        Um dicionário com:
            - perguntas_validas
            - perguntas_rejeitadas
            - flashcards_validos
            - flashcards_rejeitados
    """

    # --------------------------------------------------------
    # 1. PREPARAR AS LISTAS DE RESULTADOS
    # --------------------------------------------------------

    # Nesta lista serão guardadas as perguntas que passaram
    # em todas as verificações realizadas.
    perguntas_validas = []

    # Nesta lista guardamos as perguntas que falharam
    # em pelo menos uma das verificações.
    perguntas_rejeitadas = []

    # Lista para guardar os flashcards aprovados.
    flashcards_validos = []

    # Lista para guardar os flashcards rejeitados.
    flashcards_rejeitados = []

    # --------------------------------------------------------
    # 2. NORMALIZAR O TEXTO ORIGINAL
    # --------------------------------------------------------

    # Transformamos o texto original em minúsculas.
    # Isto permite fazer comparações sem distinguir
    # letras maiúsculas de letras minúsculas.
    texto_normalizado = texto_original.lower()

    # --------------------------------------------------------
    # 3. REVER AS PERGUNTAS DE ESCOLHA MÚLTIPLA
    # --------------------------------------------------------

    # Percorremos todas as perguntas recebidas do Agente 2.
    for pergunta in perguntas_mcq:

        # Criamos uma lista para guardar os problemas
        # encontrados nesta pergunta.
        problemas = []

        # ----------------------------------------------------
        # 3.1 VERIFICAR SE EXISTE TEXTO DA PERGUNTA
        # ----------------------------------------------------

        # Tentamos obter o texto da pergunta.
        # Se a chave não existir, devolvemos uma string vazia.
        texto_pergunta = pergunta.get("pergunta", "")

        # Verificamos se a pergunta está vazia.
        if not texto_pergunta.strip():

            # Registamos o problema encontrado.
            problemas.append(
                "A pergunta não possui texto."
            )

        # ----------------------------------------------------
        # 3.2 VERIFICAR AS OPÇÕES DE RESPOSTA
        # ----------------------------------------------------

        # Tentamos obter o dicionário de opções.
        # Se não existir, utilizamos um dicionário vazio.
        opcoes = pergunta.get("opcoes", {})

        # Definimos as letras esperadas.
        letras_esperadas = ["A", "B", "C", "D"]

        # Verificamos se existem exatamente quatro opções
        # e se estão identificadas corretamente.
        if list(opcoes.keys()) != letras_esperadas:

            # Registamos o problema.
            problemas.append(
                "As opções não estão organizadas corretamente "
                "em A, B, C e D."
            )

        # ----------------------------------------------------
        # 3.3 VERIFICAR SE EXISTE RESPOSTA CORRETA
        # ----------------------------------------------------

        # Obtemos a letra da resposta correta.
        resposta_correta = pergunta.get(
            "resposta_correta",
            ""
        )

        # Verificamos se a resposta correta corresponde
        # a uma das letras disponíveis.
        if resposta_correta not in letras_esperadas:

            # Registamos o problema.
            problemas.append(
                "A resposta correta não é válida."
            )

        # ----------------------------------------------------
        # 3.4 VERIFICAR SE A RESPOSTA EXISTE NAS OPÇÕES
        # ----------------------------------------------------

        # Apenas realizamos esta verificação se a letra
        # da resposta correta for válida.
        if resposta_correta in opcoes:

            # Obtém o texto associado à resposta correta.
            texto_resposta = opcoes[resposta_correta]

            # Verificamos se o texto da resposta existe.
            if not texto_resposta.strip():

                # Registamos o problema.
                problemas.append(
                    "A opção correta está vazia."
                )

        # ----------------------------------------------------
        # 3.5 VERIFICAR O CONCEITO ORIGINAL
        # ----------------------------------------------------

        # O Agente 2 guarda o conceito utilizado
        # para construir a pergunta.
        conceito_original = pergunta.get(
            "conceito_original",
            ""
        )

        # Verificamos se o conceito foi guardado.
        if not conceito_original:

            # Registamos o problema.
            problemas.append(
                "A pergunta não possui conceito original."
            )

        # Caso exista um conceito, verificamos se aparece
        # no material original.
        elif conceito_original.lower() not in texto_normalizado:

            # Registamos o problema.
            problemas.append(
                "O conceito utilizado não foi encontrado "
                "no material original."
            )

        # ----------------------------------------------------
        # 3.6 VERIFICAR SE A RESPOSTA CORRETA
        #       CORRESPONDE AO CONCEITO ORIGINAL
        # ----------------------------------------------------

        # Só fazemos esta verificação se:
        # - a letra da resposta estiver válida;
        # - o conceito original existir.
        if (
            resposta_correta in opcoes
            and conceito_original
        ):

            # Obtém o texto da opção correta.
            texto_resposta = opcoes[resposta_correta]

            # Comparamos a resposta com o conceito original.
            if texto_resposta != conceito_original:

                # Registamos o problema.
                problemas.append(
                    "A opção identificada como correta "
                    "não corresponde ao conceito original."
                )

        # ----------------------------------------------------
        # 3.7 DECIDIR SE A PERGUNTA É VÁLIDA
        # ----------------------------------------------------

        # Se não foram encontrados problemas,
        # consideramos a pergunta válida.
        if not problemas:

            # Adicionamos uma explicação ao resultado.
            pergunta["revisao"] = (
                "Pergunta validada pelo revisor pedagógico."
            )

            # Guardamos a pergunta na lista de aprovadas.
            perguntas_validas.append(pergunta)

        else:

            # Se existiram problemas, guardamos a lista
            # de problemas encontrados dentro da pergunta.
            pergunta["problemas"] = problemas

            # Guardamos a pergunta rejeitada.
            perguntas_rejeitadas.append(pergunta)

    # --------------------------------------------------------
    # 4. REVER OS FLASHCARDS
    # --------------------------------------------------------

    # Percorremos todos os flashcards recebidos.
    for flashcard in flashcards:

        # Criamos uma lista de problemas para o cartão.
        problemas = []

        # ----------------------------------------------------
        # 4.1 VERIFICAR A PERGUNTA DO FLASHCARD
        # ----------------------------------------------------

        # Obtemos o texto da pergunta.
        pergunta_flashcard = flashcard.get(
            "pergunta",
            ""
        )

        # Verificamos se está vazio.
        if not pergunta_flashcard.strip():

            # Registamos o problema.
            problemas.append(
                "O flashcard não possui pergunta."
            )

        # ----------------------------------------------------
        # 4.2 VERIFICAR A RESPOSTA
        # ----------------------------------------------------

        # Obtemos a resposta do flashcard.
        resposta_flashcard = flashcard.get(
            "resposta",
            ""
        )

        # Verificamos se existe resposta.
        if not resposta_flashcard.strip():

            # Registamos o problema.
            problemas.append(
                "O flashcard não possui resposta."
            )

        # ----------------------------------------------------
        # 4.3 VERIFICAR O CONCEITO ORIGINAL
        # ----------------------------------------------------

        # Obtemos o conceito que serviu de base ao cartão.
        conceito_original = flashcard.get(
            "conceito_original",
            ""
        )

        # Verificamos se o conceito existe.
        if not conceito_original:

            # Registamos o problema.
            problemas.append(
                "O flashcard não possui conceito original."
            )

        # ----------------------------------------------------
        # 4.4 VERIFICAR SE O CONCEITO
        #       EXISTE NO MATERIAL ORIGINAL
        # ----------------------------------------------------

        # Caso exista um conceito, verificamos se aparece
        # no material de estudo.
        elif conceito_original.lower() not in texto_normalizado:

            # Registamos o problema.
            problemas.append(
                "O conceito do flashcard não foi encontrado "
                "no material original."
            )

        # ----------------------------------------------------
        # 4.5 VERIFICAR SE A RESPOSTA
        #       CORRESPONDE AO CONCEITO
        # ----------------------------------------------------

        # Se existe uma resposta e um conceito,
        # comparamos ambos.
        if resposta_flashcard and conceito_original:

            # Verificamos se a resposta corresponde
            # ao conceito original.
            if resposta_flashcard != conceito_original:

                # Registamos o problema.
                problemas.append(
                    "A resposta do flashcard não corresponde "
                    "ao conceito original."
                )

        # ----------------------------------------------------
        # 4.6 DECIDIR SE O FLASHCARD É VÁLIDO
        # ----------------------------------------------------

        # Se não foram encontrados problemas,
        # consideramos o flashcard válido.
        if not problemas:

            # Adicionamos uma explicação de validação.
            flashcard["revisao"] = (
                "Flashcard validado pelo revisor pedagógico."
            )

            # Guardamos o cartão aprovado.
            flashcards_validos.append(flashcard)

        else:

            # Guardamos os problemas encontrados.
            flashcard["problemas"] = problemas

            # Guardamos o cartão rejeitado.
            flashcards_rejeitados.append(flashcard)

    # --------------------------------------------------------
    # 5. DEVOLVER TODOS OS RESULTADOS
    # --------------------------------------------------------

    # Devolvemos os materiais separados por estado.
    # O programa principal poderá mostrar os aprovados
    # e explicar os rejeitados.
    return {
        "perguntas_validas": perguntas_validas,
        "perguntas_rejeitadas": perguntas_rejeitadas,
        "flashcards_validos": flashcards_validos,
        "flashcards_rejeitados": flashcards_rejeitados
    }
