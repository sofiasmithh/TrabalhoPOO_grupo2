import unittest
from abc import ABC, abstractmethod

from modelos.usuario import Usuario  

class Leitor(Usuario):
    def tipo(self):
        return "leitor"

    def menu(self):
        return "Menu Leitor"


class Administrador(Usuario):
    def tipo(self):
        return "administrador"

    def menu(self):
        return "Menu Administrador"


class BancoDeDadosMock:
    def __init__(self):
        self.usuarios = []

    def carregar_usuarios(self):
        return self.usuarios

    def salvar_usuarios(self, usuarios):
        self.usuarios = usuarios


class TestUsuario(unittest.TestCase):

    def setUp(self):
        self.banco = BancoDeDadosMock()

    def test_nao_pode_instanciar_usuario_diretamente(self):
        with self.assertRaises(TypeError):
            Usuario(1, "Teste", "teste@email.com", "123")

    def test_criacao_e_getters_leitor(self):
        leitor = Leitor(1, "  Maria Silva  ", "  MARIA@Email.com ", "senha123")
        
        self.assertEqual(leitor.id, 1)
        self.assertEqual(leitor.nome, "Maria Silva")
        self.assertEqual(leitor.email, "maria@email.com")
        self.assertEqual(leitor.tipo(), "leitor")

    def test_fazer_login_sucesso_e_falha(self):
        usuario = Administrador(2, "Carlos Admin", "carlos@email.com", "adminpass")
        
        self.assertTrue(usuario.fazer_login("  CARLOS@email.com ", "adminpass"))
        
        self.assertFalse(usuario.fazer_login("carlos@email.com", "senhaerrada"))
        
        self.assertFalse(usuario.fazer_login("outro@email.com", "adminpass"))

    def test_alterar_senha(self):
        user = Leitor(3, "Ana", "ana@email.com", "senha1")
        
        user.alterar_senha("novaSenha123")
        self.assertTrue(user.fazer_login("ana@email.com", "novaSenha123"))

        with self.assertRaises(ValueError):
            user.alterar_senha("")
            
        with self.assertRaises(ValueError):
            user.alterar_senha("   ")

    def test_cadastrar_usuario_sucesso(self):
        novo_leitor = Leitor.cadastrar(self.banco, 10, "João Pedro", "joao@email.com", "abc456")
        
        self.assertIsInstance(novo_leitor, Leitor)
        self.assertEqual(len(self.banco.carregar_usuarios()), 1)
        self.assertEqual(self.banco.carregar_usuarios()[0]["email"], "joao@email.com")

    def test_cadastrar_email_duplicado_lanca_erro(self):
        Leitor.cadastrar(self.banco, 1, "Usuário Um", "teste@email.com", "123")
        
        with self.assertRaises(ValueError):
            Administrador.cadastrar(self.banco, 2, "Usuário Dois", " TESTE@email.com ", "456")

    def test_para_dict(self):
        admin = Administrador(5, "Diretor", "diretor@email.com", "secret")
        dicionario = admin.para_dict()
        
        self.assertEqual(dicionario["id"], 5)
        self.assertEqual(dicionario["tipo"], "administrador")
        self.assertEqual(dicionario["nome"], "Diretor")
        self.assertEqual(dicionario["email"], "diretor@email.com")
        self.assertEqual(dicionario["senha"], "secret")


if __name__ == "__main__":
    unittest.main()
