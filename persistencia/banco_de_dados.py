
import json
import os


class BancoDeDados:
    def __init__(self):
        raiz = os.path.dirname(os.path.dirname(__file__))
        pasta_dados = os.path.join(raiz, "dados")

        os.makedirs(pasta_dados, exist_ok=True)

        self.arquivo_catalogo = os.path.join(
            pasta_dados, "catalogo.json"
        )

        self.arquivo_usuarios = os.path.join(
            pasta_dados, "usuarios.json"
        )

        self.arquivo_leituras = os.path.join(
            pasta_dados, "leituras.json"
        )

        self.criar_arquivos()

    def criar_arquivos(self):
        arquivos = [
            self.arquivo_catalogo,
            self.arquivo_usuarios,
            self.arquivo_leituras
        ]

        for caminho in arquivos:
            if not os.path.exists(caminho):
                with open(caminho, "w", encoding="utf-8") as arquivo:
                    json.dump(
                        [], arquivo, ensure_ascii=False, indent=4
                    )

    def carregar_dados(self, caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def salvar_dados(self, caminho, dados):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados, arquivo, ensure_ascii=False, indent=4
            )

    def carregar_catalogo(self):
        return self.carregar_dados(self.arquivo_catalogo)

    def salvar_catalogo(self, livros):
        self.salvar_dados(self.arquivo_catalogo, livros)

    def carregar_usuarios(self):
        return self.carregar_dados(self.arquivo_usuarios)

    def salvar_usuarios(self, usuarios):
        self.salvar_dados(self.arquivo_usuarios, usuarios)

    def carregar_leituras(self):
        return self.carregar_dados(self.arquivo_leituras)

    def salvar_leituras(self, leituras):
        self.salvar_dados(self.arquivo_leituras, leituras)
