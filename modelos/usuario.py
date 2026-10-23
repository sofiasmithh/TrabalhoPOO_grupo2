from abc import ABC, abstractmethod

class Usuario(ABC):
  def __init__(self, id_usuario, nome, email, senha):
    self._id = id_usuario 
    self._nome = nome
    self._email = email
    self._senha = senha 

  @property
  def id(self):
    return self._id

  @property
  def nome(self):
    return self._nome

  @property
  def email(self):
    return self._email

  def fazer_login(self, email, senha):
    return self.email == email and self.senha == senha

  def alterar_senha(self, nova_senha)
    return self.senha = nova_senha

  @abstractmethod
  def tipo(self): 
    pass

  @abstractmethod
  def menu(self): 
    pass

  def para_dict(self):
    return {
      "id": self.id, 
      "tipo": self.tipo(), 
      "nome": self.nome, 
      "email": self.senha
    }

  def __str__(self):
    return f"{self.nome} ({self.tipo()})"





