
from modelos.livro import Livro
from persistencia.banco_de_dados import BancoDeDados


class Catalogo:
    def __init__(self):
        self.__banco = BancoDeDados()
        self.__livros = []
        self.carregar_catalogo()

    def carregar_catalogo(self):
        dados = self.__banco.carregar_catalogo()
        self.__livros = [
            Livro.from_dict(dado) for dado in dados
        ]

    def salvar_catalogo(self):
        dados = [
            livro.to_dict() for livro in self.__livros
        ]
        self.__banco.salvar_catalogo(dados)

    def adicionar_livro(self, livro, administrador=None):
        if administrador is None or administrador.tipo() != "administrador":
            raise PermissionError(
                "Somente um administrador pode adicionar livros."
            )

        if not isinstance(livro, Livro):
            raise TypeError("O objeto informado não é um livro.")

        if self.buscar_por_id(livro.id) is not None:
            raise ValueError("Já existe um livro com esse ID.")

        self.__livros.append(livro)
        self.salvar_catalogo()

    def remover_livro(self, id_livro, administrador=None):
        if administrador is None or administrador.tipo() != "administrador":
            raise PermissionError(
                "Somente um administrador pode remover livros."
            )

        livro = self.buscar_por_id(id_livro)

        if livro is None:
            raise ValueError("Livro não encontrado.")

        self.__livros.remove(livro)
        self.salvar_catalogo()

    def editar_livro(
        self, id_livro, administrador=None,
        titulo=None, autor=None, genero=None, ano=None
    ):
        if administrador is None or administrador.tipo() != "administrador":
            raise PermissionError(
                "Somente um administrador pode editar livros."
            )

        livro = self.buscar_por_id(id_livro)

        if livro is None:
            raise ValueError("Livro não encontrado.")

        if titulo is not None:
            if not titulo.strip():
                raise ValueError("O título não pode ficar vazio.")
            livro.titulo = titulo.strip()

        if autor is not None:
            if not autor.strip():
                raise ValueError("O autor não pode ficar vazio.")
            livro.autor = autor.strip()

        if genero is not None:
            if not genero.strip():
                raise ValueError("O gênero não pode ficar vazio.")
            livro.genero = genero.strip()

        if ano is not None:
            livro.ano = ano

        self.salvar_catalogo()

    def buscar_por_id(self, id_livro):
        for livro in self.__livros:
            if livro.id == id_livro:
                return livro
        return None

    def buscar_por_titulo(self, titulo):
        titulo = titulo.strip().casefold()

        return [
            livro for livro in self.__livros
            if titulo in livro.titulo.casefold()
        ]

    def listar_livros(self):
        return self.__livros.copy()

