<a id="readme-top"></a>

[![Python][python-shield]][python-url]
[![LangChain][langchain-shield]][langchain-url]
[![OpenAI][openai-shield]][openai-url]
[![Issues][issues-shield]][issues-url]
[![Project][project-shield]][project-url]
[![MIT License][license-shield]][license-url]

<br />
<div align="center">
  <h1>Pokechat AI</h1>

  <p>
    Pokédex conversacional com RAG, fundamentada em dados históricos de Pokémon Red, Blue e Yellow.
    <br />
    <a href="https://github.com/JonathanBufon/pokechat-ai/issues/1"><strong>Explorar o roadmap</strong></a>
    <br />
    <br />
    <a href="https://github.com/users/JonathanBufon/projects/1">Ver backlog</a>
    &middot;
    <a href="https://github.com/JonathanBufon/pokechat-ai/issues">Ver issues</a>
    &middot;
    <a href="https://github.com/JonathanBufon/pokechat-ai/issues/new?labels=bug">Reportar problema</a>
  </p>
</div>

<details>
  <summary>Sumário</summary>
  <ol>
    <li><a href="#sobre-o-projeto">Sobre o projeto</a></li>
    <li><a href="#objetivos-de-aprendizado">Objetivos de aprendizado</a></li>
    <li><a href="#escopo-do-mvp">Escopo do MVP</a></li>
    <li><a href="#arquitetura">Arquitetura</a></li>
    <li><a href="#fontes-de-dados">Fontes de dados</a></li>
    <li><a href="#modelagem-do-conhecimento">Modelagem do conhecimento</a></li>
    <li><a href="#stack">Stack</a></li>
    <li><a href="#organizacao-do-projeto">Organização do projeto</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#estado-atual">Estado atual</a></li>
    <li><a href="#licenca">Licença</a></li>
    <li><a href="#referencias-e-creditos">Referências e créditos</a></li>
  </ol>
</details>

## Sobre o projeto

O **Pokechat AI** será uma Pokédex conversacional em português capaz de responder perguntas factuais sobre os 151 Pokémon presentes nos jogos originais **Pokémon Red, Blue e Yellow**.

O projeto usa **Retrieval-Augmented Generation (RAG)**. Em vez de pedir que um modelo de linguagem responda apenas com o conhecimento aprendido durante o treinamento, o sistema recupera documentos relevantes de uma base vetorial e os fornece como contexto para a resposta. Isso permite inspecionar as evidências utilizadas e reduzir respostas sem fundamento.

O domínio Pokémon foi escolhido por ser conhecido e fácil de explorar, mas a arquitetura representa problemas reais de recuperação de conhecimento, como documentação técnica, bases corporativas e suporte a produtos.

Este é um projeto didático. A implementação será feita em pequenas etapas, com cada decisão explicada, testada e revisada antes do avanço do backlog.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Objetivos de aprendizado

Ao concluir o MVP, o projeto terá exercitado o pipeline RAG completo:

1. Consumo resiliente de uma API REST pública.
2. Cache local e normalização de dados heterogêneos.
3. Modelagem de uma referência histórica versionada.
4. Transformação de registros estruturados em documentos textuais.
5. Geração de embeddings.
6. Persistência e busca por similaridade em um banco vetorial.
7. Augmentação de prompt com contexto recuperado.
8. Geração de respostas fundamentadas e acompanhadas de fontes.
9. Interface de chat com estado visual e tratamento de erros.
10. Testes e avaliação separada das etapas de retrieval e geração.

Apesar de usar componentes comuns em sistemas de agentes, o MVP não será um agente autônomo. O fluxo será determinístico e não incluirá seleção de ferramentas ou tomada autônoma de decisões.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Escopo do MVP

### O que o sistema deverá conhecer

- Os 151 Pokémon existentes em Red, Blue e Yellow.
- Número e nome na Pokédex.
- Tipos válidos na Geração I.
- Altura e peso.
- Os cinco atributos originais: HP, Ataque, Defesa, Especial e Velocidade.
- Descrições da Pokédex separadas por Red, Blue e Yellow.
- Cadeias e métodos de evolução existentes na época.
- Origem e versão dos dados usados em cada documento.

### O que o sistema deverá fazer

- Responder em português.
- Recuperar os documentos semanticamente mais relevantes para a pergunta.
- Comparar um pequeno conjunto de Pokémon quando o contexto recuperado for suficiente.
- Informar quando a base não trouxer evidência suficiente.
- Exibir os registros usados como fontes da resposta.
- Persistir o índice localmente e permitir reindexação sem duplicatas.

### Fora do escopo inicial

- Habilidades, introduzidas apenas na Geração III.
- Separação moderna entre Ataque Especial e Defesa Especial.
- Tipos e evoluções introduzidos depois da Geração I.
- Golpes, TMs, locais, itens, exclusividades entre versões e estratégia competitiva.
- Todas as gerações da franquia.
- Memória conversacional semântica, agentes, ferramentas e streaming.
- Autenticação, infraestrutura de produção e deploy.
- Garantia de listagens e contagens exaustivas.

Uma busca vetorial com `top_k` pequeno recupera os documentos semanticamente mais próximos, mas não equivale a uma consulta estruturada que percorre todos os registros. Por isso, perguntas como "liste todos os Pokémon do tipo Água" não fazem parte das garantias deste MVP.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Arquitetura

O sistema será dividido em duas fases independentes: **ingestão** e **consulta**.

### Ingestão

Executada para construir ou atualizar a base de conhecimento:

```text
PokéAPI                 Referência histórica da Geração I
   |                                  |
   +---------------+------------------+
                   |
                   v
          Coleta, cache e normalização
                   |
                   v
       Um documento textual por Pokémon
                   |
                   v
          OpenAI Embeddings em lote
                   |
                   v
        ChromaDB persistente e local
```

### Consulta

Executada a cada pergunta do usuário:

```text
Pergunta do usuário
        |
        v
Embedding da pergunta
        |
        v
Busca semântica top-k no ChromaDB
        |
        v
Documentos relevantes + metadados + scores
        |
        v
Prompt com contexto e regras de recusa
        |
        v
OpenAI Chat Model
        |
        v
Resposta em português + fontes
        |
        v
Interface Streamlit
```

### Responsabilidades

| Camada | Responsabilidade |
| --- | --- |
| Coleta | Consultar a PokéAPI com timeout, retry e cache local |
| Referência histórica | Corrigir tipos e atributos que a representação atual não preserva |
| Normalização | Combinar as fontes em um modelo canônico da Geração I |
| Documentos | Produzir texto legível e metadados rastreáveis por Pokémon |
| Ingestão | Gerar embeddings e manter uma coleção idempotente no ChromaDB |
| Retrieval | Recuperar documentos relevantes sem chamar o modelo de chat |
| RAG | Montar o contexto, aplicar regras de resposta e retornar fontes |
| Interface | Apresentar conversa, fontes e erros sem concentrar lógica de negócio |
| Avaliação | Medir retrieval e geração separadamente com perguntas de referência |

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Fontes de dados

### PokéAPI

A [PokéAPI][pokeapi-url] será a fonte primária para:

- Número, nome, altura e peso.
- Dados da espécie.
- Descrições em inglês das versões Red, Blue e Yellow.
- Referências para cadeias de evolução.
- JSONs brutos usados pelo pipeline de coleta.

As respostas serão armazenadas em cache local, em conformidade com a política de uso justo da API. Os dados atuais não serão aceitos automaticamente como representação histórica quando houver conflito com os jogos originais.

### Pokémon Showdown

O conjunto de dados da Geração I do [Pokémon Showdown][showdown-data-url] será usado como referência histórica para:

- Tipos existentes em Red, Blue e Yellow.
- HP, Ataque, Defesa, Especial e Velocidade originais.

Essa referência é necessária porque a forma atual de um Pokémon pode conter mudanças posteriores. Magnemite, por exemplo, era apenas do tipo Elétrico na Geração I, e o atributo Especial ainda não havia sido dividido em Ataque Especial e Defesa Especial.

O Pokémon Showdown é distribuído sob a [licença MIT][showdown-license-url]. A atribuição e os termos aplicáveis serão preservados junto da referência versionada.

### Regra de precedência

Quando houver conflito entre a representação atual da PokéAPI e os dados de Red/Blue/Yellow, a referência histórica versionada terá precedência. Evoluções também serão limitadas aos 151 Pokémon e aos métodos existentes na Geração I.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Modelagem do conhecimento

Cada Pokémon será representado internamente por um modelo canônico e convertido em **um documento coeso**. Não será necessário dividir cada registro em vários chunks, pois os dados são curtos e pertencem ao mesmo assunto.

Exemplo conceitual:

```text
Nome: Magnemite (#081)
Jogos: Pokémon Red, Blue e Yellow
Tipos na Geração I: Elétrico
Altura: 0,3 m
Peso: 6,0 kg
Atributos base: HP 25, Ataque 35, Defesa 70, Especial 95, Velocidade 45
Descrição em Red/Blue: ...
Descrição em Yellow: ...
Evolução: Magnemite -> Magneton (nível 30)
```

Metadados escalares serão salvos junto ao vetor para identificação e citação. Entre eles estarão o ID estável, número da Pokédex, nome, geração, jogos e proveniência.

O texto em linguagem natural participa da busca semântica. Os metadados permitem identificar, filtrar e exibir as fontes sem depender de o modelo de linguagem produzir citações corretamente.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Stack

| Tecnologia | Papel no projeto |
| --- | --- |
| [Python 3.11+][python-url] | Linguagem principal |
| [HTTPX][httpx-url] | Cliente HTTP para coleta com timeout e retry |
| [python-dotenv][dotenv-url] | Carregamento de configurações locais |
| [LangChain][langchain-url] | Composição do retriever, prompt e chain RAG |
| [OpenAI API][openai-url] | Embeddings e geração de respostas |
| [ChromaDB][chroma-url] | Banco vetorial persistente local |
| [Streamlit][streamlit-url] | Interface conversacional |
| [pytest][pytest-url] | Testes unitários e de integração controlada |
| [GitHub Issues][issues-url] | Especificação e critérios de aceite das tarefas |
| [GitHub Projects][project-url] | Backlog, fases, prioridades e fluxo de trabalho |

Modelos inicialmente planejados:

- Embeddings: `text-embedding-3-small`.
- Chat: `gpt-4o-mini`.
- Retrieval: busca por similaridade com `top_k` configurável, inicialmente `4`.

Os nomes dos modelos ficarão em variáveis de ambiente para permitir alteração sem espalhar configuração pelo código.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Organização do projeto

### Estrutura planejada

A estrutura definitiva será criada durante as primeiras issues. A organização inicial prevista é:

```text
pokechat-ai/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- src/
|   |-- ingest.py
|   |-- retriever.py
|   |-- chain.py
|   `-- app.py
|-- tests/
|-- data/
|   `-- raw/          # cache local, não versionado
`-- chroma_db/        # índice local, não versionado
```

Essa estrutura é uma direção inicial, não um contrato imutável. Novos módulos serão extraídos somente quando as responsabilidades implementadas justificarem a separação.

### Backlog

O trabalho está organizado no [GitHub Project "Pokechat AI - MVP"][project-url], que contém as 25 issues do projeto.

Fluxo dos itens:

```text
Backlog -> Ready -> In Progress -> In Review -> Done
```

Campos de organização:

- **Fase:** posição da tarefa na arquitetura e no aprendizado.
- **Prioridade:** `P0 - Agora`, `P1 - Essencial` ou `P2 - Melhoria`.
- **Ordem:** sequência pedagógica de execução.
- **Status:** estado atual no fluxo de trabalho.

Cada issue descreve contexto, objetivo pedagógico, tarefas, critérios de aceite, validação, dependências e uma pergunta de verificação. Apenas uma tarefa de implementação deve permanecer em `In Progress` por vez.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Roadmap

O roadmap completo está na [issue #1][roadmap-url]. As fases planejadas são:

- [ ] **Fundação:** ambiente Python, configurações e estrutura de testes.
- [ ] **Dados históricos:** coleta, cache, modelo canônico, descrições, tipos, atributos e evoluções.
- [ ] **Documentos e indexação:** documentos textuais, embeddings e ingestão idempotente.
- [ ] **Retrieval:** busca semântica e diagnóstico dos resultados.
- [ ] **Geração RAG:** prompt fundamentado, regras de recusa, respostas e fontes.
- [ ] **Interface:** chat Streamlit, histórico visual e tratamento de erros.
- [ ] **Qualidade e conclusão:** avaliação, documentação e registro das limitações.

### Definição de pronto do MVP

- O índice local contém exatamente 151 registros únicos.
- A reexecução da ingestão não cria duplicatas.
- Casos históricos críticos possuem testes sem chamadas externas.
- O retriever encontra os registros esperados nas perguntas de referência.
- O modelo responde em português somente quando o contexto oferece suporte.
- A interface apresenta resposta, fontes e erros compreensíveis.
- O processo completo pode ser reproduzido a partir da documentação final.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Estado atual

O projeto está na fase de planejamento concluído e início da fundação.

- O escopo histórico de Red/Blue/Yellow foi definido.
- A arquitetura e as fontes de dados foram escolhidas.
- O roadmap foi dividido em 25 issues.
- O backlog foi organizado por fase, prioridade, ordem e status.
- A [issue #2][first-task-url] é a primeira tarefa pronta para implementação.
- O código da aplicação ainda não foi iniciado.

Comandos de instalação e uso serão adicionados quando a fundação e os entrypoints correspondentes estiverem implementados e validados. Isso evita documentar um setup que ainda não existe no repositório.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Licença

O código criado neste projeto é distribuído sob a **MIT License**. Consulte o arquivo [LICENSE][license-url] para conhecer os termos completos.

A licença do projeto não concede direitos sobre nomes, personagens, imagens ou marcas da franquia Pokémon, nem substitui os termos aplicáveis às fontes e dependências de terceiros.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

## Referências e créditos

- [PokeAPI documentation][pokeapi-docs-url]
- [PokeAPI fair use policy][pokeapi-fair-use-url]
- [Pokémon Showdown: dados da Geração I][showdown-data-url]
- [Pokémon Showdown: licença MIT][showdown-license-url]
- [LangChain RAG tutorial][langchain-rag-url]
- [ChromaDB documentation][chroma-url]
- [OpenAI Embeddings guide][openai-embeddings-url]
- Estrutura deste documento inspirada no [Best-README-Template][readme-template-url]

Pokémon e nomes relacionados pertencem aos seus respectivos proprietários. Este repositório é um projeto educacional independente, sem afiliação ou endosso da Nintendo, Game Freak, Creatures Inc. ou The Pokémon Company.

<p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>

[python-shield]: https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[langchain-shield]: https://img.shields.io/badge/LangChain-RAG-1C3C3C?style=for-the-badge
[langchain-url]: https://python.langchain.com/
[openai-shield]: https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white
[openai-url]: https://platform.openai.com/docs/
[issues-shield]: https://img.shields.io/github/issues/JonathanBufon/pokechat-ai.svg?style=for-the-badge
[issues-url]: https://github.com/JonathanBufon/pokechat-ai/issues
[project-shield]: https://img.shields.io/badge/GitHub_Project-Backlog-0969DA?style=for-the-badge&logo=github
[project-url]: https://github.com/users/JonathanBufon/projects/1
[license-shield]: https://img.shields.io/github/license/JonathanBufon/pokechat-ai.svg?style=for-the-badge
[license-url]: https://github.com/JonathanBufon/pokechat-ai/blob/main/LICENSE
[roadmap-url]: https://github.com/JonathanBufon/pokechat-ai/issues/1
[first-task-url]: https://github.com/JonathanBufon/pokechat-ai/issues/2
[pokeapi-url]: https://pokeapi.co/
[pokeapi-docs-url]: https://pokeapi.co/docs/v2
[pokeapi-fair-use-url]: https://pokeapi.co/docs/v2#fairuse
[showdown-data-url]: https://github.com/smogon/pokemon-showdown/blob/master/data/mods/gen1/pokedex.ts
[showdown-license-url]: https://github.com/smogon/pokemon-showdown/blob/master/LICENSE
[httpx-url]: https://www.python-httpx.org/
[dotenv-url]: https://pypi.org/project/python-dotenv/
[chroma-url]: https://docs.trychroma.com/
[streamlit-url]: https://streamlit.io/
[pytest-url]: https://docs.pytest.org/
[langchain-rag-url]: https://python.langchain.com/docs/tutorials/rag/
[openai-embeddings-url]: https://platform.openai.com/docs/guides/embeddings
[readme-template-url]: https://github.com/othneildrew/Best-README-Template
