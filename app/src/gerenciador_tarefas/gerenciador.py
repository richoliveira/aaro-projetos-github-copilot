"""Módulo responsável pela lógica do gerenciador de tarefas."""

from __future__ import annotations

from typing import Dict, List


class GerenciadorTarefas:
    """Gerencia a criação, listagem e conclusão de tarefas.

    A classe mantém uma lista em memória para representar as tarefas criadas
    durante a execução do aplicativo. A estrutura foi pensada para facilitar a
    demonstração em sala de aula e a manutenção simples do código.
    """

    def __init__(self) -> None:
        """Inicializa o gerenciador com uma lista vazia de tarefas."""
        self._tarefas: List[Dict[str, object]] = []

    def adicionar_tarefa(self, titulo: str) -> Dict[str, object]:
        """Adiciona uma nova tarefa ao sistema.

        Args:
            titulo: Nome da tarefa que será registrada.

        Returns:
            Dicionário contendo os dados da tarefa criada.

        Raises:
            ValueError: Quando o título da tarefa estiver vazio ou em branco.
        """
        titulo_limpo = titulo.strip()
        if not titulo_limpo:
            raise ValueError("O título da tarefa não pode estar vazio.")

        tarefa = {"titulo": titulo_limpo, "concluida": False}
        self._tarefas.append(tarefa)
        return tarefa

    def listar_tarefas(self) -> List[Dict[str, object]]:
        """Retorna a lista completa de tarefas cadastradas.

        Returns:
            Lista de dicionários com as tarefas e seus estados.
        """
        return self._tarefas.copy()

    def marcar_como_concluida(self, indice: int) -> Dict[str, object]:
        """Marca uma tarefa específica como concluída.

        Args:
            indice: Posição da tarefa na lista.

        Returns:
            Dicionário da tarefa atualizada.

        Raises:
            IndexError: Quando o índice informado estiver fora do alcance.
        """
        if indice < 0 or indice >= len(self._tarefas):
            raise IndexError("Índice da tarefa inválido.")

        tarefa = self._tarefas[indice]
        tarefa["concluida"] = True
        return tarefa

    def limpar_tarefas(self) -> None:
        """Remove todas as tarefas da memória."""
        self._tarefas.clear()
