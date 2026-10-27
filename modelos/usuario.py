from abc import ABC, abstractmethod

class Usuario(ABC):
    def _init_(self, id_usuario, nome, email, senha):
        self._id = id_usuario
        self._nome = nome.strip()
        self._email = email.strip().casefold()
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
        email = email.strip().casefold()
        return self._email == email and self._senha == senha

    def alterar_senha(self, nova_senha):
        if not isinstance(nova_senha, str) or not nova_senha.strip():
            raise ValueError("A senha não pode ficar vazia.")
        
        self._senha = nova_senha

    @classmethod
    def cadastrar(cls, banco_de_dados, id_usuario, nome, email, senha):
        if cls is Usuario:
            raise TypeError("Cadastre um Leitor ou Administrador.")

        if not all(
            isinstance(campo, str) and campo.strip()
            for campo in (nome, email, senha)
        ):
            raise ValueError("Preencha todos os campos corretamente.")

        usuarios = banco_de_dados.carregar_usuarios()
        email_normalizado = email.strip().casefold()

        for dados in usuarios:
            if dados["email"].strip().casefold() == email_normalizado:
                raise ValueError("Já existe um usuário com esse e-mail.")

        usuario = cls(id_usuario, nome, email, senha)

        usuarios.append(usuario.para_dict())
        banco_de_dados.salvar_usuarios(usuarios)

        return usuario

    @classmethod
    def autenticar(cls, banco_de_dados, email, senha):
        from modelos_leitor import Leitor
        from modelos_administrador import Administrador

        tipos_usuario = {
            "leitor": Leitor,
            "administrador": Administrador
        }

        usuarios = banco_de_dados.carregar_usuarios()

        for dados in usuarios:
            tipo = dados.get("tipo", "").casefold()
            classe_usuario = tipos_usuario.get(tipo)

            if classe_usuario is None:
                continue

            usuario = classe_usuario(
                dados["id"],
                dados["nome"],
                dados["email"],
                dados["senha"]
            )

            if usuario.fazer_login(email, senha):
                return usuario

        return None

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
            "email": self.email,
            "senha": self._senha
        }

    def _str_(self):
        return f"{self.nome} ({self.tipo()})"

