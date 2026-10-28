from modelos_usuario import Usuario 

class Leitor(Usuario): 
  def tipo(self):
    return "leitor"

  def menu(self):
    print("\n===== MENU DO LEITOR =====")
    print("1 - Consultar catálogo")
    print("2 - Consultar minha estante")
    print("3 - Adicionar livro à estante")
    print("4 - Remover livro da estante")
    print("5 - Atualizar status de leitura")
    print("6 - Avaliar ou favoritar livro")
    print("7 - Definir meta anual")
    print("8 - Consultar progresso da meta")
    print("9 - Sair")
