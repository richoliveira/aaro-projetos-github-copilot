"""Aplicativo Streamlit para gerenciamento de tarefas.

Este arquivo foi pensado para ser simples, didático e fácil de demonstrar em
sala de aula. Ele reúne a interface com a lógica de negócios em um único ponto
de entrada, seguindo o desafio proposto.
"""

from __future__ import annotations

import streamlit as st

try:
    from .gerenciador import GerenciadorTarefas
except ImportError:  # pragma: no cover
    from gerenciador import GerenciadorTarefas


@st.cache_resource
def inicializar_gestor() -> GerenciadorTarefas:
    """Cria e mantém uma instância única do gerenciador na sessão do Streamlit.

    Returns:
        Instância reutilizada do gerenciador de tarefas.
    """
    return GerenciadorTarefas()


def renderizar_tarefa(tarefa: dict, indice: int) -> None:
    """Renderiza uma tarefa individual dentro da interface do Streamlit.

    Args:
        tarefa: Dicionário contendo o título e o status da tarefa.
        indice: Índice da tarefa na lista para controle visual.
    """
    titulo = tarefa["titulo"]
    concluida = tarefa["concluida"]

    with st.container():
        col_titulo, col_checkbox = st.columns([4, 1])
        with col_titulo:
            if concluida:
                st.markdown(f"<s>{indice + 1}. {titulo}</s>", unsafe_allow_html=True)
            else:
                st.write(f"{indice + 1}. {titulo}")
        with col_checkbox:
            tarefa_concluida = st.checkbox(
                "OK",
                key=f"check_{indice}",
                value=concluida,
                on_change=lambda: None,
            )
            if tarefa_concluida and not concluida:
                gestor = inicializar_gestor()
                gestor.marcar_como_concluida(indice)
                st.rerun()


def main() -> None:
    """Configura a interface principal e o fluxo do aplicativo."""
    st.set_page_config(page_title="Gerenciador de Tarefas", page_icon="✅")
    st.title("Gerenciador de Tarefas")

    gestor = inicializar_gestor()

    with st.form(key="form_nova_tarefa"):
        nova_tarefa = st.text_input(
            "Nova tarefa",
            placeholder="Digite o nome da tarefa...",
        )
        submit = st.form_submit_button("Adicionar tarefa")

        if submit:
            if nova_tarefa.strip():
                gestor.adicionar_tarefa(nova_tarefa)
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("Digite um nome para a tarefa antes de adicionar.")

    st.subheader("Lista de Tarefas")
    tarefas = gestor.listar_tarefas()

    if not tarefas:
        st.info("Nenhuma tarefa cadastrada ainda. Adicione sua primeira tarefa acima.")
        return

    for indice, tarefa in enumerate(tarefas):
        renderizar_tarefa(tarefa, indice)


if __name__ == "__main__":
    main()
