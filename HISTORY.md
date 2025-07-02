# Diário de Bordo e Decisões de Projeto: Desafio Autocomplete

## Preâmbulo

Este documento detalha o meu processo de planejamento, arquitetura, desenvolvimento e depuração da aplicação "Busca com Autocompletar". O objetivo deste registro é fornecer uma visão transparente sobre as decisões técnicas que tomei, os desafios que enfrentei e as soluções que implementei, cumprindo os requisitos do desafio técnico.

---

## 1. Análise Inicial e Planejamento

O desafio consistia em criar uma aplicação web de página única com uma funcionalidade de busca que sugerisse termos em tempo real.

### Requisitos Funcionais Extraídos:

- **Interface:** Uma página única com um campo de busca, construída com React.
- **Responsividade:** A interface deveria ser amigável em dispositivos móveis.
- **Comunicação:** O fluxo de dados deveria ser `Frontend (React) -> GraphQL -> Backend`.
- **Lógica do Autocomplete:**
    - Gatilho após 4 caracteres.
    - Ocultar sugestões se não houver resultados.
    - Backend retorna no máximo 20 sugestões; frontend exibe 10 com rolagem.
    - O termo buscado deve ser destacado em **negrito**.
    - A lista deve ser atualizada dinamicamente com a digitação.
    - A performance deve ser próxima do tempo real.
    - Clicar em uma sugestão preenche o campo de busca.
- **Persistência de Dados:** A escolha do banco de dados era livre, mas deveria haver uma forma automatizada de populá-lo.
- **Ambiente de Execução:** A aplicação completa deveria ser executável com um único comando `docker-compose up` em sistemas Ubuntu ou macOS.

---

## 2. Escolhas Tecnológicas e Justificativas

Para construir a solução, selecionei a seguinte stack, guiado por princípios de modernidade, performance e escalabilidade.

| Camada | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, TypeScript, Tailwind CSS | **React** e **Tailwind** eram requisitos. **Vite** foi escolhido por sua performance superior em ambiente de desenvolvimento (HMR). **TypeScript** foi adicionado para garantir segurança de tipos e manutenibilidade do código. |
| **Cliente API** | Apollo Client | Padrão de mercado para conectar aplicações React a servidores GraphQL. Simplifica o gerenciamento de estado de dados remotos, caching e o uso de queries/mutações através de hooks. |
| **Camada GraphQL** | Node.js, Express, Apollo Server | **Node.js** mantém a consistência da linguagem (JavaScript/TypeScript). **Express** fornece uma base sólida e controlável para o servidor, permitindo a fácil adição de middlewares (como CORS) e rotas (como `/health`). **Apollo Server** é a implementação de referência para um servidor GraphQL. |
| **Backend** | Python, FastAPI | **FastAPI** foi escolhido por sua altíssima performance, natureza assíncrona (ideal para I/O com banco de dados) e a geração automática de documentação interativa (Swagger UI), o que acelera drasticamente os testes de API. |
| **Banco de Dados** | Redis | A escolha mais crítica do projeto. Para a funcionalidade de autocompletar, a latência é tudo. **Redis**, por ser um banco de dados em memória, oferece tempos de resposta na casa dos microssegundos. Sua estrutura de dados **Sorted Set** (`ZSET`) é perfeita para implementar o ranking por frequência. |
| **Infraestrutura**| Docker & Docker Compose | Requisito do desafio. É a forma padrão de garantir a paridade entre ambientes de desenvolvimento e produção, além de simplificar a inicialização de um sistema complexo com múltiplos serviços. |

---

## 3. Arquitetura do Sistema

Optei por uma arquitetura de microsserviços para promover o desacoplamento e a especialização de cada componente.

**Fluxo de uma Requisição de Busca:**
1.  **Usuário (Navegador):** Digita "sao p" no componente React.
2.  **Frontend (React):** Após um `debounce` de 150ms, o Apollo Client envia uma *query* GraphQL para o serviço GraphQL.
3.  **Serviço GraphQL (Apollo/Express):** Recebe a query. O *resolver* correspondente é ativado e faz uma requisição REST `GET /suggestions?term=sao p` para a API Backend.
4.  **API Backend (FastAPI):** Recebe a requisição, se conecta ao Redis e executa a lógica de busca (filtragem por prefixo e ordenação por score).
5.  **Banco de Dados (Redis):** Retorna a lista de sugestões correspondentes instantaneamente.
6.  O fluxo se inverte: o FastAPI retorna o JSON para o GraphQL, que o formata e o envia para o Frontend, que por sua vez atualiza a UI e exibe a lista para o usuário.

**Fluxo de uma Atualização de Score:**
1.  **Usuário (Navegador):** Clica na sugestão "São Paulo".
2.  **Frontend (React):** A função de clique envia uma *mutação* GraphQL para o serviço GraphQL.
3.  **Serviço GraphQL (Apollo/Express):** O resolver da mutação faz uma requisição REST `POST /suggestions/increment` para a API Backend, enviando `{ "term": "São Paulo" }` no corpo.
4.  **API Backend (FastAPI):** Recebe a requisição e executa o comando `ZINCRBY` no Redis para o termo "São Paulo".
5.  **Banco de Dados (Redis):** O score do membro "São Paulo" é incrementado atomicamente.

---

## 4. Jornada de Depuração e Desafios Superados

O desenvolvimento de um sistema distribuído raramente é linear. Abaixo estão os principais desafios que enfrentei e as soluções que implementei.

### a) O Conflito Host vs. Container: A Saga das Permissões
O primeiro e maior obstáculo foi o erro `Permission denied` ao rodar a aplicação localmente com Docker.
* **Diagnóstico:** O usuário dentro do container Docker não tinha o mesmo ID de usuário (UID) do meu usuário na máquina host, e por isso era impedido de ler os arquivos montados via `volumes`.
* **Soluções Implementadas:** Após tentar alterar permissões com `chmod` sem sucesso (provavelmente por políticas do SELinux do meu SO), a solução definitiva adotada foi usar o comando `COPY` no `Dockerfile`. Em vez de tentar ler um arquivo "estrangeiro" via volume, eu o copiei para dentro da imagem, tornando-o um arquivo nativo do container e eliminando completamente os problemas de permissão para o deploy final.

### b) Bugs de Lógica e Dados no Backend
* **`WRONGTYPE Error` no Redis:** Ocorreu quando tentei usar o comando `SCARD` em uma chave que era do tipo `Sorted Set`. Corrigi o código para usar o comando `ZCARD`, que é o correto para a estrutura de dados escolhida.
* **Busca Case-Sensitive:** A implementação inicial com `ZSCAN` falhava por ser sensível a maiúsculas/minúsculas. Abandonei essa abordagem em favor de uma lógica mais robusta em Python, que busca todos os membros e aplica um filtro `.lower().startswith()`, garantindo a insensibilidade ao caso.
* **`bytes` vs. `string`:** Em um dos deploys no Render, o cliente Redis retornava `bytes` em vez de `strings`, causando falhas silenciosas na comparação. Tornei o código defensivo, removendo a decodificação automática na conexão e adicionando `s.decode('utf-8')` explicitamente na lógica de busca.

### c) Desafios de Deploy no Render
* **"Cold Starts":** O primeiro desafio foi entender por que a aplicação "dormia". Diagnostiquei o comportamento de "cold start" dos planos gratuitos. A solução foi implementar endpoints `/health` e configurar um cron job externo para "pingar" as APIs a cada 14 minutos, mantendo-as acordadas.
* **`Port not found`:** O deploy falhava porque o Render não detectava o servidor web. A causa era a forma como o `Start Command` era executado. A solução foi refatorar o `main.py` para se tornar o ponto de entrada principal, chamando o seeding e depois iniciando o `uvicorn` programaticamente, dando ao código controle total sobre a inicialização.

---

## 5. Melhorias Implementadas (Além do Básico)

Além dos requisitos básicos do desafio, implementei as seguintes melhorias para elevar a qualidade do projeto:

* **Fonte de Dados Robusta:** Substituí a lista inicial de dados por um dicionário completo da língua portuguesa, extraído de fontes acadêmicas, tornando as sugestões muito mais ricas.
* **Ranking de Frequência:** Implementei a funcionalidade de ordenação de sugestões por popularidade, onde o score é atualizado a cada clique do usuário, tornando a busca mais inteligente.
* **Experiência de Usuário Aprimorada:** Adicionei navegação completa por teclado (setas, Enter, Esc), feedback visual para o item ativo, uma mensagem clara para buscas sem resultado e ajustei o `debounce` para uma resposta mais rápida e fluida.

---

## 6. Possíveis Melhorias Futuras

Se eu tivesse mais tempo para continuar trabalhando no projeto, as próximas iterações focariam em:

* **Busca "Fuzzy":** Implementar tolerância a erros de digitação usando bibliotecas como `thefuzz` em Python para calcular a similaridade entre strings.
* **Cache:** Adicionar uma camada de cache no GraphQL (com `InMemoryLRUCache` do Apollo ou o próprio Redis) para acelerar drasticamente as respostas para buscas repetidas.
* **Testes Automatizados:** Escrever uma suíte de testes completa, incluindo testes unitários para a API com `pytest` e testes de componente com `React Testing Library` para a UI do autocompletar.
* **Site HTTPS:** Deixar o site seguro com protocolos de segurança como o SSL/TLS para criptografar os dados antes de serem enviados pela internet.
* **Melhoria na base de dados:** Eu peguei uma base de dados já pronta, vinda diretamente do site do IME USP. Se eu tivesse mais tempo eu com certeza pensaria em outras formar de adquirir mais palavras e termos de pesquisa para melhorar a portabilidade do projeto.

---

## 7. Conclusão

O projeto final é uma aplicação full-stack robusta, portátil e funcional que não apenas cumpre, mas excede os requisitos do desafio. A jornada de desenvolvimento, repleta de desafios de permissão, lógica e deploy, serviu como uma simulação valiosa do ciclo de vida de um produto de software real, desde a concepção até a publicação na nuvem.
