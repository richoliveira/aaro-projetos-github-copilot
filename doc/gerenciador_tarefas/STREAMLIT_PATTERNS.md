# Padrões e Otimizações Streamlit - Gerenciador de Tarefas

## Índice
1. [Visão Geral de Padrões Streamlit](#visão-geral-de-padrões-streamlit)
2. [Caching e Performance](#caching-e-performance)
3. [Gerenciamento de Estado](#gerenciamento-de-estado)
4. [Re-renderização (Rerun)](#re-renderização-rerun)
5. [Callbacks e Event Handling](#callbacks-e-event-handling)
6. [Layout e Componentes](#layout-e-componentes)
7. [Boas Práticas](#boas-práticas)
8. [Otimizações Implementadas](#otimizações-implementadas)
9. [Troubleshooting Comum](#troubleshooting-comum)
10. [Patterns Avançados](#patterns-avançados)

---

## Visão Geral de Padrões Streamlit

### O que é Streamlit?

Streamlit é um framework que permite criar aplicações web interativas com Python puro, sem JavaScript/HTML/CSS. Funciona através de um modelo declarativo onde o script é re-executado integralmente em cada interação.

### Modelo de Execução do Streamlit

```
┌─────────────────────────────────────────────────┐
│  1. Usuário Carrega Aplicação ou Interage      │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │ 2. Streamlit Executa:   │
        │    def main():          │
        │     st.title(...)       │
        │     st.write(...)       │
        │     ... (todo o script) │
        └────────────┬────────────┘
                     │
              ┌──────▼────────┐
              │ Mudanças?    │
              └──────┬────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
         ▼                      ▼
    Primeiro Run         Rerun (st.rerun)
    ├─ Cache miss        ├─ Cache hit
    ├─ Cria objetos      ├─ Reutiliza objetos
    └─ Armazena em cache └─ UI atualizada
```

### Características Importantes

1. **Script re-executa completamente** a cada interação
2. **Cache preserva objetos** entre execuções
3. **Ordem de execução** importa (top-down)
4. **Estado da sessão** é único por abrir do navegador

---

## Caching e Performance

### Padrão 1: @st.cache_resource

**Uso**: Cache de recursos (objetos caros, singletons)

```python
@st.cache_resource
def inicializar_gestor() -> GerenciadorTarefas:
    """Cria instância única do gerenciador na sessão."""
    return GerenciadorTarefas()
```

**Características**:
- ✅ Executa apenas uma vez por sessão
- ✅ Resultado é reutilizado entre reruns
- ✅ Ideal para singletons e inicializações caras
- ✅ Seguro para objetos mutáveis

**Ciclo de Vida**:

```
Primeira Execução
├─ @cache_resource detecta
├─ Função é executada
├─ Resultado armazenado em cache
└─ Objeto criado: GerenciadorTarefas()

Rerun 1
├─ @cache_resource encontra no cache
├─ Função NÃO é executada
└─ Retorna objeto existente

Rerun 2
├─ @cache_resource encontra no cache
├─ Função NÃO é executada
└─ Retorna mesmo objeto

... (sessão continua)

Sessão Encerra
└─ Cache é descartado
   Novo acesso = novo objeto
```

### Padrão 2: @st.cache_data

**Uso**: Cache de dados computados (cálculos caros, APIs)

```python
@st.cache_data  # Exemplo (não usado neste projeto)
def obter_dados_externos():
    """Cache de dados computados."""
    return requests.get("https://api.example.com").json()
```

**Características**:
- ✅ Otimiza cálculos custosos
- ✅ Reutiliza entre sessões (por padrão)
- ❌ Não deve ser usado com objetos mutáveis

**Quando Usar**:
- Resultados de APIs
- Cálculos matemáticos
- Processamento de dados

### Comparação: cache_resource vs cache_data

| Aspecto | cache_resource | cache_data |
|---|---|---|
| **Escopo** | Por sessão | Pode ser global |
| **Dados Mutáveis** | ✅ OK | ❌ Evitar |
| **Objetos Stateful** | ✅ Ideal | ❌ Problema |
| **Compartilhamento** | Sessão única | Múltiplas sessões |
| **Uso Típico** | BD connections, classes | Resultados computados |

### Por que cache_resource no Projeto?

```
✅ Precisamos de SINGLETON (uma instância)
✅ Objeto é MUTÁVEL (modifica _tarefas)
✅ Deve ser ÚNICO por sessão
✅ Cada usuário tem seu próprio estado
```

---

## Gerenciamento de Estado

### Modelo de Estado do Streamlit

```
┌────────────────────────────────────────┐
│  Session State (st.session_state)      │
│                                        │
│  Armazena variáveis durante sessão    │
│  Preserva entre reruns                │
│  Específico por navegador              │
└────────────────────────────────────────┘
```

### Estado Neste Projeto

```
Session State
│
└─ @st.cache_resource
   └─ GerenciadorTarefas
      └─ _tarefas: List[Dict]
         ├─ {"titulo": "...", "concluida": False}
         ├─ {"titulo": "...", "concluida": False}
         └─ {"titulo": "...", "concluida": True}
```

### Fluxo de Estado

```
1. Primeira Visita
   ├─ Session inicia
   ├─ @cache_resource executa
   ├─ GerenciadorTarefas() é criado
   └─ _tarefas = []

2. Usuário Adiciona Tarefa
   ├─ st.form_submit_button clicado
   ├─ gestor.adicionar_tarefa() chamado
   ├─ _tarefas.append(nova_tarefa)
   ├─ st.success() mostra mensagem
   └─ st.rerun() recarrega página

3. Rerun Ocorre
   ├─ @cache_resource recupera do cache
   ├─ Mesmo gerenciador retornado
   ├─ _tarefas contém a nova tarefa
   └─ listar_tarefas() retorna [tarefa_nova]

4. UI Re-renderiza
   ├─ Tarefa nova aparece na lista
   └─ Usuário vê mudança
```

---

## Re-renderização (Rerun)

### Conceito: st.rerun()

```python
st.rerun()  # Restart o script do topo
```

**Efeito**:
- Re-executa `main()` do início
- Reconstrói toda a UI
- Mantém estado do cache

**Quando Usar**:
- ✅ Após modificar dados (CRUD)
- ✅ Após ações do usuário
- ✅ Quando UI precisa atualizar
- ❌ Em loops infinitos (causa travamento)
- ❌ Em callbacks sem condição

### Fluxo com st.rerun()

```
┌────────────────────────────────────────┐
│  Usuário Clica em "Adicionar Tarefa"   │
└────────────┬───────────────────────────┘
             │
             ▼
    ┌────────────────────────────────┐
    │ if submit:                     │
    │   if nova_tarefa.strip():      │
    │     gestor.adicionar_tarefa()  │
    │     st.success("...")          │
    │     st.rerun() ← AQUI!         │
    └────────────┬───────────────────┘
                 │ (Script interrompido)
                 │ (Novo run iniciado)
                 ▼
    ┌────────────────────────────────┐
    │ main() Executa Novamente       │
    │ (do topo)                      │
    │                                │
    │ 1. set_page_config()           │
    │ 2. title()                     │
    │ 3. inicializar_gestor()        │
    │    └─ @cache recupera          │
    │ 4. form()                      │
    │ 5. subheader()                 │
    │ 6. listar_tarefas()            │
    │    └─ Inclui nova tarefa       │
    │ 7. renderizar_tarefa()         │
    │    └─ Renderiza todas (nova)   │
    └────────────┬───────────────────┘
                 │
                 ▼
    ┌────────────────────────────────┐
    │ UI Atualizada com Nova Tarefa  │
    │ Usuário Vê a Mudança           │
    └────────────────────────────────┘
```

### Alternativa: Sem st.rerun()

**O que aconteceria**:
```python
if submit:
    if nova_tarefa.strip():
        gestor.adicionar_tarefa(nova_tarefa)
        st.success("Tarefa adicionada!")
        # SEM st.rerun()
```

**Problema**:
- ❌ Script continua até o fim da main()
- ❌ listar_tarefas() já foi executado (antes da adição)
- ❌ Lista na tela não mostra tarefa nova
- ❌ Usuário não vê mudança até recarregar manualmente

---

## Callbacks e Event Handling

### Padrão 1: on_change Callback (Não Utilizado)

```python
st.checkbox(
    "OK",
    key=f"check_{indice}",
    value=concluida,
    on_change=lambda: None  # on_change = lambda: None (no-op)
)
```

**Por que `on_change=lambda: None`?**

```
❌ Sem on_change:
   - Checkbox dispara ao mudar
   - st.rerun() seria chamado automaticamente
   - Problema: Renderiza antes de capturar o novo valor

✅ Com on_change=lambda: None:
   - Callback é executado (função vazia)
   - Nada acontece
   - Script continua até o final
   - Captura o novo valor
   - st.rerun() é chamado manualmente
   - Novo run usa novo valor
```

### Fluxo com Checkbox e on_change

```
1. Usuário Clica no Checkbox
   │
   ▼
2. Streamlit Detecta Mudança
   │
   ▼
3. on_change callback Executado
   ├─ (função vazia: lambda: None)
   │
   ▼
4. Script Continua (renderizar_tarefa)
   │
   ├─ tarefa_concluida = st.checkbox() retorna
   │                     novo valor (True/False)
   │
   ▼
5. Condicional Verifica
   │
   ├─ if tarefa_concluida and not tarefa["concluida"]:
   │    └─ True: tarefa foi marcada
   │
   ▼
6. Chamar Core
   │
   ├─ gestor.marcar_como_concluida(indice)
   │
   ▼
7. Recarregar UI
   │
   ├─ st.rerun()
   │
   ▼
8. Script Re-executa com Novo Estado
   │
   ├─ renderizar_tarefa() renderiza com strikethrough
   │
   ▼
9. UI Atualizada
   │
   └─ Usuário Vê Tarefa Concluída
```

### Padrão 2: Form Submit Button

```python
with st.form(key="form_nova_tarefa"):
    nova_tarefa = st.text_input(...)
    submit = st.form_submit_button("Adicionar tarefa")
    
    if submit:  # Dispara apenas quando botão clicado
        # Processar
```

**Características**:
- ✅ Agrupamento de inputs
- ✅ Submissão apenas quando botão clicado
- ✅ Todos os inputs capturados junto
- ✅ Evita submissões acidentais

---

## Layout e Componentes

### Padrão: Columns para Layout Horizontal

```python
def renderizar_tarefa(tarefa: dict, indice: int) -> None:
    """Layout responsivo com colunas."""
    
    with st.container():  # Agrupamento visual
        col_titulo, col_checkbox = st.columns([4, 1])
        
        with col_titulo:  # 80% da largura
            if tarefa["concluida"]:
                st.markdown(f"<s>{indice + 1}. {tarefa['titulo']}</s>",
                           unsafe_allow_html=True)
            else:
                st.write(f"{indice + 1}. {tarefa['titulo']}")
        
        with col_checkbox:  # 20% da largura
            tarefa_concluida = st.checkbox(
                "OK",
                key=f"check_{indice}",
                value=tarefa["concluida"]
            )
```

**Vantagens**:
- ✅ Responsivo: Proporção [4:1] se adapta ao tamanho
- ✅ Alinhamento: Título e checkbox lado a lado
- ✅ Flexível: Fácil mudar proporções

### Padrão: Mensagens Contextuais

```python
# Sucesso
if submit and nova_tarefa.strip():
    gestor.adicionar_tarefa(nova_tarefa)
    st.success("Tarefa adicionada com sucesso!")

# Aviso
elif submit and not nova_tarefa.strip():
    st.warning("Digite um nome para a tarefa antes de adicionar.")

# Informação (Lista vazia)
if not tarefas:
    st.info("Nenhuma tarefa cadastrada ainda...")
```

**Padrão**:
- `st.success()` - Operação bem-sucedida (verde)
- `st.warning()` - Aviso ao usuário (amarelo)
- `st.info()` - Informação geral (azul)
- `st.error()` - Erro crítico (vermelho)

---

## Boas Práticas

### Prática 1: Evitar Mutable Default Arguments

```python
# ❌ Errado (Python antipattern)
def criar_gerenciador(tarefas=[]):
    # ...
    return GerenciadorTarefas(tarefas)

# ✅ Correto
def criar_gerenciador():
    return GerenciadorTarefas()  # Cria novo internamente
```

### Prática 2: Usar Type Hints

```python
# ✅ Bom - Tipos explícitos
def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
    """Adiciona tarefa tipada."""
    pass

# ❌ Evitar - Tipos implícitos
def adicionar_tarefa(self, titulo):
    """Não fica claro o tipo esperado."""
    pass
```

### Prática 3: Colocar st.cache_resource Antes de Usar

```python
def main() -> None:
    # ✅ Chamado no início de main()
    gestor = inicializar_gestor()
    
    # Usar gerenciador...
```

### Prática 4: Evitar Computação Pesada em main()

```python
# ❌ Evitar - Executa todo rerun
def main() -> None:
    dados = processar_dados_pesado()  # Re-calcula sempre!
    st.write(dados)

# ✅ Melhor - Cache a computação
@st.cache_data
def processar_dados_pesado():
    return dados

def main() -> None:
    dados = processar_dados_pesado()  # Do cache
    st.write(dados)
```

### Prática 5: Limpar Chaves de Keys Únicos

```python
# ✅ Bom - Chaves únicas por elemento
for indice, tarefa in enumerate(tarefas):
    st.checkbox(
        "OK",
        key=f"check_{indice}"  # Único por indice
    )

# ❌ Evitar - Mesmo key para todos
for tarefa in tarefas:
    st.checkbox("OK", key="check")  # Problema!
```

---

## Otimizações Implementadas

### Otimização 1: Cache Resource para Singleton

```python
@st.cache_resource
def inicializar_gestor() -> GerenciadorTarefas:
    return GerenciadorTarefas()
```

**Impacto**:
- ✅ Evita recriar gerenciador a cada rerun
- ✅ Preserva estado entre reruns
- ✅ Performance: O(1) em vez de O(n)

### Otimização 2: Defensive Copy em listar_tarefas()

```python
def listar_tarefas(self) -> List[Dict[str, object]]:
    return self._tarefas.copy()  # Cópia rasa
```

**Impacto**:
- ✅ Protege estado interno
- ✅ Evita modificações acidentais
- ✅ Performance: Cópia O(n) é aceitável para listas pequenas

### Otimização 3: Renderização Iterativa

```python
for indice, tarefa in enumerate(tarefas):
    renderizar_tarefa(tarefa, indice)
```

**Impacto**:
- ✅ DRY (Don't Repeat Yourself) - Código limpo
- ✅ Reutilização de lógica de renderização
- ✅ Fácil adicionar features (ex: filtros)

### Otimização 4: Validação em Duas Camadas

```python
# UI Layer
if nova_tarefa.strip():
    try:
        # Core Layer
        gestor.adicionar_tarefa(nova_tarefa)
        st.success("...")
    except ValueError as e:
        st.error(str(e))
else:
    st.warning("...")
```

**Impacto**:
- ✅ Falha rápido na UI (evita chamada ao core)
- ✅ Validação dupla em core (defesa profunda)
- ✅ Experiência do usuário melhor (feedback rápido)

---

## Troubleshooting Comum

### Problema 1: Tarefa Não Aparece Após Adicionar

**Sintomas**: Usuário clica em "Adicionar", vê mensagem de sucesso, mas tarefa não aparece

**Causas Possíveis**:
1. ❌ `st.rerun()` não foi chamado
2. ❌ Gerenciador não está em cache
3. ❌ Validação impede criação

**Solução**:
```python
if submit:
    if nova_tarefa.strip():
        gestor.adicionar_tarefa(nova_tarefa)
        st.success("Tarefa adicionada com sucesso!")
        st.rerun()  # ← CRUCIAL
    else:
        st.warning("Digite um nome...")
```

### Problema 2: Checkbox Dispara Múltiplas Vezes

**Sintomas**: Clicar checkbox causa múltiplos reruns

**Causas**:
1. ❌ `on_change` chama `st.rerun()` recursivamente
2. ❌ Condicional não protege

**Solução**:
```python
# ✅ Verificar se houve mudança real
if tarefa_concluida and not tarefa["concluida"]:
    # Apenas se mudou de False → True
    gestor.marcar_como_concluida(indice)
    st.rerun()
```

### Problema 3: Dados Perdidos ao Recarregar

**Sintomas**: Fechar aba e reabrir = dados sumem

**Causa**: É esperado - dados em memória

**Solução**: Adicionar persistência (DB)

---

## Patterns Avançados

### Pattern 1: Conditional Rendering

```python
if not tarefas:
    st.info("Nenhuma tarefa...")
    # Renderização diferente para lista vazia
else:
    for tarefa in tarefas:
        renderizar_tarefa(tarefa, indice)
    # Renderização normal
```

### Pattern 2: Form Validation

```python
with st.form("meu_form"):
    entrada = st.text_input("Campo")
    submit = st.form_submit_button("Enviar")
    
    if submit:
        # Validar após submit
        if validar(entrada):
            processar(entrada)
            st.success("OK!")
        else:
            st.error("Inválido!")
```

### Pattern 3: Multi-Step Wizard

```python
if "step" not in st.session_state:
    st.session_state.step = 0

if st.session_state.step == 0:
    st.write("Passo 1")
    if st.button("Próximo"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 1:
    st.write("Passo 2")
    if st.button("Anterior"):
        st.session_state.step = 0
        st.rerun()
```

### Pattern 4: Dynamic Sidebar

```python
with st.sidebar:
    opcao = st.selectbox(
        "Escolha",
        ["Opção 1", "Opção 2", "Opção 3"]
    )

if opcao == "Opção 1":
    pagina_1()
elif opcao == "Opção 2":
    pagina_2()
```

---

## Checklist de Otimização Streamlit

- [ ] Usar `@st.cache_resource` para objetos estateful
- [ ] Usar `@st.cache_data` para cálculos caros
- [ ] Evitar computação pesada em `main()`
- [ ] Usar `st.session_state` para estado compartilhado
- [ ] Chamar `st.rerun()` após modificar dados
- [ ] Usar `key` único para widgets dinâmicos
- [ ] Validar em múltiplas camadas
- [ ] Usar `columns` para layouts responsivos
- [ ] Feedback visual (success, warning, info, error)
- [ ] Defensive copying para proteger estado

---

## Resumo de Padrões Utilizados

| Padrão | Localização | Benefício |
|---|---|---|
| **@st.cache_resource** | `inicializar_gestor()` | Singleton, persistência |
| **st.form()** | Formulário de entrada | Agrupamento, submissão controlada |
| **st.columns()** | Renderização de tarefa | Layout responsivo |
| **st.rerun()** | Após CRUD | UI atualizada |
| **Validação dupla** | UI + Core | Defesa profunda |
| **Defensive copy** | `listar_tarefas()` | Estado protegido |
| **Keys dinâmicas** | `f"check_{indice}"` | Renderização iterativa |
| **Mensagens contextuais** | Feedback ao usuário | UX melhorado |

---

**Última Atualização**: 2026-09-01  
**Versão**: 1.0  
**Autor**: Documentação Técnica
