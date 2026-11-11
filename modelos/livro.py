
class Livro:
    def __init__(self, id, titulo, autor, genero, ano, numero_paginas=0):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.ano = ano
        self.numero_paginas = numero_paginas

    def __str__(self):
        return f"[{self.id}] '{self.titulo}' - {self.autor} ({self.ano}) | Gênero: {self.genero}"

    def para_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "ano": self.ano,
            "numero_paginas": self.numero_paginas
        }

    def to_dict(self):
        return self.para_dict()

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["id"],
            dados["titulo"],
            dados["autor"],
            dados["genero"],
            dados["ano"],
            dados.get("numero_paginas", 0)
        )
