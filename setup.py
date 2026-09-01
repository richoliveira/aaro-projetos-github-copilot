"""Configuração do pacote do projeto."""

from setuptools import find_packages, setup

setup(
    name="gerenciador-tarefas-streamlit",
    version="0.1.0",
    description="Aplicativo de gerenciamento de tarefas com Streamlit.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.35.0",
    ],
    python_requires=">=3.8",
)
