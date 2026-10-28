from modelos.usuario import Usuario 

class Administrador(Usuario):
    
  def tipo(self):
    return "administrador"

  def menu(self):
    print("\n===== MENU DO ADMINISTRADOR =====")
    print("1 - Adicionar livro")
    print("2 - Remover livro")
    print("3 - Editar livro")
    print("4 - Listar livros")
    print("5 - Sair")

  def adicionar_livro(self, catalogo, livro):
    catalogo.adicionar_livro(
        livro,
        administrador=self
    )

  def remover_livro(self, catalogo, id_livro):
    catalogo.remover_livro(
        id_livro,
        administrador=self
    )

  def editar_livro(self, catalogo, id_livro, **alteracoes):
    catalogo.editar_livro(
        id_livro,
        administrador=self,
        **alteracoes
    )
