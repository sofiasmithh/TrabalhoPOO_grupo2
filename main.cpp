from gestores.catalogo import Catalogo
from gestores.estante import Estante
from modelos.administrador import Administrador
from modelos.leitor import Leitor
from modelos.livro import Livro
from persistencia.banco_de_dados import BancoDeDados


def inicializar_dados_exemplo(catalogo):
    """Adiciona alguns livros de exemplo caso o catálogo esteja vazio."""
    if not catalogo.listar_livros():
        print("A carregar livros de exemplo no catálogo...")
        # Cria um administrador temporário apenas para popular o catálogo inicial
        admin_temp = Administrador(id_usuario=1, nome="Admin Master", email="admin@admin.com", senha="123")
        
        l1 = Livro(id=1, titulo="Dom Casmurro", autor="Machado de Assis", genero="Romance", ano=1899, numero_paginas=256)
        l2 = Livro(id=2, titulo="O Hobbit", autor="J.R.R. Tolkien", genero="Fantasia", ano=1937, numero_paginas=310)
        
        catalogo.adicionar_livro(l1, admin_temp)
        catalogo.adicionar_livro(l2, admin_temp)


def menu_administrador(admin, catalogo):
    """Controla o fluxo do menu específico para Administradores."""
    while True:
        admin.menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            try:
                print("\n--- Cadastrar Novo Livro ---")
                id_livro = int(input("ID do Livro (número): "))
                titulo = input("Título: ")
                autor = input("Autor: ")
                genero = input("Gênero: ")
                ano = int(input("Ano de Publicação: "))
                paginas = int(input("Número de Páginas: "))
                
                novo_livro = Livro(id=id_livro, titulo=titulo, autor=autor, genero=genero, ano=ano, numero_paginas=paginas)
                catalogo.adicionar_livro(novo_livro, admin)
                print("Livro cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao cadastrar: {e}")
                
        elif opcao == "2":
            try:
                print("\n--- Remover Livro ---")
                id_livro = int(input("ID do Livro a remover: "))
                catalogo.remover_livro(id_livro, admin)
                print("Livro removido com sucesso!")
            except Exception as e:
                print(f"Erro ao remover: {e}")
                
        elif opcao == "3":
            try:
                print("\n--- Editar Livro ---")
                id_livro = int(input("ID do Livro a editar: "))
                titulo = input("Novo Título (deixe em branco para não alterar): ").strip()
                autor = input("Novo Autor (deixe em branco para não alterar): ").strip()
                genero = input("Novo Gênero (deixe em branco para não alterar): ").strip()
                ano_str = input("Novo Ano (deixe em branco para não alterar): ").strip()
                
                ano = int(ano_str) if ano_str else None
                titulo = titulo if titulo else None
                autor = autor if autor else None
                genero = genero if genero else None
                
                catalogo.editar_livro(id_livro, admin, titulo=titulo, autor=autor, genero=genero, ano=ano)
                print("Livro atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao editar: {e}")
                
        elif opcao == "4":
            print("\n--- Acervo Completo ---")
            livros = catalogo.listar_livros()
            if not livros:
                print("O catálogo está vazio.")
            else:
                for livro in livros:
                    print(livro)
                    
        elif opcao == "5":
            print("A terminar sessão de administrador...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def menu_leitor(leitor, catalogo):
    """Controla o fluxo do menu específico para Leitores e a sua Estante."""
    estante = Estante(leitor_id=leitor.id, catalogo=catalogo)
    
    while True:
        leitor.menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n--- Catálogo Disponível ---")
            for livro in catalogo.listar_livros():
                print(livro)
                
            try:
                livro_id = int(input("\nDigite o ID do livro que deseja adicionar à estante: "))
                print("Status disponíveis: Quero ler, Lendo, Lido, Abandonado")
                status = input("Digite o status desejado: ").strip()
                estante.adicionar_leitura(livro_id, status)
                print("Livro adicionado à estante com sucesso!")
            except Exception as e:
                print(f"Erro: {e}")
                
        elif opcao == "2":
            print("\n--- Minha Estante ---")
            leituras = estante.listar_todas()
            if not leituras:
                print("A sua estante está vazia.")
            else:
                for leitura in leituras:
                    livro_obj = catalogo.buscar_por_id(leitura.livro_id)
                    titulo = livro_obj.titulo if livro_obj else "Livro desconhecido"
                    print(f"- [{leitura.livro_id}] {titulo} | Status: {leitura.status} | Nota: {leitura.avaliacao}/5")
                    
        elif opcao == "3":
            try:
                print("\n--- Definir Meta Anual de Leitura ---")
                meta = int(input("Quantos livros pretende ler este ano? "))
                estante.definir_meta_anual(meta)
                print("Meta definida com sucesso!")
            except Exception as e:
                print(f"Erro: {e}")
                
        elif opcao == "4":
            progresso = estante.calcular_progresso_meta()
            print(f"\nProgresso da meta anual: {progresso:.1f}% concluído.")
            
        elif opcao == "5":
            print("A terminar sessão de leitor...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def main():
    catalogo = Catalogo()
    inicializar_dados_exemplo(catalogo)
    
    print("\n========================================")
    print("      BEM-VINDO AO ASSISTENTE LITERÁRIO ")
    print("========================================")
    
    # Simulação de autenticação rápida para testes no terminal
    tipo_conta = input("Deseja entrar como (1) Administrador ou (2) Leitor? ").strip()
    
    if tipo_conta == "1":
        # Instancia um Administrador de teste
        admin = Administrador(id_usuario=99, nome="Gestor Principal", email="admin@sistema.com", senha="123")
        menu_administrador(admin, catalogo)
    elif tipo_conta == "2":
        # Instancia um Leitor de teste
        leitor = Leitor(id_usuario=1, nome="Lígia Leitora", email="ligia@email.com", senha="123")
        menu_leitor(leitor, catalogo)
    else:
        print("Opção inválida. Reinicie o programa.")


if __name__ == "__main__":
    main()
