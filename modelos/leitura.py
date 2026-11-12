
class Leitura:
    STATUS_VALIDOS = [
        "Lendo",
        "Lido",
        "Quero ler",
        "Abandonado"
    ]

    def __init__(
        self,
        livro,
        status="Quero ler",
        favorito=False,
        avaliacao=0,
        resenha="",
        data_conclusao=None
    ):
        self.livro = livro
        self.status = status
        self.favorito = favorito
        self.avaliacao = avaliacao
        self.resenha = resenha
        self.data_conclusao = data_conclusao

    @property
    def livro_id(self):
        return self.livro.id if hasattr(self.livro, "id") else self.livro

    def __str__(self):
        fav_texto = " [Favorito]" if self.favorito else ""

        titulo_livro = (
            self.livro.titulo
            if hasattr(self.livro, "titulo")
            else f"Livro ID {self.livro}"
        )

        return (
            f"'{titulo_livro}' | "
            f"Status: {self.status} | "
            f"Nota: {self.avaliacao}/5{fav_texto}"
        )

    def para_dict(self):
        return {
            "livro_id": self.livro_id,
            "status": self.status,
            "favorito": self.favorito,
            "avaliacao": self.avaliacao,
            "resenha": self.resenha,
            "data_conclusao": self.data_conclusao
        }

    def to_dict(self, leitor_id):
        dados = self.para_dict()
        dados["tipo"] = "leitura"
        dados["leitor_id"] = leitor_id
        return dados

    @classmethod
    def from_dict(cls, dados, livro):
        return cls(
            livro=livro,
            status=dados.get("status", "Quero ler"),
            favorito=dados.get("favorito", False),
            avaliacao=dados.get("avaliacao", 0),
            resenha=dados.get("resenha", ""),
            data_conclusao=dados.get("data_conclusao")
        )
