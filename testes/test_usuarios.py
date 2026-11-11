import unittest
from modelos.usuario import Usuario


class UsuarioTeste(Usuario):

    def tipo(self):
        return "leitor"

    def menu(self):
        pass


class TestUsuario(unittest.TestCase):

    def setUp(self):
        self.usuario = UsuarioTeste(
            1,
            "Maria",
            " maria@email.com ",
            "123456"
        )

    def test_inicializacao(self):
        self.assertEqual(self.usuario.id, 1)
        self.assertEqual(self.usuario.nome, "Maria")
        self.assertEqual(self.usuario.email, "maria@email.com")

    def test_fazer_login(self):
        self.assertTrue(
            self.usuario.fazer_login("maria@email.com", "123456")
        )

    def test_login_com_email_maiusculo(self):
        self.assertTrue(
            self.usuario.fazer_login("MARIA@EMAIL.COM", "123456")
        )

    def test_login_com_senha_incorreta(self):
        self.assertFalse(
            self.usuario.fazer_login("maria@email.com", "senhaerrada")
        )

    def test_login_com_email_incorreto(self):
        self.assertFalse(
            self.usuario.fazer_login("outro@email.com", "123456")
        )

    def test_alterar_senha(self):
        self.usuario.alterar_senha("654321")

        self.assertTrue(
            self.usuario.fazer_login("maria@email.com", "654321")
        )

    def test_impedir_senha_vazia(self):
        with self.assertRaises(ValueError):
            self.usuario.alterar_senha("")

    def test_para_dict(self):
        dados = self.usuario.para_dict()

        self.assertEqual(dados["id"], 1)
        self.assertEqual(dados["tipo"], "leitor")
        self.assertEqual(dados["nome"], "Maria")
        self.assertEqual(dados["email"], "maria@email.com")
        self.assertEqual(dados["senha"], "123456")

    def test_str(self):
        self.assertEqual(str(self.usuario), "Maria (leitor)")

    def test_usuario_e_abstrato(self):
        with self.assertRaises(TypeError):
            Usuario(1, "Maria", "maria@email.com", "123456")


if __name__ == "__main__":
    unittest.main()
