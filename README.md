#  Assistente Literário Virtual

> Projeto prático desenvolvido para a disciplina de **Programação Orientada a Objetos** (Prof.ª Gabriela Nunes Lopes)[span_3](start_span)[span_3](end_span).

---

##  Sobre o Projeto

O **Assistente Literário Virtual** é uma plataforma inspirada em redes e aplicações literárias (como o Skoob)[span_4](start_span)[span_4](end_span), desenvolvida para auxiliar leitores na organização do seu hábito de leitura e no acompanhamento de metas literárias.

###  Apelo Social e Necessidade
Num cenário digital repleto de estímulos e distrações, manter a constância de leitura torna-se um desafio. O sistema oferece uma solução centralizada, acessível e intuitiva para que os utilizadores possam gerir as suas estantes virtuais, registar o progresso de leitura, avaliar obras e cultivar hábitos sustentáveis de leitura.

---

##  Estrutura e Arquitetura do Sistema (POO)

O projeto foi estruturado aplicando os conceitos fundamentais da **Programação Orientada a Objetos**[span_5](start_span)[span_5](end_span):

* **Classes & Abstração:** Modela entidades do domínio como `Livro`, `Leitura`, `Estante`, `Catalogo` e `BancoDeDados`[span_6](start_span)[span_6](end_span).
* **Herança:** A classe base `Usuario` é herdada pelas subclasses `Leitor` e `Administrador`[span_7](start_span)[span_7](end_span).
* **Polimorfismo:** Métodos de exibição e interação (como `exibir_menu()`) comportam-se de forma específica conforme o perfil do utilizador (`Leitor` vs. `Administrador`)[span_8](start_span)[span_8](end_span)[span_9](start_span)[span_9](end_span).
* **Classes Abstratas:** A classe `Usuario` utiliza o módulo `abc` do Python, impedindo a sua instanciação direta e definindo contratos para as subclasses[span_10](start_span)[span_10](end_span).

---

##  Organização dos Módulos

A estrutura de ficheiros foi modularizada segundo o **Princípio da Responsabilidade Única (SRP)**[span_11](start_span)[span_11](end_span):

```text
assistente_literario/
│
├── main.py                   # Ponto de entrada do sistema
├── modelos/                  # Entidades de domínio (Classes base)
│   ├── __init__.py
│   ├── usuario.py            # Classe abstrata Usuario
│   ├── leitor.py             # Subclasse Leitor
│   ├── administrador.py      # Subclasse Administrador
│   ├── livro.py              # Classe Livro
│   └── leitura.py            # Associação entre Leitor e Livro
│
├── gestores/                 # Lógica de organização das coleções
│   ├── __init__.py
│   ├── estante.py            # Classe Estante (estante do leitor)
│   └── catalogo.py           # Classe Catalogo (acervo global)
│
├── persistencia/             # Camada de dados
│   ├── __init__.py
│   └── banco_de_dados.py     # Classe BancoDeDados (gestão de ficheiros JSON)
│
└── dados/                    # Armazenamento persistente
    ├── usuarios.json
    └── catalogo.json
