# Controle de Estoque - Programação Dinâmica

## Descrição

Este projeto foi desenvolvido como parte do desafio DASA/Challenge para a disciplina de Algoritmos e Estruturas de Dados da FIAP. O objetivo é implementar um sistema de controle de estoque utilizando dicionários e listas aninhados, além de técnicas de programação dinâmica (memoização).

## Integrantes

- 558488 Anthony Motobe
- 555342 Arthur Rodrigues
- 554743 Guilherme Abe
- 554779 Gustavo Paulino
- 558017 Victor Dias

Turma: 2ESR-2025

## Objetivo

O sistema permite:
- Cadastrar novos estoques e insumos.
- Visualizar todos os estoques e seus itens.
- Identificar produtos em falta ou em excesso.
- Redistribuir itens entre estoques para equilibrar os níveis.
- Demonstrar automaticamente as principais funcionalidades.

## Estrutura dos Dados

O estoque é representado por um dicionário aninhado, onde:
- A chave principal é o nome do estoque.
- Cada estoque possui insumos (produtos) como chaves, com valores atuais e ideais.

Exemplo:
```python
stock = {
    "Almoxarifado A": {
        "luvas": {"current": 120, "ideal": 150},
        "máscaras": {"current": 60, "ideal": 100},
        "álcool": {"current": 80, "ideal": 80}
    },
    ...
}
```

## Técnicas Utilizadas

- **Memoização (Programação Dinâmica):**  
  A função `calculate_diff` utiliza um dicionário para armazenar diferenças já calculadas, evitando cálculos repetidos.

- **Funções Modulares:**  
  O código é dividido em funções para facilitar manutenção e entendimento.

## Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Baixe/clique no arquivo `challenge.py`.
3. Execute no terminal:
   ```
   python challenge.py
   ```
4. Siga o menu interativo para utilizar as funcionalidades.

## Funcionalidades

- **Verificar estoques:** Exibe todos os estoques e seus itens.
- **Cadastrar estoque:** Permite adicionar um novo estoque.
- **Cadastrar produtos:** Adiciona ou atualiza itens em um estoque.
- **Ver produtos em falta:** Lista itens abaixo do ideal.
- **Ver produtos em excesso:** Lista itens acima do ideal.
- **Redistribuir estoques:** Sugere e aplica redistribuição de itens.
- **Demonstração automática:** Executa todas as funções principais automaticamente.

## Hipóteses e Dados Considerados

- Os estoques e insumos são exemplos fictícios, podendo ser alterados conforme a necessidade.
- O valor ideal de cada insumo deve ser definido pelo usuário ou pelo sistema.
- O sistema não faz controle de usuários ou permissões.

## Referências

- Material didático FIAP - Algoritmos e Estruturas de Dados
- Documentação oficial do Python

## Observações

- O código está documentado com docstrings em todas as funções.
- Para dúvidas ou sugestões, consulte os integrantes do grupo.

---