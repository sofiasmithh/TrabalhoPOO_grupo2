class Leitura:
    def __init__(self, livro, status="Quero ler", favorito=False, avaliacao=0, resenha=""):
        self.livro = livro              
        self.status = status           
        self.favorito = favorito        
        self.avaliacao = avaliacao      
        self.resenha = resenha         

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
