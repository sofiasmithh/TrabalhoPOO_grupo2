
from datetime import date
from modelos.leitura import Leitura
from persistencia.banco_de_dados import BancoDeDados


class Estante:
    STATUS_VALIDOS = Leitura.STATUS_VALIDOS

    def __init__(self, leitor_id, catalogo, banco=None):
        self.__leitor_id = leitor_id
        self.__catalogo = catalogo

        if banco is None:
            self.__banco = BancoDeDados()
        else:
            self.__banco = banco

        self.__leituras = []
        self.__meta_anual = 0
        self.carregar_estante()

    def carregar_estante(self):
        self.__leituras = []
        self.__meta_anual = 0

        dados = self.__banco.carregar_leituras()

        for registro in dados:
            if registro.get("leitor_id") != self.__leitor_id:
                continue

            if registro.get("tipo") == "meta":
                self.__meta_anual = int(
                    registro.get("meta_anual", 0)
                )

            elif registro.get("tipo") == "leitura" or "livro_id" in registro:
                livro = self.__catalogo.buscar_por_id(
                    int(registro["livro_id"])
                )

                if livro is not None:
                    leitura = Leitura.from_dict(registro, livro)
                    self.__leituras.append(leitura)

    def salvar_estante(self):
        dados = self.__banco.carregar_leituras()

        # Mantém os registros dos outros leitores.
        dados = [
            registro for registro in dados
            if registro.get("leitor_id") != self.__leitor_id
        ]

        for leitura in self.__leituras:
            dados.append(leitura.to_dict(self.__leitor_id))

        dados.append({
            "tipo": "meta",
            "leitor_id": self.__leitor_id,
            "meta_anual": self.__meta_anual
        })

        self.__banco.salvar_leituras(dados)

    
    def adicionar_leitura(self, livro_id, status="Quero ler"):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status inválido.")

        livro = self.__catalogo.buscar_por_id(livro_id)

        if livro is None:
            raise ValueError("Livro não encontrado no catálogo.")

        for leitura in self.__leituras:
            if leitura.livro_id == livro_id:
                raise ValueError("Livro já está na estante.")

        data_conclusao = date.today().isoformat() if status == "Lido" else None

        leitura = Leitura(
            livro,
            status,
            data_conclusao=data_conclusao
        )

        self.__leituras.append(leitura)
        self.salvar_estante()

    def remover_leitura(self, livro_id):
        leitura = self.buscar_leitura(livro_id)
        self.__leituras.remove(leitura)
        self.salvar_estante()

    def buscar_leitura(self, livro_id):
        for leitura in self.__leituras:
            if leitura.livro_id == livro_id:
                return leitura

        raise ValueError("Livro não encontrado na estante.")

    def listar_todas(self):
        return self.__leituras.copy()

    def filtrar_por_status(self, status):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status inválido.")

        return [
            leitura for leitura in self.__leituras
            if leitura.status == status
        ]

    def listar_favoritos(self):
        return [
            leitura for leitura in self.__leituras
            if leitura.favorito
        ]

    def atualizar_status(self, livro_id, novo_status):
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError("Status inválido.")

        leitura = self.buscar_leitura(livro_id)
        leitura.status = novo_status

        if novo_status == "Lido":
            leitura.data_conclusao = date.today().isoformat()
        else:
            leitura.data_conclusao = None

        self.salvar_estante()

    def avaliar_livro(self, livro_id, avaliacao):
        if (
            not isinstance(avaliacao, int)
            or isinstance(avaliacao, bool)
            or not 1 <= avaliacao <= 5
        ):
            raise ValueError(
                "A avaliação deve ser um número inteiro de 1 a 5."
            )

        leitura = self.buscar_leitura(livro_id)
        leitura.avaliacao = avaliacao
        self.salvar_estante()

    def alternar_favorito(self, livro_id):
        leitura = self.buscar_leitura(livro_id)
        leitura.favorito = not leitura.favorito
        self.salvar_estante()

        return leitura.favorito

    def definir_meta_anual(self, meta):
        if (
            not isinstance(meta, int)
            or isinstance(meta, bool)
            or meta <= 0
        ):
            raise ValueError(
                "A meta deve ser um número inteiro positivo."
            )

        self.__meta_anual = meta
        self.salvar_estante()

    def calcular_progresso_meta(self):
        if self.__meta_anual == 0:
            return 0

        ano_atual = date.today().year

        concluidos = sum(
            1 for leitura in self.__leituras
            if leitura.status == "Lido"
            and leitura.data_conclusao
            and date.fromisoformat(
                leitura.data_conclusao
            ).year == ano_atual
        )

        return concluidos / self.__meta_anual * 100

    
    def adicionar_resenha(self, livro_id, resenha):
        leitura = self.buscar_leitura(livro_id)

        if not isinstance(resenha, str) or not resenha.strip():
            raise ValueError("A resenha não pode ficar vazia.")

        leitura.resenha = resenha.strip()
        self.salvar_estante()

    def consultar_resenha(self, livro_id):
        leitura = self.buscar_leitura(livro_id)
        return leitura.resenha

