from modelos_usuario import Usuario 

class Leitor(Usuario): 
  def init(self, id_usuario, nome, email, senha): 
    super().init(id_usuario, nome, email, senha)
    
    self.estante = []
    self.meta_anual = 0
    self.livros_lidos_no_ano = 0

  def tipo(self):
    return "Leitor"

  def menu(self):
    print("1 - Adicionar leitura")
    print("2 - Remover leitura")
    print("3 - Definir meta anual")
    print("4 - Consultar progresso da meta")
    print("5 - Sair")

  def adicionar_leitura(self, leitura):
    self.estante.append(leitura)

  def remover_leitura(self, leitura):
    if leitura in self.estante:
        self.estante.remove(leitura)

  def definir_meta_anual(self, meta):
    if meta > 0:
        self.meta_anual = meta

  def atualizar_livros_lidos(self):
    self.livros_lidos_no_ano += 1

  def calcular_progresso_meta(self):
    if self.meta_anual == 0:
        return 0

    return (self.livros_lidos_no_ano / self.meta_anual) * 100
  
