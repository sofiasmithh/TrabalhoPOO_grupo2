import unittest

from modelos.leitura import Leitura
from modelos.livro import Livro

class TestLeitura(unittest.TestCase):
  def setUp(self):
      self.livro = Livro(
          1,
          "O Pequeno Principe",
          "Antonio de Saint-Exupéry",
          "Literatura infantil",
          1943,
          96
      )

      self.leitura = Leitura(
          self.livro,
          "Lendo",
          False,
          4,
          "Livro muito interessante."
      )

  def test_criar_leitura(self):
      self.assertEqual(self.leitura.livro, self.livro)
      self.assertEqual(self.leitura.status, "Lendo")
      self.assertFalse(self.leitura.favorito)
      self.assertEqual(self.leitura.avaliacao, 4)
      self.assertEqual(
          self.leitura.resenha,
          "Livro muito interessante."
      )

  def test_status_padrao(self):
      leitura = Leitura(self.livro)
    
      self.assertEqual(leitura.status, "Quero ler")

  def test_favorito_padrao(self):
      leitura = Leitura(self.livro)

      self.assertFalse(leitura.favorito)

  def test_avaliacao_padrao(self):
      leitura = Leitura(self.livro)

      self.assertEqual(leitura.avaliacao, 0)

  def test_resenha_padrao(self):
      leitura = Leitura(self.livro)

      self.assertEqual(leitura.resenha, "")

  def test_para_dict(self):
      dados = self.leitura.para_dict()

      esperado = {
          "livro_id": 1,
          "status": "Lendo",
          "favorito": False,
          "avaliacao": 4,
          "resenha": "Livro muito interessante."
      }

      self.assertEqual(dados, esperado)

  def test_para_dict_com_livro_id(self):
      leitura = Leitura(10)

      dados = leitura.para_dict()

      self.assertEqual(dados["livro_id"], 10)

  def test_str(self):
      resultado = str(self.leitura)

      self.assertIn("Dom Casmurro", resultado)
      self.assertIn("Lendo", resultado)
      self.assertIn("4/5", resultado)

  def test_str_com_favorito(self):
      leitura = Leitura(self.livro, favorito=True)

      resultado = str(leitura)

      self.assertIn("[Favorito]", resultado)
if __name__ == __"main"__:
    unittest.main()
