"""Implementa o CRUD de cadastro de pessoas em memória."""

from __future__ import annotations

from typing import Dict, List, Optional

from .pessoa import Pessoa


class CadastroPessoas:
    """Gerencia o armazenamento e operações de CRUD em memória.

    A estrutura é simples para fins de demonstração e utiliza uma lista de
    objetos Pessoa como repositório em memória.
    """

    def __init__(self) -> None:
        """Inicializa o cadastro com uma lista vazia."""
        self._pessoas: List[Pessoa] = []

    def adicionar(self, pessoa: Pessoa) -> None:
        """Adiciona uma pessoa ao cadastro.

        Args:
            pessoa: Instância da classe Pessoa.

        Raises:
            ValueError: Se a pessoa não for válida ou já existir no cadastro.
        """
        if any(p.nome.lower() == pessoa.nome.lower() for p in self._pessoas):
            raise ValueError(f"A pessoa '{pessoa.nome}' já está cadastrada.")
        self._pessoas.append(pessoa)

    def listar(self) -> List[Pessoa]:
        """Retorna a lista de pessoas cadastradas.

        Returns:
            Lista de objetos Pessoa.
        """
        return self._pessoas.copy()

    def buscar_por_nome(self, nome: str) -> Optional[Pessoa]:
        """Busca uma pessoa pelo nome exato.

        Args:
            nome: Nome a ser pesquisado.

        Returns:
            Objeto Pessoa caso encontre, caso contrário None.
        """
        for pessoa in self._pessoas:
            if pessoa.nome.lower() == nome.strip().lower():
                return pessoa
        return None

    def atualizar(self, nome: str, novo_nome: str, nova_idade: int) -> Pessoa:
        """Atualiza os dados de uma pessoa existente.

        Args:
            nome: Nome atual da pessoa.
            novo_nome: Novo nome para a pessoa.
            nova_idade: Nova idade da pessoa.

        Returns:
            Pessoa atualizada.

        Raises:
            ValueError: Se a pessoa não for encontrada ou os dados forem inválidos.
        """
        pessoa = self.buscar_por_nome(nome)
        if pessoa is None:
            raise ValueError(f"Pessoa '{nome}' não encontrada.")

        if not novo_nome or not novo_nome.strip():
            raise ValueError("O novo nome não pode ficar vazio.")
        if nova_idade < 0:
            raise ValueError("A nova idade não pode ser negativa.")

        pessoa.nome = novo_nome.strip()
        pessoa.idade = nova_idade
        return pessoa

    def remover(self, nome: str) -> Pessoa:
        """Remove uma pessoa do cadastro.

        Args:
            nome: Nome da pessoa a ser removida.

        Returns:
            Pessoa removida.

        Raises:
            ValueError: Se a pessoa não for encontrada.
        """
        pessoa = self.buscar_por_nome(nome)
        if pessoa is None:
            raise ValueError(f"Pessoa '{nome}' não encontrada.")

        self._pessoas.remove(pessoa)
        return pessoa

    def __len__(self) -> int:
        """Retorna a quantidade de pessoas cadastradas."""
        return len(self._pessoas)
