# Interface e Componentes - Gerenciador de Tarefas

## Índice
1. [Visão Geral da Interface](#visão-geral-da-interface)
2. [Componentes Streamlit Utilizados](#componentes-streamlit-utilizados)
3. [Layout e Estrutura](#layout-e-estrutura)
4. [Métodos Públicos da API](#métodos-públicos-da-api)
5. [Parâmetros de Entrada](#parâmetros-de-entrada)
6. [Retorno de Saída](#retorno-de-saída)
7. [Exemplos de Uso](#exemplos-de-uso)
8. [Estados e Transições de UI](#estados-e-transições-de-ui)
9. [Feedback ao Usuário](#feedback-ao-usuário)

---

## Visão Geral da Interface

A interface do Gerenciador de Tarefas é construída com **Streamlit**, um framework que permite criar aplicações web interativas com Python puro, sem necessidade de HTML/CSS/JavaScript.

### Características da Interface

- **Responsiva**: Adapta-se a diferentes tamanhos de tela
- **Intuitiva**: Usa componentes visuais familiares e convencionais
- **Reactiva**: Atualiza em tempo real após ações do usuário
- **Acessível**: Componentes padrão com bom suporte a acessibilidade
- **Eficiente**: Re-renderização otimizada com cache

### Estrutura Visual

```
┌─────────────────────────────────────────────────┐
│  Gerenciador de Tarefas                    [✅] │ (page_config)
├─────────────────────────────────────────────────┤
│                                                 │
│  Gerenciador de Tarefas                         │ (title)
│  ─────────────────────                          │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │ Nova tarefa                               │  │
│  │ [______________________________________]  │  │ (form)
│  │ [Adicionar tarefa]                        │  │ (form_submit_button)
│  └───────────────────────────────────────────┘  │
│                                                 │
│  Lista de Tarefas                               │ (subheader)
│  ────────────────                               │
│                                                 │
│  ☐ 1. Tarefa 1                                  │ (checkbox + container)
│  ☑ 2. Tarefa 2                                  │ (completed - strikethrough)
│  ☐ 3. Tarefa 3                                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Componentes Streamlit Utilizados

### 1. st.set_page_config()

**Localização**: `app.py` - `main()` - Primeira linha

**Propósito**: Configurar metadados e aparência da página

```python
st.set_page_config(page_title="Gerenciador de Tarefas", page_icon="✅")
```

| Parâmetro | Valor | Descrição |
|---|---|---|
| `page_title` | "Gerenciador de Tarefas" | Título na aba do navegador |
| `page_icon` | "✅" | Emoji/ícone na aba |

**Saída Visual**: Aba do navegador mostra "✅ Gerenciador de Tarefas"

---

### 2. st.title()

**Localização**: `app.py` - `main()` - Após `set_page_config`

**Propósito**: Exibir título principal da página (h1)

```python
st.title("Gerenciador de Tarefas")
```

**Saída Visual**:
```
Gerenciador de Tarefas
═══════════════════════
```

---

### 3. st.form()

**Localização**: `app.py` - `main()` - Bloco de formulário

**Propósito**: Agrupar componentes de entrada com envio controlado

```python
with st.form(key="form_nova_tarefa"):
    nova_tarefa = st.text_input("Nova tarefa", placeholder="...")
    submit = st.form_submit_button("Adicionar tarefa")
    
    if submit:
        # Processar entrada
```

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `key` | str | Identificador único do formulário |

**Comportamento**: 
- Agrupa entrada e botão como uma unidade
- Submissão apenas quando botão é clicado
- Evita submissões acidentais

---

### 4. st.text_input()

**Localização**: Dentro do `st.form()`

**Propósito**: Campo de entrada de texto de linha única

```python
nova_tarefa = st.text_input(
    "Nova tarefa",
    placeholder="Digite o nome da tarefa...",
)
```

| Parâmetro | Valor | Descrição |
|---|---|---|
| `label` | "Nova tarefa" | Rótulo do campo |
| `placeholder` | "Digite o nome da tarefa..." | Texto de dica |

**Saída**: String com o texto digitado pelo usuário

**Eventos**: 
- Captura texto em tempo real
- Permite ações `on_change` (não utilizado neste caso)

---

### 5. st.form_submit_button()

**Localização**: Dentro do `st.form()`

**Propósito**: Botão para submeter o formulário

```python
submit = st.form_submit_button("Adicionar tarefa")
```

**Retorno**: Boolean (True quando clicado, False caso contrário)

**Comportamento**:
- Só dispara quando clicado
- Todos os inputs do form são capturados juntos

---

### 6. st.success()

**Localização**: `app.py` - Após adicionar tarefa com sucesso

**Propósito**: Exibir mensagem de sucesso (verde com ícone ✓)

```python
st.success("Tarefa adicionada com sucesso!")
```

**Saída Visual**:
```
✓ Tarefa adicionada com sucesso!
```

**Estilo**: Fundo verde, ícone checkmark

---

### 7. st.warning()

**Localização**: `app.py` - Quando entrada é inválida

**Propósito**: Exibir aviso/atenção (amarelo com ícone ⚠)

```python
st.warning("Digite um nome para a tarefa antes de adicionar.")
```

**Saída Visual**:
```
⚠ Digite um nome para a tarefa antes de adicionar.
```

**Estilo**: Fundo amarelo, ícone warning

---

### 8. st.info()

**Localização**: `app.py` - Quando lista está vazia

**Propósito**: Exibir mensagem informativa (azul com ícone ℹ)

```python
st.info("Nenhuma tarefa cadastrada ainda. Adicione sua primeira tarefa acima.")
```

**Saída Visual**:
```
ℹ Nenhuma tarefa cadastrada ainda. Adicione sua primeira tarefa acima.
```

**Estilo**: Fundo azul, ícone info

---

### 9. st.subheader()

**Localização**: `app.py` - Antes da lista de tarefas

**Propósito**: Exibir subtítulo (h2)

```python
st.subheader("Lista de Tarefas")
```

**Saída Visual**:
```
Lista de Tarefas
────────────────
```

---

### 10. st.columns()

**Localização**: `app.py` - `renderizar_tarefa()` - Para layout horizontal

**Propósito**: Dividir espaço em colunas

```python
col_titulo, col_checkbox = st.columns([4, 1])
```

**Parâmetros**:
- Lista `[4, 1]` define proporção das colunas (4:1 = 80%:20%)

**Uso**:
```python
with col_titulo:
    st.write(f"{indice + 1}. {titulo}")

with col_checkbox:
    st.checkbox("OK", key=f"check_{indice}", value=concluida)
```

**Estrutura Visual**:
```
col_titulo (80%)          col_checkbox (20%)
[Título da Tarefa]  |     [✓]
```

---

### 11. st.container()

**Localização**: `app.py` - `renderizar_tarefa()` - Agrupamento visual

**Propósito**: Agrupar componentes em um contêiner

```python
with st.container():
    col_titulo, col_checkbox = st.columns([4, 1])
    # ...
```

**Uso**: Organizar visualmente cada tarefa como uma unidade

---

### 12. st.checkbox()

**Localização**: `app.py` - `renderizar_tarefa()` - Dentro da coluna

**Propósito**: Input booleano com visualização interativa

```python
tarefa_concluida = st.checkbox(
    "OK",
    key=f"check_{indice}",
    value=concluida,
    on_change=lambda: None,
)
```

| Parâmetro | Descrição |
|---|---|
| `label` | "OK" - Rótulo do checkbox |
| `key` | Identificador único para cada tarefa |
| `value` | Estado inicial (True/False) |
| `on_change` | Callback quando estado muda |

**Retorno**: Boolean (True se checado, False se não)

---

### 13. st.markdown()

**Localização**: `app.py` - `renderizar_tarefa()` - Para estilo strikethrough

**Propósito**: Renderizar markdown (suporta HTML)

```python
st.markdown(f"<s>{indice + 1}. {titulo}</s>", unsafe_allow_html=True)
```

**Saída**: Texto com strikethrough para tarefas concluídas

```
<s>1. Tarefa Concluída</s>  →  ̶1̶.̶ ̶T̶a̶r̶e̶f̶a̶ ̶C̶o̶n̶c̶l̶u̶í̶d̶a̶
```

---

### 14. st.rerun()

**Localização**: `app.py` - Após ações que modificam o estado

**Propósito**: Recarregar o script e re-renderizar a interface

```python
st.rerun()
```

**Comportamento**:
- Executa `main()` novamente do topo
- Reconstrói toda a UI com novo estado
- Cache preserva o gerenciador (via `@st.cache_resource`)

---

### 15. @st.cache_resource

**Localização**: `app.py` - Decorador da função `inicializar_gestor()`

**Propósito**: Cache de recursos (gerenciador) entre reruns

```python
@st.cache_resource
def inicializar_gestor() -> GerenciadorTarefas:
    """Cria instância única do gerenciador."""
    return GerenciadorTarefas()
```

**Comportamento**:
- Primeira execução: Cria novo gerenciador
- Execuções subsequentes: Reutiliza a mesma instância
- Garante persistência de dados durante a sessão

---

## Layout e Estrutura

### Hierarquia Visual

```
Page Container
│
├── Page Config
│   └── page_title, page_icon
│
├── Title (h1)
│   └── "Gerenciador de Tarefas"
│
├── Form Container
│   ├── Text Input
│   │   └── "Nova tarefa"
│   └── Submit Button
│       └── "Adicionar tarefa"
│
├── Feedback Messages
│   ├── Success
│   ├── Warning
│   └── Info
│
├── Subheader (h2)
│   └── "Lista de Tarefas"
│
└── Tasks List Container
    │
    └── [Para cada tarefa]
        ├── Container
        │   └── Columns [4:1]
        │       ├── Col 1: Título (com strikethrough se concluída)
        │       └── Col 2: Checkbox
        │
        └── Feedback (on change)
            └── st.rerun()
```

### Fluxo de Renderização

```
main()
│
├─→ set_page_config()  (configuração)
│
├─→ title()            (cabeçalho)
│
├─→ inicializar_gestor()  (get/create gerenciador)
│
├─→ form()             (entrada de dados)
│   └─→ validação + adicionar_tarefa()
│
├─→ feedback (sucesso/aviso)
│
├─→ subheader()        (título da lista)
│
├─→ listar_tarefas()   (obter dados)
│
├─→ if not tarefas     (lista vazia)
│   └─→ st.info()
│
└─→ for tarefa:        (renderizar cada tarefa)
    └─→ renderizar_tarefa()
        ├─→ container()
        ├─→ columns()
        ├─→ checkbox()
        └─→ marcar_como_concluida() (on change)
```

---

## Métodos Públicos da API

### API do GerenciadorTarefas

```python
class GerenciadorTarefas:
    """Gerencia a criação, listagem e conclusão de tarefas."""
    
    def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
        """Adiciona uma nova tarefa ao sistema."""
        
    def listar_tarefas(self) -> List[Dict[str, object]]:
        """Retorna a lista completa de tarefas cadastradas."""
        
    def marcar_como_concluida(self, indice: int) -> Dict[str, object]:
        """Marca uma tarefa específica como concluída."""
        
    def limpar_tarefas(self) -> None:
        """Remove todas as tarefas da memória."""
```

### Assinatura Detalhada

#### `adicionar_tarefa(titulo: str) -> Dict[str, object]`

```python
def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
    """Adiciona uma nova tarefa ao sistema.
    
    Args:
        titulo: Nome da tarefa que será registrada.
    
    Returns:
        Dicionário contendo os dados da tarefa criada.
        {'titulo': str, 'concluida': False}
    
    Raises:
        ValueError: Quando o título estiver vazio ou em branco.
    """
```

#### `listar_tarefas() -> List[Dict[str, object]]`

```python
def listar_tarefas(self) -> List[Dict[str, object]]:
    """Retorna a lista completa de tarefas cadastradas.
    
    Returns:
        Lista de dicionários com as tarefas.
        [{'titulo': str, 'concluida': bool}, ...]
    """
```

#### `marcar_como_concluida(indice: int) -> Dict[str, object]`

```python
def marcar_como_concluida(self, indice: int) -> Dict[str, object]:
    """Marca uma tarefa específica como concluída.
    
    Args:
        indice: Posição da tarefa na lista (0-based).
    
    Returns:
        Dicionário da tarefa atualizada.
        {'titulo': str, 'concluida': True}
    
    Raises:
        IndexError: Quando o índice estiver fora do alcance.
    """
```

#### `limpar_tarefas() -> None`

```python
def limpar_tarefas(self) -> None:
    """Remove todas as tarefas da memória."""
```

---

## Parâmetros de Entrada

### Fonte 1: Text Input (Formulário)

| Campo | Tipo | Validação UI | Validação Core | Exemplo |
|---|---|---|---|---|
| `nova_tarefa` | str | `strip()` não vazio | `strip()` + exceção | "Fazer compras" |

### Fonte 2: Checkbox (Interação)

| Campo | Tipo | Captura | Processamento | Exemplo |
|---|---|---|---|---|
| `tarefa_concluida` | bool | Valor do checkbox | Índice + core | True |

### Fonte 3: Iteração (Renderização)

| Campo | Tipo | Origem | Uso | Exemplo |
|---|---|---|---|---|
| `indice` | int | `enumerate()` | Key do checkbox, renderização | 0, 1, 2 |
| `tarefa` | dict | `listar_tarefas()` | Exibição, estado | `{"titulo": "...", "concluida": bool}` |

---

## Retorno de Saída

### Mensagens ao Usuário

| Tipo | Função | Condição | Mensagem |
|---|---|---|---|
| **Success** | `st.success()` | Tarefa adicionada com sucesso | "Tarefa adicionada com sucesso!" |
| **Warning** | `st.warning()` | Entrada vazia | "Digite um nome para a tarefa antes de adicionar." |
| **Info** | `st.info()` | Lista vazia | "Nenhuma tarefa cadastrada ainda. Adicione sua primeira tarefa acima." |
| **Error** | `st.error()` | Exceção capturada | Mensagem da exceção |

### Estruturas Renderizadas

| Elemento | Dados | Renderização |
|---|---|---|
| **Título** | "Gerenciador de Tarefas" | h1 com emoji ✅ |
| **Tarefa Pendente** | `{"titulo": "x", "concluida": False}` | `1. x` com checkbox |
| **Tarefa Concluída** | `{"titulo": "x", "concluida": True}` | `<s>1. x</s>` com checkbox |

---

## Exemplos de Uso

### Exemplo 1: Adicionar Tarefa via UI

```
Usuário: [Digita "Estudar Python"][Clica em "Adicionar tarefa"]

Sistema:
1. Valida: "Estudar Python".strip() → "Estudar Python" ✓
2. Chama: gestor.adicionar_tarefa("Estudar Python")
3. Core: Cria {"titulo": "Estudar Python", "concluida": False}
4. Retorna: Tarefa criada
5. UI: st.success("Tarefa adicionada com sucesso!")
6. UI: st.rerun()
7. Renderiza: Tarefa na lista

Resultado: Usuário vê a tarefa adicionada
```

### Exemplo 2: Marcar Tarefa como Concluída

```
Usuário: [Clica no checkbox ao lado da tarefa]

Sistema:
1. renderizar_tarefa() detecta mudança
2. Valida: tarefa_concluida=True e antes era False
3. Chama: gestor.marcar_como_concluida(0)
4. Core: self._tarefas[0]["concluida"] = True
5. Retorna: Tarefa atualizada
6. UI: st.rerun()
7. Renderiza: Tarefa com strikethrough

Resultado: Usuário vê tarefa marcada como concluída
```

### Exemplo 3: Feedback para Entrada Vazia

```
Usuário: [Digita apenas espaços "   "][Clica em "Adicionar tarefa"]

Sistema:
1. Valida UI: "   ".strip() → "" (vazio)
2. Condicional: if nova_tarefa.strip() → False
3. Executa: st.warning("Digite um nome...")
4. Não chama core (validação falhou)

Resultado: Usuário vê aviso amarelo
```

---

## Estados e Transições de UI

### Estado 1: Inicial (Sem Tarefas)

```
┌─────────────────────────────────┐
│  Gerenciador de Tarefas         │
│                                 │
│  [_______________] [Adicionar]  │
│                                 │
│  Lista de Tarefas               │
│  ─────────────────              │
│  ℹ Nenhuma tarefa cadastrada... │
└─────────────────────────────────┘
```

### Estado 2: Com Tarefas (Mista)

```
┌─────────────────────────────────┐
│  Gerenciador de Tarefas         │
│                                 │
│  [_______________] [Adicionar]  │
│  ✓ Tarefa adicionada com sucesso!
│                                 │
│  Lista de Tarefas               │
│  ─────────────────              │
│  ☐ 1. Tarefa Pendente           │
│  ☑ 2. Tarefa Concluída          │
│  ☐ 3. Outra Tarefa              │
└─────────────────────────────────┘
```

### Fluxo de Estados

```
INICIAL
(Lista vazia)
    │
    ▼
ADICIONANDO_TAREFA
(Usuário digita)
    │
    ▼
VALIDA_E_CRIA
(Sistema processa)
    │
    ├─→ Sucesso: COM_TAREFAS
    │              │
    │              ▼
    │           MARCANDO_CONCLUIDA
    │              │
    │              ▼
    │           TAREFA_CONCLUIDA
    │
    └─→ Erro: EXIBE_AVISO
                   │
                   ▼
               (volta para COM_TAREFAS)
```

---

## Feedback ao Usuário

### Níveis de Feedback

#### 1. Feedback Imediato (Real-time)

```
Campo de entrada: Usuário digita → Texto atualiza instantaneamente
```

#### 2. Feedback de Validação (Após ação)

```
Se válido:  [✓ Tarefa adicionada com sucesso!]  (verde)
Se inválido: [⚠ Digite um nome para a tarefa...] (amarelo)
Se erro:    [✗ Mensagem de erro]                (vermelho)
```

#### 3. Feedback Visual (Após atualização)

```
Tarefa adicionada:     Aparece na lista
Tarefa concluída:      Texto em strikethrough
Checkbox marcado:      Visual de "checked"
```

#### 4. Feedback de Navegação

```
Página recarregada:    st.rerun() → UI atualizada
Estado preservado:     Gerenciador em cache → dados mantêm
```

### Exemplos de Mensagens

| Cenário | Mensagem | Cor | Ícone |
|---|---|---|---|
| Sucesso | "Tarefa adicionada com sucesso!" | Verde | ✓ |
| Aviso | "Digite um nome para a tarefa antes de adicionar." | Amarelo | ⚠ |
| Info | "Nenhuma tarefa cadastrada ainda..." | Azul | ℹ |
| Erro | "Índice da tarefa inválido." | Vermelho | ✗ |

---

## Resumo de Componentes

| Componente | Localização | Propósito | Entrada | Saída |
|---|---|---|---|---|
| set_page_config | main() | Config da página | - | - |
| title | main() | Cabeçalho principal | - | str |
| form | main() | Agrupar inputs | - | - |
| text_input | form | Campo de texto | - | str |
| form_submit_button | form | Botão submit | - | bool |
| success | main() | Msg sucesso | - | - |
| warning | main() | Msg aviso | - | - |
| info | main() | Msg info | - | - |
| subheader | main() | Subtítulo | - | str |
| columns | renderizar_tarefa() | Layout horizontal | - | - |
| container | renderizar_tarefa() | Agrupar visual | - | - |
| checkbox | renderizar_tarefa() | Input booleano | - | bool |
| markdown | renderizar_tarefa() | Md com HTML | - | str |
| rerun | main() | Recarregar | - | - |
| cache_resource | inicializar_gestor() | Cache recursos | - | GerenciadorTarefas |

---

**Última Atualização**: 2026-09-01  
**Versão**: 1.0  
**Autor**: Documentação Técnica
