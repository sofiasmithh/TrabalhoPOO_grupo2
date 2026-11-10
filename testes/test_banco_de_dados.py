
import unittest
import json
import tempfile
import os

from persistencia.banco_de_dados import BancoDeDados


class TestBancoDeDados(unittest.TestCase):
    def setUp(self):
        self.pasta_temporaria = tempfile.TemporaryDirectory()
        self.pasta_dados = os.path.join(
            self.pasta_temporaria.name, "dados"
        )
        os.makedirs(self.pasta_dados)

        self.banco = BancoDeDados.__new__(BancoDeDados)

        self.banco.arquivo_catalogo = os.path.join(
            self.pasta_dados, "catalogo.json"
        )
        self.banco.arquivo_usuarios = os.path.join(
            self.pasta_dados, "usuarios.json"
        )
        self.banco.arquivo_leituras = os.path.join(
            self.pasta_dados, "leituras.json"
        )

        self.banco.criar_arquivos()

    def tearDown(self):
        self.pasta_temporaria.cleanup()

    def test_criar_arquivos(self):
        self.assertTrue(os.path.exists(self.banco.arquivo_catalogo))
        self.assertTrue(os.path.exists(self.banco.arquivo_usuarios))
        self.assertTrue(os.path.exists(self.banco.arquivo_leituras))

    def test_arquivos_iniciam_vazios(self):
        self.assertEqual(self.banco.carregar_catalogo(), [])
        self.assertEqual(self.banco.carregar_usuarios(), [])
        self.assertEqual(self.banco.carregar_leituras(), [])

    def test_salvar_e_carregar_catalogo(self):
        livros = [
            {
                "id": 1,
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "genero": "Romance",
                "ano": 1899,
                "numero_paginas": 256
            }
        ]

        self.banco.salvar_catalogo(livros)

        self.assertEqual(self.banco.carregar_catalogo(), livros)

    def test_salvar_e_carregar_usuarios(self):
        usuarios = [
            {
                "id": 1,
                "nome": "Ana",
                "email": "ana@email.com"
            }
        ]

        self.banco.salvar_usuarios(usuarios)

        self.assertEqual(self.banco.carregar_usuarios(), usuarios)

    def test_salvar_e_carregar_leituras(self):
        leituras = [
            {
                "tipo": "meta",
                "leitor_id": 1,
                "meta_anual": 12
            }
        ]

        self.banco.salvar_leituras(leituras)

        self.assertEqual(self.banco.carregar_leituras(), leituras)

    def test_salvar_dados_json(self):
        dados = [{"nome": "José"}]

        self.banco.salvar_dados(
            self.banco.arquivo_usuarios, dados
        )

        with open(
            self.banco.arquivo_usuarios, "r", encoding="utf-8"
        ) as arquivo:
            dados_salvos = json.load(arquivo)

        self.assertEqual(dados_salvos, dados)


if __name__ == "__main__":
    unittest.main(verbosity=2)

