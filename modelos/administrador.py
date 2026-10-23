from modelos.usuario import Usuario 

class Administrador(Usuario):
  def __init__(self, id_usuario, nome, email, senha):
    super().__init__(id_usuario, nome, email, senha)
    
  def tipo(self):
    return "administrador"

  def menu(self):
    print("1 - Adicionar livro")
    print("2 - Remover livro")
    print("3 - Editar livro")
    print("4 - Sair")

  def adicionar_livro(self, catalogo, livro):
    catalogo.adicionar(livro)

   def remover_livro(self, catalogo, livro):
    catalogo.remover(livro)

  def editar_livro(self, livro, novo_titulo, novo_autor):
    livro.titulo = novo_titulo 
    livro.autor = novo_autor
