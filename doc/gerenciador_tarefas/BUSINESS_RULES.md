# Regras de Negócio - Gerenciador de Tarefas

## Índice
1. [Visão Geral das Regras](#visão-geral-das-regras)
2. [Validações Obrigatórias](#validações-obrigatórias)
3. [Constraints de Dados](#constraints-de-dados)
4. [Políticas de Estado](#políticas-de-estado)
5. [Comportamento de Cache e Sessão](#comportamento-de-cache-e-sessão)
6. [Regras de Transição](#regras-de-transição)
7. [Tratamento de Casos Especiais](#tratamento-de-casos-especiais)
8. [Políticas de Integridade](#políticas-de-integridade)

---

## Visão Geral das Regras

### Regras Fundamentais

O Gerenciador de Tarefas opera sob um conjunto de regras que garantem a integridade dos dados e a consistência do sistema.

```
┌────────────────────────────────────────────┐
│      Regras de Negócio Principais          │
├────────────────────────────────────────────┤
│ 1. Validação de Título                     │
│ 2. Unicidade Implícita (por índice)        │
│ 3. Imutabilidade de Tarefa Concluída       │
│ 4. Persistência durante Sessão             │
│ 5. Sem Relacionamentos entre Tarefas       │
│ 6. Estado Binário de Conclusão             │
│ 7. Ordem Preservada (FIFO)                 │
└────────────────────────────────────────────┘
```

---

## Validações Obrigatórias

### RN-VAL-001: Validação de Título

**Descrição**: O título de uma tarefa deve ser uma string não-vazia

**Regra**:
```python
titulo_limpo = titulo.strip()
assert len(titulo_limpo) > 0
```

**Implementação**:
```python
def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
    titulo_limpo = titulo.strip()
    if not titulo_limpo:
        raise ValueError("O título da tarefa não pode estar vazio.")
    # ...
```

**Casos de Teste**:

| Entrada | Resultado | Motivo |
|---|---|---|
| "Fazer compras" | ✅ Válido | Não vazio |
| "   " | ❌ Inválido | Apenas espaços |
| "" | ❌ Inválido | String vazia |
| " Estudar " | ✅ Válido | Strip remove espaços |
| "A" | ✅ Válido | Caractere único |
| "Tarefa muito longa com..." | ✅ Válido | Sem limite de comprimento |

**Camadas de Validação**:
1. **UI Layer** (`app.py`): `if nova_tarefa.strip():`
2. **Core Layer** (`gerenciador.py`): Exceção `ValueError`
3. **Tratamento** (`app.py`): Captura e exibe erro

---

### RN-VAL-002: Validação de Índice

**Descrição**: O índice deve estar dentro do intervalo válido da lista

**Regra**:
```python
assert 0 <= indice < len(self._tarefas)
```

**Implementação**:
```python
def marcar_como_concluida(self, indice: int) -> Dict[str, object]:
    if indice < 0 or indice >= len(self._tarefas):
        raise IndexError("Índice da tarefa inválido.")
    # ...
```

**Casos de Teste** (com lista de 3 tarefas):

| Índice | Resultado | Motivo |
|---|---|---|
| 0 | ✅ Válido | Primeira tarefa |
| 1 | ✅ Válido | Segunda tarefa |
| 2 | ✅ Válido | Última tarefa |
| 3 | ❌ Inválido | Fora do intervalo (>= len) |
| -1 | ❌ Inválido | Índice negativo |
| -5 | ❌ Inválido | Índice negativo |

---

### RN-VAL-003: Type Validation (Implícita)

**Descrição**: Os campos devem respeitar seus tipos definidos

**Regra**:
```python
titulo: str       # Deve ser string
concluida: bool   # Deve ser boolean
indice: int       # Deve ser inteiro
```

**Implementação**: Python type hints + verificação em runtime (opcional)

```python
def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
    """Type hints indicam tipos esperados."""
    if not isinstance(titulo, str):
        raise TypeError("Título deve ser string")
```

---

## Constraints de Dados

### RN-CON-001: Título Sempre Normalizado

**Descrição**: Títulos são sempre armazenados com trim (espaços removidos)

**Regra**:
```python
titulo_armazenado = titulo_entrada.strip()
```

**Garantia**: Nenhuma tarefa será criada com espaços em branco no início/fim

**Exemplo**:
```python
entrada = "  Estudar Python  "
armazenado = "Estudar Python"  # Espaços removidos
```

---

### RN-CON-002: Campo concluida Sempre Binário

**Descrição**: O campo `concluida` só pode ser `True` ou `False`

**Regra**:
```python
concluida: bool  # Não pode ser None, int, str, etc.
```

**Garantia**: Valores iniciais = `False`, após conclusão = `True`

---

### RN-CON-003: Tarefa Sem Duplicação de Índice

**Descrição**: Cada tarefa na lista tem um índice único

**Regra**:
```python
para cada i em range(len(tarefas)):
    tarefas[i] tem índice único i
```

**Implementação**: Armazenamento em List garante índices únicos por posição

---

### RN-CON-004: Não Há Campos Obrigatórios Faltantes

**Descrição**: Toda tarefa criada DEVE ter `titulo` E `concluida`

**Regra**:
```python
tarefa = {
    "titulo": str (obrigatório),
    "concluida": bool (obrigatório)
}
```

**Garantia**: Nenhuma tarefa existe sem ambos os campos

---

## Políticas de Estado

### RN-EST-001: Estado Inicial de Tarefa

**Descrição**: Toda tarefa criada inicia com `concluida = False`

**Regra**:
```python
nova_tarefa = {
    "titulo": titulo_limpo,
    "concluida": False  # Sempre False na criação
}
```

**Implicação**: Usuário nunca pode criar uma tarefa já concluída

---

### RN-EST-002: Imutabilidade de Tarefa Concluída

**Descrição**: Uma tarefa concluída (`concluida=True`) permanece assim permanentemente

**Regra**:
```python
if tarefa["concluida"] == True:
    tarefa["concluida"] = True  # Não há operação de "desmarcar"
```

**Implicação**: Não há rollback ou "desfazer" na conclusão

**Fluxo de Estados Permitido**:
```
False → True  ✅ Permitido
True → False  ❌ Não permitido
True → True   ✅ Permitido (idempotente)
```

---

### RN-EST-003: Não Há Estado Intermediário

**Descrição**: Uma tarefa está sempre em um dos dois estados: pendente ou concluída

**Regra**:
```python
concluida ∈ {True, False}  # Sem None, "Em Progresso", "Bloqueada", etc.
```

**Simplificação**: Modelo de dados é binário, sem complexidade de múltiplos estados

---

### RN-EST-004: Ordem de Inserção é Preservada

**Descrição**: Tarefas aparecem na lista na ordem em que foram criadas

**Regra**:
```python
tarefas = []  # List (não Set, não Dict)
self._tarefas.append(tarefa)  # Mantém ordem FIFO
```

**Implementação**: Use `List` (ordered) em vez de `Set` (unordered)

**Exemplo**:
```python
adicionar_tarefa("Tarefa A")  # índice 0
adicionar_tarefa("Tarefa B")  # índice 1
adicionar_tarefa("Tarefa C")  # índice 2

listar_tarefas() retorna [A, B, C]  # Ordem preservada
```

---

## Comportamento de Cache e Sessão

### RN-CACHE-001: Uma Instância por Sessão

**Descrição**: A aplicação mantém exatamente UMA instância do `GerenciadorTarefas` por sessão Streamlit

**Implementação**:
```python
@st.cache_resource
def inicializar_gestor() -> GerenciadorTarefas:
    """Cria instância única na sessão."""
    return GerenciadorTarefas()
```

**Garantia**: 
- Primeira execução: Cria novo gerenciador
- Execuções subsequentes: Reutiliza a mesma instância
- Dados persistem entre reloads da página

---

### RN-CACHE-002: Persistência Limitada à Sessão

**Descrição**: Dados existem apenas durante a sessão ativa do navegador

**Regra**:
```
Sessão Ativa → Dados na Memória → Sessão Encerra → Dados Perdidos
```

**Implicações**:
- ✅ Dados persistem ao recarregar a página
- ✅ Dados persistem ao mudar de aba e voltar
- ❌ Dados são perdidos ao fechar a aba
- ❌ Dados não persistem entre diferentes usuários

---

### RN-CACHE-003: Compartilhamento de Instância

**Descrição**: Uma única instância é compartilhada entre todos os reruns

**Fluxo**:
```
1º rerun:  inicializar_gestor() → Cria novo
2º rerun:  inicializar_gestor() → Reutiliza do cache
3º rerun:  inicializar_gestor() → Reutiliza do cache
...
```

**Efeito**: Modificações em um rerun são visíveis no próximo

---

## Regras de Transição

### RN-TRANS-001: Adicionar Tarefa Sempre Retorna Tarefa Criada

**Regra**:
```python
retorno = adicionar_tarefa(titulo)
assert retorno["titulo"] == titulo.strip()
assert retorno["concluida"] == False
assert isinstance(retorno, dict)
```

---

### RN-TRANS-002: Listar Tarefas Retorna Cópia (Deep Safety)

**Regra**:
```python
tarefas_retornadas = listar_tarefas()
tarefas_retornadas[0]["titulo"] = "Modificada"
tarefas_internas = listar_tarefas()
assert tarefas_internas[0]["titulo"] != "Modificada"
```

**Implementação**:
```python
def listar_tarefas(self) -> List[Dict[str, object]]:
    return self._tarefas.copy()  # Retorna cópia shallow
```

**Nota**: Cópia shallow é suficiente porque dicts são copiados

---

### RN-TRANS-003: Marcar Concluída é Idempotente

**Regra**:
```python
marcar_como_concluida(0)
marcar_como_concluida(0)  # Segunda chamada não muda nada
# tarefa ainda tem concluida=True
```

**Benefício**: Chamadas duplicadas não causam erro

---

## Tratamento de Casos Especiais

### RN-ESPEC-001: Tarefa com Caracteres Especiais

**Regra**: Qualquer caractere Unicode é permitido no título

**Casos Válidos**:
```python
"Comprar café @ Starbucks"  # ✅
"Implementar #feature"       # ✅
"Reunião 15:30 (sala 201)"  # ✅
"Checar email [IMPORTANTE]" # ✅
"Tarefa em português: çáéíóú" # ✅
"😀 Tarefa com emoji"        # ✅
```

---

### RN-ESPEC-002: Tarefa com Espaços Múltiplos Internos

**Regra**: Espaços internos são preservados, apenas trim é aplicado

**Exemplo**:
```python
entrada = "  Tarefa   com    espaços  "
armazenado = "Tarefa   com    espaços"
# Espaços internos mantêm, apenas trim em bordas
```

---

### RN-ESPEC-003: Lista Vazia

**Regra**: Uma lista vazia é um estado válido e esperado

**Comportamento**:
```python
gestor = GerenciadorTarefas()
tarefas = gestor.listar_tarefas()  # []
len(tarefas) == 0  # True
# Não há erro, é estado normal
```

---

### RN-ESPEC-004: Limpar Tarefas em Lista Já Vazia

**Regra**: Limpar uma lista já vazia não causa erro

**Comportamento**:
```python
gestor = GerenciadorTarefas()
gestor.limpar_tarefas()  # OK, sem erro
# Lista permanece vazia
```

---

## Políticas de Integridade

### RN-INT-001: Integridade Referencial

**Descrição**: Índices usados para referenciar tarefas devem sempre ser válidos

**Regra**: Antes de usar um índice, validar:
```python
if 0 <= indice < len(self._tarefas):
    # Seguro usar
else:
    raise IndexError(...)
```

---

### RN-INT-002: Imutabilidade da Estrutura Interna

**Descrição**: Usuários não devem modificar `_tarefas` diretamente

**Padrão**:
```python
# ❌ Não fazer
tarefas = gestor.listar_tarefas()
tarefas.append(...)  # Modificar lista retornada

# ✅ Fazer
gestor.adicionar_tarefa(...)  # Use métodos da API
```

**Garantia**: API pública (`adicionar_tarefa`, etc.) é ponto único de entrada

---

### RN-INT-003: Validação em Múltiplas Camadas

**Arquitetura**:
```
UI Layer (app.py)
├─ Validação básica
├─ Feedback visual
└─ Chamada ao Core

Core Layer (gerenciador.py)
├─ Validação completa
├─ Lógica de negócio
└─ Exceções

Handler Layer (app.py)
├─ Captura exceções
└─ Mensagens ao usuário
```

**Exemplo - Adicionar Tarefa**:
```
1. UI: if nova_tarefa.strip():          # Validação 1
2. Core: if not titulo_limpo:           # Validação 2
         raise ValueError(...)
3. Handler: try/except + st.error()     # Tratamento
```

---

### RN-INT-004: Atomicidade de Operações

**Descrição**: Cada operação é atômica (completa ou falha totalmente)

**Garantia**: Não há estado intermediário

**Exemplo**:
```python
# Operação: adicionar_tarefa("Nova")
# Resultado 1: Sucesso - tarefa criada e adicionada
# Resultado 2: Falha - ValueError lançada, nada adicionado
# NÃO HÁ: Tarefa criada mas não adicionada
```

---

## Matriz de Validação Completa

| Operação | Entrada | Validação 1 | Validação 2 | Sucesso | Erro |
|---|---|---|---|---|---|
| **Criar Tarefa** | titulo:str | UI: trim | Core: não vazio | Dict criado | ValueError |
| **Listar Tarefas** | - | - | - | List retornada | - |
| **Marcar Concluída** | indice:int | - | Core: valid range | Tarefa atualizada | IndexError |
| **Limpar Tarefas** | - | - | - | Lista vazia | - |

---

## Resumo de Regras Críticas

| Regra ID | Descrição | Impacto |
|---|---|---|
| RN-VAL-001 | Título não vazio | Previne dados inválidos |
| RN-VAL-002 | Índice válido | Previne acesso indevido |
| RN-EST-002 | Tarefa concluída é permanente | Define workflow irreversível |
| RN-CACHE-001 | Uma instância por sessão | Garante persistência |
| RN-CACHE-002 | Persistência limitada a sessão | Define escopo de dados |
| RN-INT-001 | Integridade referencial | Garante consistência |
| RN-INT-003 | Validação em camadas | Defesa em profundidade |

---

**Última Atualização**: 2026-09-01  
**Versão**: 1.0  
**Autor**: Documentação Técnica
