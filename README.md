# Busca com Autocompletar Full-Stack

Uma aplicação web completa que implementa uma funcionalidade de busca com sugestões em tempo real (autocompletar), construída com uma arquitetura moderna e containerizada.

**[➡️ Acesse a demonstração ao vivo aqui!](https://autocomplete-michelheckerfaria.onrender.com/)**

![Demonstração da Aplicação](https://i.imgur.com/ABp8kkB.png)

## ✨ Funcionalidades Principais

- **Sugestões em Tempo Real:** As sugestões aparecem de forma reativa enquanto o usuário digita.
- **Ranking por Popularidade:** O sistema "aprende" com o uso. As sugestões mais selecionadas sobem no ranking e aparecem primeiro.
- **Navegação por Teclado:** Suporte completo para navegar (`▲`/`▼`), selecionar (`Enter`) e fechar (`Esc`) as sugestões usando o teclado.
- **Busca Externa no Google:** O botão "BUSCAR" e a tecla `Enter` (quando nenhuma sugestão está selecionada) abrem uma nova aba com os resultados da busca do Google para o termo digitado.
- **Feedback de UI:** Mensagens claras para "Buscando..." e "Nenhum resultado encontrado".
- **Design Responsivo:** Interface adaptada para uma ótima experiência tanto em desktops quanto em dispositivos móveis.
- **100% Containerizado:** Toda a aplicação (frontend, backend, GraphQL, banco de dados) sobe com um único comando.

## 🛠️ Stack Tecnológica

A arquitetura foi dividida em microsserviços para garantir escalabilidade e separação de responsabilidades.

| Camada          | Tecnologia                         | Propósito                                                                                                            |
| :-------------- | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Frontend** | React.js, TypeScript, Vite, Tailwind CSS | Interface do usuário moderna, rápida e reativa.                                                                      |
| **Cliente API** | Apollo Client                      | Gerenciamento de estado e comunicação com o servidor GraphQL.                                                          |
| **Camada GraphQL**| Node.js, Express, Apollo Server      | Atua como um Backend-For-Frontend (BFF), definindo o contrato de dados e traduzindo as requisições para a API de backend. |
| **Backend** | Python, FastAPI                    | API de alta performance que contém a lógica de negócio, busca e ranking.                                               |
| **Banco de Dados**| Redis                              | Banco de dados em memória de altíssima velocidade, usando `Sorted Sets` para armazenar e rankear as sugestões.         |
| **Infraestrutura**| Docker & Docker Compose            | Containerização de toda a aplicação para um ambiente de desenvolvimento e deploy previsível e isolado.                 |

## 🚀 Como Rodar o Projeto Localmente

Qualquer pessoa com Docker instalado pode rodar este projeto com um único comando.

### Pré-requisitos
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/MichelH7cker/autocomplete
    cd autocomplete 
    ```

2.  **Suba os containers:**
    Este comando irá construir as imagens, instalar todas as dependências, popular o banco de dados e iniciar todos os serviços.
    ```bash
    docker-compose up --build
    ```
    *Use `docker-compose up -d --build` para rodar em segundo plano (detached mode).*

3.  **Acesse os serviços:**
    - **Aplicação Frontend:** [http://localhost:5173](http://localhost:5173)
    - **GraphQL Playground (para testes):** [http://localhost:4000/graphql](http://localhost:4000/graphql)
    - **API Backend (documentação interativa):** [http://localhost:8000/docs](http://localhost:8000/docs)

## ☁️ Deploy

A aplicação está configurada para deploy contínuo (CI/CD) em plataformas como o [Render](https://render.com). As configurações de ambiente são gerenciadas por variáveis de ambiente, permitindo que o mesmo código funcione em qualquer lugar.

- **Gatilho de Deploy:** Um `git push` para a branch `main` inicia o processo de build e deploy automático dos serviços modificados.
- **Keep-Alive:** A aplicação no ar conta com endpoints `/health` que podem ser usados por serviços de cron job para manter os containers do plano gratuito sempre "acordados".

## 📝 Documentação do Processo

Para uma análise detalhada das decisões de arquitetura, desafios encontrados (permissões, deploy, bugs de lógica) e a jornada completa de desenvolvimento, consulte o arquivo [COMMENTS.md](COMMENTS.md).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
