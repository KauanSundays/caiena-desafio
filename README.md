# ☁️ Desafio Técnico Caiena --- Previsão do Tempo + GitHub Gist

API em **Flask** responsável por obter a previsão do tempo atual e dos
próximos 5 dias (via **OpenWeatherMap**) e publicar essas informações
como **comentário em um Gist** do GitHub.

------------------------------------------------------------------------

## 🛠️ Configuração Inicial

### 1. Clonar o Repositório

``` sh
git clone https://github.com/KauanSundays/caiena-desafio.git
cd caiena-desafio
```

------------------------------------------------------------------------

### 2. Configurar Variáveis de Ambiente

Crie um arquivo **.env** na raiz do projeto (pode copiar do
`.env.example`, se existir) e preencha as chaves necessárias.

#### 🔑 OpenWeatherMap (OWM)

Adicione sua chave no campo `OPENWEATHER_API_KEY`.\
Você pode obter uma chave gratuita aqui:
https://openweathermap.org/appid

``` ini
# Configuração OpenWeatherMap
OPENWEATHER_API_KEY=SUA_CHAVE_AQUI

# URLs padrão
OPENWEATHER_URL_5_DAYS=http://api.openweathermap.org/data/2.5/forecast
GEO_API_URL=http://api.openweathermap.org/geo/1.0/direct
```

#### 🐙 GitHub Gist

Defina as credenciais para postar o comentário no Gist:

-   **GITHUB_TOKEN**: gere um *Personal Access Token (Classic)* com
    permissão **gist**.\
    Caminho: GitHub Settings → Developer Settings → Personal access
    tokens.

-   **GITHUB_GIST_ID**: ID do Gist onde os comentários serão publicados.

``` ini
# Configurações GitHub
GITHUB_TOKEN=SEU_TOKEN_GITHUB_CLASSIC
GITHUB_GIST_ID=ID_DO_SEU_GIST
```

------------------------------------------------------------------------

## 🚀 Executando com Docker

O projeto usa **Docker** e **Docker Compose** para facilitar a execução.

Para construir e subir o serviço:

``` sh
docker-compose up --build -d
```

O serviço ficará acessível em:\
**http://localhost:5000**

------------------------------------------------------------------------

## 🧪 Executando Testes

Para rodar os testes automatizados (pytest) dentro do container:

``` sh
docker compose exec caiena-app pytest
```

------------------------------------------------------------------------

## 💻 Uso da API --- Publicar Previsão

A API expõe o endpoint:

    GET /previsao?cidade=<nome-da-cidade>

### 🔗 Exemplo

Obter a previsão de São Paulo (BR):

    http://localhost:5000/previsao?cidade=Sao Paulo,BR

------------------------------------------------------------------------

## 📦 Exemplo de Resposta (200 OK)

``` json
{
    "status": "sucesso",
    "cidade_processada": "Sao Paulo,BR",
    "mensagem_enviada": "30°C e sol em Sao Paulo,BR em 17/11. Média para os próximos dias:...",
    "detalhes": "Comentário enviado com sucesso para o Gist."
}
```

------------------------------------------------------------------------

## 📄 Licença

**MIT**
