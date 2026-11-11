from gestores.catalogo import Catalogo
from gestores.estante import Estante
from modelos.administrador import Administrador
from modelos.leitor import Leitor
from modelos.usuario import Usuario
from modelos.livro import Livro
from persistencia.banco_de_dados import BancoDeDados


def criar_administrador_inicial(banco):
    usuarios = banco.carregar_usuarios()
    email_admin = "admin@sistema.com"

    for dados in usuarios:
        if dados["email"].strip().casefold() == email_admin.casefold():
            return

    ids = [
        usuario["id"]
        for usuario in usuarios
        if isinstance(usuario.get("id"), int)
    ]

    id_admin = max(ids, default=0) + 1

    admin = Administrador(
        id_usuario=id_admin,
        nome="Administrador",
        email=email_admin,
        senha="Admin@2026"
    )

    usuarios.append(admin.para_dict())
    banco.salvar_usuarios(usuarios)

    print("Conta inicial de administrador criada.")


def inicializar_dados_exemplo(catalogo):
    if not catalogo.listar_livros():
        admin_temp = Administrador(
            id_usuario=0,
            nome="Administrador temporário",
            email="temporario@sistema.com",
            senha="123"
        )

        livro1 = Livro(
            id=1,
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            genero="Romance",
            ano=1899,
            numero_paginas=256
        )

        livro2 = Livro(
            id=2,
            titulo="O Hobbit",
            autor="J.R.R. Tolkien",
            genero="Fantasia",
            ano=1937,
            numero_paginas=310
        )

        catalogo.adicionar_livro(livro1, admin_temp)
        catalogo.adicionar_livro(livro2, admin_temp)


def cadastrar_leitor(banco):
    print("\n===== CADASTRO DE LEITOR =====")

    try:
        usuarios = banco.carregar_usuarios()

        ids = [
            usuario["id"]
            for usuario in usuarios
            if isinstance(usuario.get("id"), int)
        ]

        id_usuario = max(ids, default=0) + 1

        nome = input("Nome: ").strip()
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()

        Leitor.cadastrar(
            banco,
            id_usuario,
            nome,
            email,
            senha
        )

        print("Cadastro realizado com sucesso!")

    except (ValueError, TypeError) as erro:
        print(f"Não foi possível realizar o cadastro: {erro}")


def fazer_login(banco, catalogo):
    print("\n===== LOGIN =====")

    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    usuario = Usuario.autenticar(banco, email, senha)

    if usuario is None:
        print("E-mail ou senha incorretos.")
        return

    print(f"\nBem-vindo(a), {usuario.nome}!")

    if isinstance(usuario, Administrador):
        menu_administrador(usuario, catalogo)
    elif isinstance(usuario, Leitor):
        menu_leitor(usuario, catalogo)


def menu_administrador(admin, catalogo):
    while True:
        admin.menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            try:
                print("\n--- Cadastrar Livro ---")

                id_livro = int(input("ID do livro: "))
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                genero = input("Gênero: ").strip()
                ano = int(input("Ano de publicação: "))
                paginas = int(input("Número de páginas: "))

                livro = Livro(
                    id=id_livro,
                    titulo=titulo,
                    autor=autor,
                    genero=genero,
                    ano=ano,
                    numero_paginas=paginas
                )

                catalogo.adicionar_livro(livro, admin)
                print("Livro cadastrado com sucesso!")

            except (ValueError, TypeError) as erro:
                print(f"Erro ao cadastrar livro: {erro}")

        elif opcao == "2":
            try:
                id_livro = int(input("ID do livro que deseja remover: "))
                catalogo.remover_livro(id_livro, admin)
                print("Livro removido com sucesso!")

            except (ValueError, TypeError) as erro:
                print(f"Erro ao remover livro: {erro}")

        elif opcao == "3":
            try:
                id_livro = int(input("ID do livro que deseja editar: "))

                titulo = input("Novo título: ").strip()
                autor = input("Novo autor: ").strip()
                genero = input("Novo gênero: ").strip()
                ano_texto = input("Novo ano: ").strip()

                alteracoes = {}

                if titulo:
                    alteracoes["titulo"] = titulo

                if autor:
                    alteracoes["autor"] = autor

                if genero:
                    alteracoes["genero"] = genero

                if ano_texto:
                    alteracoes["ano"] = int(ano_texto)

                catalogo.editar_livro(
                    id_livro,
                    admin,
                    **alteracoes
                )

                print("Livro atualizado com sucesso!")

            except (ValueError, TypeError) as erro:
                print(f"Erro ao editar livro: {erro}")

        elif opcao == "4":
            print("\n===== CATÁLOGO =====")

            livros = catalogo.listar_livros()

            if not livros:
                print("O catálogo está vazio.")
            else:
                for livro in livros:
                    print(livro)

        elif opcao == "5":
            print("Saindo da conta de administrador...")
            break

        else:
            print("Opção inválida.")

def menu_leitor(leitor, catalogo):
    estante = Estante(
        leitor_id=leitor.id,
        catalogo=catalogo
    )

    while True:
        leitor.menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\n===== CATÁLOGO =====")
            livros = catalogo.listar_livros()

            if not livros:
                print("O catálogo está vazio.")
            else:
                for livro in livros:
                    print(livro)

        elif opcao == "2":
            print("\n===== MINHA ESTANTE =====")
            leituras = estante.listar_todas()

            if not leituras:
                print("Sua estante está vazia.")
            else:
                for leitura in leituras:
                    livro = catalogo.buscar_por_id(leitura.livro_id)
                    titulo = livro.titulo if livro else "Livro desconhecido"

                    print(
                        f"ID: {leitura.livro_id} | "
                        f"Título: {titulo} | "
                        f"Status: {leitura.status} | "
                        f"Nota: {leitura.avaliacao}/5"
                    )

        elif opcao == "3":
            try:
                livro_id = int(input("ID do livro que deseja adicionar: "))
                status = input(
                    "Status (Quero ler, Lendo, Lido ou Abandonado): "
                ).strip()

                estante.adicionar_leitura(livro_id, status)
                print("Livro adicionado à estante!")

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

        elif opcao == "4":
            try:
                livro_id = int(input("ID do livro que deseja remover: "))
                estante.remover_leitura(livro_id)
                print("Livro removido da estante!")

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

        elif opcao == "5":
            try:
                livro_id = int(input("ID do livro: "))
                status = input(
                    "Novo status (Quero ler, Lendo, Lido ou Abandonado): "
                ).strip()

                estante.atualizar_status(livro_id, status)
                print("Status atualizado!")

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

        elif opcao == "6":
            print("\n1 - Avaliar livro")
            print("2 - Favoritar ou desfavoritar livro")

            escolha = input("Escolha uma opção: ").strip()

            try:
                livro_id = int(input("ID do livro: "))

                if escolha == "1":
                    nota = int(input("Nota de 1 a 5: "))
                    estante.avaliar_livro(livro_id, nota)
                    print("Avaliação registrada!")

                elif escolha == "2":
                    estante.alternar_favorito(livro_id)
                    print("Favorito atualizado!")

                else:
                    print("Opção inválida.")

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

        elif opcao == "7":
            try:
                meta = int(
                    input("Quantos livros deseja ler este ano? ")
                )
                estante.definir_meta_anual(meta)
                print("Meta anual definida!")

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

        elif opcao == "8":
            try:
                progresso = estante.calcular_progresso_meta()
                print(f"Progresso da meta anual: {progresso:.1f}%")

            except (ValueError, TypeError) as erro:
                print(f"Erro: {erro}")

        elif opcao == "9":
            print("Saindo da conta de leitor...")
            break

        else:
            print("Opção inválida. Tente novamente.")



def main():
    banco = BancoDeDados()

    criar_administrador_inicial(banco)

    catalogo = Catalogo()
    inicializar_dados_exemplo(catalogo)

    while True:
        print("\n========================================")
        print("       ASSISTENTE LITERÁRIO")
        print("========================================")
        print("1 - Fazer login")
        print("2 - Cadastrar leitor")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            fazer_login(banco, catalogo)

        elif opcao == "2":
            cadastrar_leitor(banco)

        elif opcao == "3":
            print("Encerrando o Assistente Literário...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()