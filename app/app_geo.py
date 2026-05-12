import streamlit as st
import brazilcep
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
from openai import OpenAI
import os
from dotenv import load_dotenv
import time

# 1. Configurações de Ambiente
load_dotenv()
MINHA_CHAVE = os.getenv("DEEPSEEK_API_KEY")

if MINHA_CHAVE:
    client = OpenAI(api_key=MINHA_CHAVE, base_url="https://api.deepseek.com")
else:
    st.error("Chave DEEPSEEK_API_KEY não encontrada no .env")

st.set_page_config(page_title="Agente de Busca de Precisão", layout="wide", page_icon="📍")

st.title("📍 Busca de Precisão com Filtro Inteligente")
st.markdown("Este agente foca no **nome exato** do local, eliminando vizinhos indesejados.")

# Barra Lateral
with st.sidebar:
    st.header("Parâmetros")
    cep_input = st.text_input("Seu CEP:", value="01310100")
    # Entrada livre para o usuário
    pergunta_usuario = st.text_area("O que você busca exatamente?", 
                                   placeholder="Ex: Faculdade Mackenzie")
    
    raio_km = st.slider("Raio de busca (km):", 1, 6, 3)
    
    botao_buscar = st.button("Executar Busca 🚀")

if botao_buscar:
    if not pergunta_usuario:
        st.warning("Descreva o local que deseja encontrar.")
    else:
        try:
            with st.spinner('DeepSeek refinando o termo de busca...'):
                # 2. IA limpa o termo para garantir que o nome próprio seja o foco
                prompt = f"O usuário quer encontrar: '{pergunta_usuario}'. Extraia apenas o nome principal do estabelecimento para busca em mapa. Responda apenas o nome limpo."
                
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=20
                )
                nome_alvo = response.choices[0].message.content.strip()
                st.info(f"🔍 Buscando por: **{nome_alvo}**")

            with st.spinner('Mapeando arredores...'):
                # 3. Localização da Origem (CEP)
                endereco = brazilcep.get_address_from_cep(cep_input)
                geolocator = Nominatim(user_agent="wellington_precision_geo_v1")
                
                time.sleep(1) # Respeita o limite da API
                rua_cidade = f"{endereco['street']}, {endereco['city']}, Brazil"
                origem = geolocator.geocode(rua_cidade)

                if origem:
                    lat, lon = origem.latitude, origem.longitude
                    
                    # 4. Cálculo da área de busca (Bounding Box)
                    margem = raio_km / 111.0
                    viewbox = [
                        [lat - margem, lon - margem], 
                        [lat + margem, lon + margem]
                    ]

                    # Criar Mapa
                    m = folium.Map(location=[lat, lon], zoom_start=14)
                    folium.Marker([lat, lon], popup="Você", icon=folium.Icon(color="red", icon="home")).add_to(m)

                    # 5. Busca Restrita (bounded=1)
                    # Buscamos pelo nome exato dentro da área definida
                    resultados = geolocator.geocode(
                        nome_alvo, 
                        viewbox=viewbox, 
                        bounded=1, 
                        exactly_one=False, 
                        limit=30
                    )

                    if resultados:
                        cont_sucesso = 0
                        for lug in resultados:
                            # --- FILTRO DE PRECISÃO ---
                            # Só coloca o marcador se o nome buscado estiver no nome retornado
                            # Isso evita que "Faculdade Mackenzie" traga a "PUC" só por estar perto
                            if nome_alvo.lower() in lug.address.lower():
                                folium.Marker(
                                    [lug.latitude, lug.longitude], 
                                    popup=lug.address,
                                    icon=folium.Icon(color="blue", icon="university", prefix="fa")
                                ).add_to(m)
                                cont_sucesso += 1
                        
                        if cont_sucesso > 0:
                            folium_static(m)
                            st.success(f"Encontrados {cont_sucesso} pontos correspondentes a '{nome_alvo}'.")
                        else:
                            st.warning(f"O mapa sugeriu locais próximos, mas nenhum deles continha o nome '{nome_alvo}'.")
                    else:
                        st.warning("Nenhum resultado encontrado para este nome no raio escolhido.")
                else:
                    st.error("Não foi possível converter o CEP em coordenadas.")
                    
        except Exception as e:
            st.error(f"Erro na operação: {e}")

st.caption("Engenharia de Computação | UNIVESP | OCI Instance")