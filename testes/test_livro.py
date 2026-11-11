import unittest
from modelos.livro import Livro

class TestLivro(unittest.TestCase):
    def setUp(self):
      self.livro = Livro(
          1,
          "O Pequeno Príncipe",
          "Antoine de Saint-Exupéry",
          "Literatura infantil",
          1943,
          96
      )

    def test_criar_livro(self):
        self.assertEqual(self.livro.id, 1)
        self.assertEqual(self.livro.titulo, "O Pequeno Príncipe")
        self.assertEqual(self.livro.autor, "Antoine de Saint-Exupéry")
        self.assertEqual(self.livro.genero, "Literatura infantil")
        self.assertEqual(self.livro.ano, 1943)
        self.assertEqual(self.livro.numero_paginas, 96)

    def test_numero_paginas_padrao(self):
        livro = Livro(
            2,
            "A Revolução dos Bichos",
            "George Orwell",
            "Fábula",
            1945
        )
        self.assertEqual(livro.numero_paginas, 0)

    def test_para_dict(self):
        dados = self.livro.para_dict()

        esperado = {
              "id": 1,
              "titulo": "O Pequeno Príncipe",
              "autor": "Antoine de Saint-Exupéry",
              "genero": "Literatura infantil",
              "ano": 1943,
              "numero_paginas": 96
        }

        self.assertEqual(dados, esperado)

    def test_str(self):
        resultado = str(self.livro)

        self.assertIn("O Pequeno Príncipe", resultado)
        self.assertIn("Antoine de Saint-Exupéry", resultado)
        self.assertIn("1943", resultado)
        self.assertIn("Literatura infantil", resultado)
        self.assertIn("[1]", resultado)
if __name__ == "__main__":
    unittest.main()
  

