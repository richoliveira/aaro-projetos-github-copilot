"""Testes unitários para o módulo de CRUD de cadastro de pessoas."""

import pytest

from app.src.crud_cadastro.cadastro_pessoas import CadastroPessoas
from app.src.crud_cadastro.console_app import ConsoleApp
from app.src.crud_cadastro.pessoa import Pessoa


def test_pessoa_criada_com_dados_validos():
    """Deve criar uma pessoa com nome e idade válidos."""
    pessoa = Pessoa(nome="Maria Silva", idade=30)

    assert pessoa.nome == "Maria Silva"
    assert pessoa.idade == 30
    assert str(pessoa) == "Maria Silva - 30 anos"


def test_pessoa_rejeita_nome_vazio():
    """Deve rejeitar nomes vazios."""
    with pytest.raises(ValueError, match="nome da pessoa"):
        Pessoa(nome="   ", idade=18)


def test_pessoa_rejeita_idade_negativa():
    """Deve rejeitar idades negativas."""
    with pytest.raises(ValueError, match="idade"):
        Pessoa(nome="João", idade=-1)


def test_cadastro_adiciona_pessoa_nova():
    """Deve adicionar uma pessoa ao cadastro."""
    cadastro = CadastroPessoas()
    pessoa = Pessoa(nome="Ana", idade=25)

    cadastro.adicionar(pessoa)

    assert len(cadastro) == 1
    assert cadastro.listar()[0].nome == "Ana"


def test_cadastro_nao_permite_nome_duplicado():
    """Deve impedir cadastro duplicado com mesmo nome."""
    cadastro = CadastroPessoas()
    cadastro.adicionar(Pessoa(nome="Carlos", idade=41))

    with pytest.raises(ValueError, match="já está cadastrada"):
        cadastro.adicionar(Pessoa(nome="carlos", idade=35))


def test_cadastro_busca_pessoa_por_nome():
    """Deve localizar pessoa pelo nome informado."""
    cadastro = CadastroPessoas()
    cadastro.adicionar(Pessoa(nome="Beatriz", idade=28))

    pessoa = cadastro.buscar_por_nome("beatriz")

    assert pessoa is not None
    assert pessoa.idade == 28
    assert cadastro.buscar_por_nome("Inexistente") is None


def test_cadastro_atualiza_dados_da_pessoa():
    """Deve atualizar nome e idade de uma pessoa cadastrada."""
    cadastro = CadastroPessoas()
    cadastro.adicionar(Pessoa(nome="Daniel", idade=21))

    pessoa = cadastro.atualizar("daniel", "Daniel Martins", 22)

    assert pessoa.nome == "Daniel Martins"
    assert pessoa.idade == 22
    assert cadastro.buscar_por_nome("Daniel Martins").idade == 22


def test_cadastro_atualiza_rejeita_dados_invalidos():
    """Deve rejeitar atualizações com dados inválidos."""
    cadastro = CadastroPessoas()
    cadastro.adicionar(Pessoa(nome="Eduardo", idade=33))

    with pytest.raises(ValueError, match="não encontrada"):
        cadastro.atualizar("Inexistente", "Novo Nome", 25)

    with pytest.raises(ValueError, match="novo nome"):
        cadastro.atualizar("Eduardo", "   ", 30)

    with pytest.raises(ValueError, match="nova idade"):
        cadastro.atualizar("Eduardo", "Eduardo Novo", -1)


def test_cadastro_remove_pessoa():
    """Deve remover uma pessoa existente do cadastro."""
    cadastro = CadastroPessoas()
    cadastro.adicionar(Pessoa(nome="Fernanda", idade=27))

    pessoa_removida = cadastro.remover("fernanda")

    assert pessoa_removida.nome == "Fernanda"
    assert len(cadastro) == 0


def test_cadastro_remove_ve_pessoa_nao_encontrada():
    """Deve rejeitar remoção de pessoa inexistente."""
    cadastro = CadastroPessoas()

    with pytest.raises(ValueError, match="não encontrada"):
        cadastro.remover("NaoExiste")


def test_console_app_cadastra_pessoa(monkeypatch, capsys):
    """Deve cadastrar pessoa via input do console."""
    app = ConsoleApp()
    entradas = iter(["Maria", "25"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(entradas))

    app.cadastrar_pessoa()

    captured = capsys.readouterr()
    assert "Pessoa cadastrada com sucesso!" in captured.out
    assert len(app._cadastro) == 1


def test_console_app_lista_pessoas_vazias(capsys):
    """Deve informar que não há pessoas cadastradas."""
    app = ConsoleApp()

    app.listar_pessoas()

    captured = capsys.readouterr()
    assert "Nenhuma pessoa cadastrada." in captured.out


def test_console_app_busca_pessoa(monkeypatch, capsys):
    """Deve buscar pessoa no cadastro."""
    app = ConsoleApp()
    app._cadastro.adicionar(Pessoa(nome="Gabriel", idade=31))
    monkeypatch.setattr("builtins.input", lambda prompt="": "gabriel")

    app.buscar_pessoa()

    captured = capsys.readouterr()
    assert "Pessoa encontrada" in captured.out


def test_console_app_atualiza_pessoa(monkeypatch, capsys):
    """Deve atualizar pessoa via console."""
    app = ConsoleApp()
    app._cadastro.adicionar(Pessoa(nome="Helena", idade=24))
    entradas = iter(["Helena", "Helena Souza", "26"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(entradas))

    app.atualizar_pessoa()

    captured = capsys.readouterr()
    assert "Pessoa atualizada com sucesso" in captured.out
    assert app._cadastro.buscar_por_nome("Helena Souza").idade == 26


def test_console_app_remove_pessoa(monkeypatch, capsys):
    """Deve remover pessoa via console."""
    app = ConsoleApp()
    app._cadastro.adicionar(Pessoa(nome="Igor", idade=40))
    monkeypatch.setattr("builtins.input", lambda prompt="": "igor")

    app.remover_pessoa()

    captured = capsys.readouterr()
    assert "Pessoa removida" in captured.out
    assert len(app._cadastro) == 0


def test_console_app_executa_menu_e_sai(monkeypatch, capsys):
    """Deve executar o menu e encerrar ao escolher sair."""
    app = ConsoleApp()
    respostas = iter(["0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(respostas))

    app.executar()

    captured = capsys.readouterr()
    assert "=== CRUD de Cadastro de Pessoas ===" in captured.out
    assert "Encerrando o sistema" in captured.out
