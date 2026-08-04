# Pokédex RAG Chatbot

Chatbot de Pokémon construído com **RAG (Retrieval-Augmented Generation)** para demonstrar a arquitetura de agentes de IA com recuperação de contexto. O bot responde perguntas sobre os 151 Pokémon da primeira geração usando dados oficiais da [PokéAPI](https://pokeapi.co/), embeddings da OpenAI e busca vetorial local com ChromaDB.

---

## Objetivo

Demonstrar domínio prático do pipeline RAG completo:

1. **Ingestão** de dados de uma API pública real.
2. **Chunking** e **embedding** de documentos.
3. **Armazenamento vetorial** persistente.
4. **Retrieval semântico** por similaridade.
5. **Augmentação de prompt** com contexto recuperado.
6. **Geração** condicionada via LLM (OpenAI).

O caso de uso "Pokémon" é intencionalmente lúdico — a arquitetura é a mesma que se aplicaria a documentação técnica, base de conhecimento corporativa ou suporte a produto.

---

## Arquitetura

```
                       ┌──────────────────┐
                       │    PokéAPI       │
                       │  (fonte pública) │
                       └────────┬─────────┘
                                │  fetch (script único de ingest)
                                ▼
                       ┌──────────────────┐
                       │  Normalização    │  → 1 documento por Pokémon
                       │  + Chunking      │    (nome, tipos, stats, habilidades,
                       └────────┬─────────┘     descrição da Pokédex, evoluções)
                                │
                                ▼
                       ┌──────────────────┐
                       │ OpenAI Embeddings│  text-embedding-3-small
                       │   (batch)        │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │    ChromaDB      │  persistência local em ./chroma_db
                       │ (vector store)   │
                       └──────────────────┘

                     ─── query time ───

  usuário → Streamlit UI → embed(query) → top-k retrieve → prompt aumentado
                                                                  │
                                                                  ▼
                                                          OpenAI Chat Completions
                                                                  │
                                                                  ▼
                                                          resposta ao usuário
```

### Componentes

| Camada          | Ferramenta                    | Papel                                                        |
|-----------------|-------------------------------|--------------------------------------------------------------|
| Fonte de dados  | PokéAPI                       | REST API pública, sem autenticação                           |
| Orquestração    | LangChain                     | Abstrações de retriever, prompt template, chain              |
| Embeddings      | `text-embedding-3-small`      | Vetor de 1536 dimensões, barato e performático               |
| Vector store    | ChromaDB (modo persistente)   | Roda local, zero configuração de servidor                    |
| LLM             | `gpt-4o-mini`                 | Geração de resposta com contexto injetado                    |
| UI              | Streamlit                     | Chat interface com histórico de conversa                     |

---

## Stack

- **Python 3.11+**
- `langchain` + `langchain-openai` + `langchain-chroma`
- `chromadb` (embutido, persistência em disco)
- `openai` (SDK)
- `streamlit` (UI)
- `httpx` (fetch da PokéAPI com retry)
- `python-dotenv` (config)

---

## Estrutura de arquivos (planejada)

```
rag-imp/
├── README.md                    # este arquivo
├── requirements.txt             # dependências pinadas
├── .env.example                 # template de variáveis de ambiente
├── .gitignore
│
├── src/
│   ├── ingest.py                # fetch da PokéAPI → embed → grava no Chroma
│   ├── retriever.py             # wrapper do retriever + config de top-k
│   ├── chain.py                 # monta prompt template + RAG chain
│   └── app.py                   # UI Streamlit (entrypoint do chat)
│
├── data/
│   └── raw/                     # cache local dos JSONs da PokéAPI (opcional)
│
└── chroma_db/                   # gerado pelo ingest — NÃO commitar
```

---

## Modelagem do documento

Cada Pokémon vira **um documento** no vector store. O texto indexado é uma string estruturada em linguagem natural (melhor para embeddings do que JSON cru):

```
Nome: Bulbasaur (#001)
Tipos: Grama, Venenoso
Altura: 0.7m | Peso: 6.9kg
Habilidades: Overgrow, Chlorophyll (oculta)
Estatísticas base: HP 45, Ataque 49, Defesa 49, Sp.Atk 65, Sp.Def 65, Velocidade 45
Descrição da Pokédex: Uma semente estranha foi plantada em suas costas ao nascer...
Evolução: Bulbasaur → Ivysaur (nível 16) → Venusaur (nível 32)
```

**Metadados** salvos junto ao vetor (para filtros e citação):
`id`, `nome`, `tipos`, `geracao`, `numero_pokedex`.

---

## Pipeline RAG detalhado

### 1. Ingestão (`ingest.py`) — executado uma vez

- Faz `GET /pokemon/{1..151}` e `/pokemon-species/{id}` na PokéAPI.
- Normaliza cada resposta no formato de documento acima.
- Chunking: **1 Pokémon = 1 chunk** (documentos curtos, não precisa split).
- Gera embeddings em batch (reduz chamadas à OpenAI).
- Persiste no ChromaDB (`./chroma_db`).

### 2. Retrieval

- `similarity_search` por cosine similarity.
- `top_k = 4` como default (ajustável na UI).
- Retorna os documentos mais relevantes + score.

### 3. Augmentação e geração

Prompt template:

```
Você é um Professor Pokémon especialista na primeira geração.
Responda usando APENAS o contexto abaixo. Se a informação não
estiver no contexto, diga que não sabe.

Contexto:
{contexto_recuperado}

Pergunta: {pergunta}
```

O contexto injetado são os documentos vindos do retriever, concatenados com separadores.

---

## Setup

```bash
# 1. clonar e entrar no diretório
cd rag-imp

# 2. criar ambiente virtual
python -m venv .venv
source .venv/bin/activate

# 3. instalar dependências
pip install -r requirements.txt

# 4. configurar chave da OpenAI
cp .env.example .env
# editar .env e preencher OPENAI_API_KEY=sk-...

# 5. rodar a ingestão (~2 min, gasta ~$0.01 em embeddings)
python src/ingest.py

# 6. iniciar o chat
streamlit run src/app.py
```

Acesse `http://localhost:8501`.

---

## Variáveis de ambiente (`.env`)

| Variável              | Descrição                                              | Default                    |
|-----------------------|--------------------------------------------------------|----------------------------|
| `OPENAI_API_KEY`      | Chave da API OpenAI (obrigatória)                      | —                          |
| `OPENAI_CHAT_MODEL`   | Modelo de geração                                      | `gpt-4o-mini`              |
| `OPENAI_EMBED_MODEL`  | Modelo de embedding                                    | `text-embedding-3-small`   |
| `CHROMA_PERSIST_DIR`  | Caminho do banco vetorial                              | `./chroma_db`              |
| `RETRIEVER_TOP_K`     | Nº de documentos recuperados por query                 | `4`                        |

---

## Exemplos de uso

Perguntas que o RAG resolve bem (informação está nos dados):

- *"Quais os Pokémon do tipo Fogo da primeira geração?"*
- *"Compare as estatísticas de Charizard e Blastoise."*
- *"Qual a evolução final do Eevee no jogo original?"*
- *"Que Pokémon têm a habilidade Levitate?"*

Perguntas que o modelo deve recusar (fora do escopo indexado):

- *"Quem é o campeão da Liga Pokémon em Unova?"* → 2ª geração+, não está no índice.
- *"Qual a estratégia competitiva de Landorus-T?"* → dados competitivos não foram ingeridos.

---

## Decisões de design

- **ChromaDB local** em vez de Pinecone/Weaviate: zero setup, roda offline, suficiente para demo.
- **1 documento por Pokémon** em vez de chunking fino: os dados são curtos e coesos; splittar quebraria a semântica.
- **Descrição em linguagem natural** em vez de JSON: embeddings performam melhor em prosa.
- **`gpt-4o-mini`** em vez de `gpt-4o`: 20x mais barato, qualidade suficiente para Q&A factual.
- **Streamlit** em vez de framework web completo: foco fica no RAG, não em boilerplate de UI.

---

## Extensões possíveis

Ideias para evoluir o projeto (não fazem parte do escopo inicial):

- **Ferramentas (tool use)**: agente decide entre RAG ou chamada direta à PokéAPI para dados dinâmicos.
- **Re-ranking**: adicionar Cohere Rerank ou cross-encoder após o retrieval inicial.
- **Hybrid search**: combinar BM25 + vetorial (via `EnsembleRetriever` do LangChain).
- **Avaliação**: adicionar `ragas` ou `deepeval` para medir groundedness e answer relevancy.
- **Streaming**: exibir tokens em tempo real na UI.
- **Multimodal**: indexar sprites dos Pokémon e permitir busca por imagem.

---

## Custos estimados

- **Ingestão** (uma vez): ~151 embeddings × ~200 tokens ≈ 30K tokens → **< $0.01**
- **Query típica**: ~800 tokens de contexto + ~200 de resposta ≈ 1K tokens no `gpt-4o-mini` → **~$0.0002**

Praticamente gratuito para uma demo.

---

## Referências

- [PokéAPI docs](https://pokeapi.co/docs/v2)
- [LangChain — RAG tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [ChromaDB docs](https://docs.trychroma.com/)
- [OpenAI Embeddings guide](https://platform.openai.com/docs/guides/embeddings)
