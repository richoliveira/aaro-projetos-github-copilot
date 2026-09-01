"""Aplicação de console para testar o CRUD de cadastro de pessoas."""

from __future__ import annotations

from .cadastro_pessoas import CadastroPessoas
from .pessoa import Pessoa


class ConsoleApp:
    """Controla o menu interativo do cadastro de pessoas no console."""

    def __init__(self) -> None:
        """Inicializa a aplicação com um cadastro em memória."""
        self._cadastro = CadastroPessoas()

    def exibir_menu(self) -> None:
        """Exibe o menu principal da aplicação."""
        print("\n=== CRUD de Cadastro de Pessoas ===")
        print("1. Cadastrar pessoa")
        print("2. Listar pessoas")
        print("3. Buscar pessoa")
        print("4. Atualizar pessoa")
        print("5. Remover pessoa")
        print("0. Sair")

    def cadastrar_pessoa(self) -> None:
        """Coleta dados e adiciona uma nova pessoa."""
        nome = input("Nome: ").strip()
        idade_input = input("Idade: ").strip()

        try:
            idade = int(idade_input)
            pessoa = Pessoa(nome=nome, idade=idade)
            self._cadastro.adicionar(pessoa)
            print("Pessoa cadastrada com sucesso!")
        except ValueError as exc:
            print(f"Erro: {exc}")

    def listar_pessoas(self) -> None:
        """Lista todas as pessoas cadastradas."""
        pessoas = self._cadastro.listar()
        if not pessoas:
            print("Nenhuma pessoa cadastrada.")
            return

        print("\nPessoas cadastradas:")
        for pessoa in pessoas:
            print(f"- {pessoa}")

    def buscar_pessoa(self) -> None:
        """Busca uma pessoa pelo nome e exibe o resultado."""
        nome = input("Digite o nome da pessoa: ").strip()
        pessoa = self._cadastro.buscar_por_nome(nome)

        if pessoa is None:
            print("Pessoa não encontrada.")
            return

        print(f"Pessoa encontrada: {pessoa}")

    def atualizar_pessoa(self) -> None:
        """Atualiza os dados de uma pessoa existente."""
        nome_atual = input("Nome atual da pessoa: ").strip()
        novo_nome = input("Novo nome: ").strip()
        nova_idade_input = input("Nova idade: ").strip()

        try:
            nova_idade = int(nova_idade_input)
            pessoa = self._cadastro.atualizar(nome_atual, novo_nome, nova_idade)
            print(f"Pessoa atualizada com sucesso: {pessoa}")
        except ValueError as exc:
            print(f"Erro: {exc}")

    def remover_pessoa(self) -> None:
        """Remove uma pessoa do cadastro."""
        nome = input("Digite o nome da pessoa a ser removida: ").strip()
        try:
            pessoa_removida = self._cadastro.remover(nome)
            print(f"Pessoa removida: {pessoa_removida}")
        except ValueError as exc:
            print(f"Erro: {exc}")

    def executar(self) -> None:
        """Executa o loop principal do menu do console."""
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.cadastrar_pessoa()
            elif opcao == "2":
                self.listar_pessoas()
            elif opcao == "3":
                self.buscar_pessoa()
            elif opcao == "4":
                self.atualizar_pessoa()
            elif opcao == "5":
                self.remover_pessoa()
            elif opcao == "0":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    console = ConsoleApp()
    console.executar()
