"""Define a entidade Pessoa para o cadastro simples."""

from dataclasses import dataclass


@dataclass
class Pessoa:
    """Representa uma pessoa cadastrada no sistema.

    Attributes:
        nome: Nome completo da pessoa.
        idade: Idade da pessoa em anos.
    """

    nome: str
    idade: int

    def __post_init__(self) -> None:
        """Valida os dados da pessoa após a instanciação."""
        if not self.nome or not self.nome.strip():
            raise ValueError("O nome da pessoa não pode estar vazio.")
        if self.idade < 0:
            raise ValueError("A idade não pode ser negativa.")

    def __str__(self) -> str:
        """Retorna a representação textual da pessoa."""
        return f"{self.nome} - {self.idade} anos"
