"""Testes unitários para o gerenciador de tarefas."""

from app.src.gerenciador_tarefas.gerenciador import GerenciadorTarefas


def test_adicionar_tarefa():
    """Deve adicionar uma nova tarefa com status pendente."""
    gestor = GerenciadorTarefas()

    gestor.adicionar_tarefa("Estudar Python")

    tarefas = gestor.listar_tarefas()
    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Estudar Python"
    assert tarefas[0]["concluida"] is False


def test_marcar_tarefa_como_concluida():
    """Deve atualizar a tarefa para concluída."""
    gestor = GerenciadorTarefas()
    gestor.adicionar_tarefa("Revisar PR")

    gestor.marcar_como_concluida(0)

    tarefas = gestor.listar_tarefas()
    assert tarefas[0]["concluida"] is True
