class Leitura:
    STATUS_VALIDOS = [
        "Lendo",
        "Lido",
        "Quero ler",
        "Abandonado"
    ]

    def __init__(self, livro, status="Quero ler", favorito=False, avaliacao=0, resenha=""):
        self.livro = livro              
        self.status = status           
        self.favorito = favorito        
        self.avaliacao = avaliacao      
        self.resenha = resenha   

    @property
    def livro_id(self):
        return self.livro.id if hasattr(self.livro, "id") else self.livro      

    def __str__(self):
        fav_texto = " [Favorito]" if self.favorito else ""
        titulo_livro = self.livro.titulo if hasattr(self.livro, 'titulo') else f"Livro ID {self.livro}"
        return f"'{titulo_livro}' | Status: {self.status} | Nota: {self.avaliacao}/5{fav_texto}"

    def para_dict(self):
        return {
            "livro_id": self.livro.id if hasattr(self.livro, 'id') else self.livro,
            "status": self.status,
            "favorito": self.favorito,
            "avaliacao": self.avaliacao,
            "resenha": self.resenha
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
            resenha=dados.get("resenha", "")
        )
    