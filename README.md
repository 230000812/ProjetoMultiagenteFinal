# Gerador Automático de Testes e Cartões de Estudo

Sistema multiagente em Python que recebe dois blocos de texto classificados pelo utilizador: material correto e material incorreto. O Agente 2 cria perguntas de escolha múltipla usando exatamente uma afirmação do material correto e três afirmações do material incorreto.

## Estrutura

- `main.py` — recebe separadamente os dois materiais, coordena os agentes e apresenta os resultados. Mantém funções recursivas para receber e apresentar informação.
- `agente_extrator.py` — Agente 1. Mantém a função original `extrair_conceitos(texto)`. A main chama-a duas vezes, uma por cada material.
- `agente_perguntas.py` — Agente 2. Recebe `criar_perguntas(conceitos_corretos, conceitos_incorretos)` e seleciona uma afirmação correta e três incorretas para cada pergunta.
- `agente_revisor.py` — Agente 3. Mantém a função original `rever_perguntas(perguntas_mcq, flashcards, texto_original)`.
- `testes_projeto.py` — testes automáticos.
- `requirements.txt` — dependências externas (nenhuma).

## Como executar

Requer Python 3.10 ou superior. Não são necessárias bibliotecas externas.

```bash
python main.py
```

A aplicação pede primeiro o **MATERIAL CORRETO** e depois o **MATERIAL INCORRETO**. É o utilizador que decide em que grupo coloca cada afirmação. Introduza uma afirmação por linha e escreva `FIM` numa linha isolada para terminar cada bloco.

O programa passa cada bloco separadamente ao Agente 1. Depois, envia as duas listas ao Agente 2. O Agente 2 não decide o que é verdadeiro ou falso: escolhe uma afirmação da lista correta e três da lista incorreta. Os flashcards são feitos apenas com o material correto.

## Testes

```bash
python -m unittest -v testes_projeto.py
```

## Regras da geração de perguntas

- Cada pergunta tem quatro opções distintas.
- Exatamente uma opção é retirada do material correto.
- Exatamente três opções são retiradas do material incorreto.
- São necessárias pelo menos três afirmações incorretas distintas para criar perguntas.
- São criadas até cinco perguntas, conforme o número de afirmações corretas distintas.
- São criados até três flashcards com afirmações do material correto.
- O sistema não inventa opções erradas para preencher lacunas. Se o material incorreto tiver menos de três afirmações distintas, as perguntas MCQ não são criadas e é apresentado um aviso.

## Nota sobre a estrutura dos agentes

O Agente 1 e o Agente 3 mantêm os ficheiros, nomes e assinaturas originais. O Agente 1 é chamado duas vezes pela main. A alteração funcional necessária está no Agente 2, que passa a receber duas listas. A main continua a ser apenas o coordenador do pipeline.

## Limitações

A classificação de cada afirmação é feita pelo utilizador. O Agente 2 respeita essa classificação, mas não verifica por conhecimento próprio se a informação é factualmente verdadeira. O Agente 3 original confirma a estrutura e a presença da resposta correta no material correto; não faz uma validação semântica das três opções erradas.
