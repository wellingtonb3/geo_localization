
# 📍 Agente Geográfico Inteligente (IA + Precisão Geo)

Este projeto é um **Agente de Busca de Precisão** que une Inteligência Artificial Generativa com serviços de geolocalização. O sistema foi projetado para resolver o problema de "ruído" em buscas urbanas, garantindo que apenas locais que correspondam exatamente à intenção do usuário sejam exibidos no mapa.

## 📺 Demonstração

Abaixo, o Agente interpretando comandos em linguagem natural e filtrando resultados em um raio de 3km:

![Agente Localização](/img/Dashboard.png)

---

## 🚀 Funcionalidades

- **Processamento de Linguagem Natural (NLP):** Integração com a API do **DeepSeek v3** para extrair nomes de estabelecimentos de frases complexas.
- **Busca por CEP:** Conversão automática de CEP para endereços via `brazilcep`.
- **Filtro de Precisão (Anti-Ruído):** 
  - Restrição de área via *Bounding Box* (Latitude/Longitude).
  - Seletor de raio dinâmico limitado a **5km** para máxima acurácia.
  - Validação de string: O código valida se o nome buscado está presente no endereço retornado, eliminando vizinhos indesejados.
- **Interface Web:** Dashboard interativo construído com **Streamlit** e mapas **Folium**.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12
- **IA:** DeepSeek API (Model: deepseek-chat)
- **Cloud:** Oracle Cloud Infrastructure (OCI) - Instância Ubuntu
- **Bibliotecas Principais:** 
  - `streamlit`, `folium`, `geopy`, `brazilcep`, `python-dotenv`.
 
![Agente Localização](/img/Mapa.png)

## 📦 Como Instalar e Rodar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
   cd seu-repositorio
   
Crie o Ambiente Virtual e Instale as dependências:

Bash
python3 -m venv geo_env
source geo_env/bin/activate
pip install streamlit brazilcep geopy folium streamlit-folium openai python-dotenv


3. **Configure as Credenciais:**
   Crie um arquivo `.env` na raiz:
   ```text
   DEEPSEEK_API_KEY=sua_chave_aqui
Execute a aplicação:

Bash
streamlit run app_geo_ai.py --server.port 8501 --server.runOnSave false


## 📐 Engenharia e Lógica de Dados

Diferente de buscas geográficas comuns, este agente aplica um filtro de **Data Quality** na saída:
1. A IA limpa o termo (ex: "Quero ir no Mackenzie" -> "Mackenzie").
2. O sistema define uma "janela espacial" rígida baseada no raio escolhido.
3. O Python compara o resultado do mapa com o nome alvo: `if nome_alvo in resultado_endereco`.
4. Apenas correspondências exatas são plotadas, garantindo uma interface limpa e útil.

---
**Desenvolvido por:** Wellington Carlos de Lacerda  
*Engenharia de Computação - UNIVESP*  
*Foco em Cloud, IA e Data Science*
