# ============================================================
# AGENTE 1 - EXTRATOR DE CONCEITOS
# ============================================================

# Importamos o módulo re (regular expressions).
# Este módulo permite procurar e dividir texto usando padrões.
import re


def extrair_conceitos(texto):
    """
    Recebe um texto de estudo e extrai frases que possam
    representar conceitos, definições ou informação importante.

    Parâmetro:
        texto -> material de estudo introduzido pelo utilizador

    Retorno:
        lista_conceitos -> lista de frases consideradas relevantes
    """

    # --------------------------------------------------------
    # 1. VALIDAR O TEXTO RECEBIDO
    # --------------------------------------------------------

    # Verificamos se o texto está vazio ou contém apenas espaços.
    # Se não existir conteúdo, não há nada que possamos analisar.
    if not texto or texto.strip() == "":
        return []

    # --------------------------------------------------------
    # 2. DIVIDIR O TEXTO EM FRASES
    # --------------------------------------------------------

    # Utilizamos uma expressão regular para dividir o texto
    # quando encontramos um ponto final, uma interrogação
    # ou um ponto de exclamação.
    #
    # Exemplo:
    # "Python é uma linguagem. É fácil de aprender!"
    #
    # Resultado:
    # ["Python é uma linguagem", "É fácil de aprender"]
    frases = re.split(r'[.!?]+', texto)

    # --------------------------------------------------------
    # 3. CRIAR A LISTA DE CONCEITOS
    # --------------------------------------------------------

    # Nesta lista vamos guardar as frases que forem consideradas
    # suficientemente relevantes para serem utilizadas pelo
    # agente seguinte.
    lista_conceitos = []

    # --------------------------------------------------------
    # 4. DEFINIR UM CONJUNTO PARA EVITAR DUPLICADOS
    # --------------------------------------------------------

    # O conjunto (set) permite verificar rapidamente se uma
    # frase já foi adicionada anteriormente.
    #
    # Guardamos uma versão em minúsculas para que, por exemplo,
    # "Python" e "python" sejam considerados iguais.
    conceitos_existentes = set()

    # --------------------------------------------------------
    # 5. ANALISAR CADA FRASE DO TEXTO
    # --------------------------------------------------------

    # Percorremos todas as frases obtidas anteriormente.
    for frase in frases:

        # Removemos espaços no início e no fim da frase.
        frase = frase.strip()

        # ----------------------------------------------------
        # 5.1 IGNORAR FRASES MUITO CURTAS
        # ----------------------------------------------------

        # Frases muito pequenas podem não conter informação útil.
        # Por isso, apenas consideramos frases com mais de
        # 15 caracteres.
        if len(frase) <= 15:
            continue

        # ----------------------------------------------------
        # 5.2 NORMALIZAR A FRASE
        # ----------------------------------------------------

        # Transformamos a frase em minúsculas para facilitar
        # a comparação e a deteção de frases repetidas.
        frase_normalizada = frase.lower()

        # ----------------------------------------------------
        # 5.3 VERIFICAR SE A FRASE JÁ EXISTE
        # ----------------------------------------------------

        # Se a frase já tiver sido encontrada, não a adicionamos
        # novamente à lista.
        if frase_normalizada in conceitos_existentes:
            continue

        # ----------------------------------------------------
        # 5.4 GUARDAR O CONCEITO
        # ----------------------------------------------------

        # Se a frase passou pelas verificações anteriores,
        # consideramos que pode ser relevante para o estudo.
        lista_conceitos.append(frase)

        # Guardamos também a versão normalizada no set.
        # Isto permite detetar duplicados nas próximas frases.
        conceitos_existentes.add(frase_normalizada)

    # --------------------------------------------------------
    # 6. DEVOLVER OS CONCEITOS EXTRAÍDOS
    # --------------------------------------------------------

    # O agente devolve a lista ao programa principal.
    # O programa principal poderá posteriormente entregar
    # esta lista ao Agente 2.
    return lista_conceitos
