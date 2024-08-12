import streamlit as st
import requests

# Configurar las API keys usando Streamlit secrets
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

# Función para realizar búsquedas con Serper
def search_serper(query):
    url = "https://google.serper.dev/search"
    payload = {
        "q": query + " ley Guatemala",
        "num": 5
    }
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Función para generar respuestas con Together AI
def generate_response(prompt, search_results):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    context = "Información relevante de la búsqueda:\n"
    for result in search_results.get("organic", [])[:3]:
        context += f"- {result['title']}: {result['snippet']}\n"
    
    messages = [
        {"role": "system", "content": "Eres un asistente legal experto en las leyes de Guatemala. Utiliza la información proporcionada para responder preguntas, pero también usa tu conocimiento general sobre leyes. Si no estás seguro, indícalo claramente."},
        {"role": "user", "content": f"{context}\n\nPregunta: {prompt}\n\nPor favor, responde a la pregunta basándote en la información proporcionada y tu conocimiento sobre las leyes de Guatemala."}
    ]
    
    payload = {
        "model": "togethercomputer/llama-2-70b-chat",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# Configuración de la página de Streamlit
st.set_page_config(page_title="Asistente Legal de Guatemala", page_icon="🇬🇹")
st.title("Asistente Legal de Guatemala 🇬🇹⚖️")

# Interfaz de usuario
user_question = st.text_input("Haz una pregunta sobre las leyes de Guatemala:")

if user_question:
    with st.spinner("Buscando información y generando respuesta..."):
        # Realizar búsqueda
        search_results = search_serper(user_question)
        
        # Generar respuesta
        response = generate_response(user_question, search_results)
        
        # Mostrar respuesta
        st.write("Respuesta:")
        st.write(response)
        
        # Mostrar fuentes
        st.write("Fuentes de información:")
        for result in search_results.get("organic", [])[:3]:
            st.write(f"- [{result['title']}]({result['link']})")

# Nota de descargo de responsabilidad
st.markdown("---")
st.write("**Nota:** Este asistente proporciona información general y no debe considerarse como asesoramiento legal profesional. Consulte a un abogado para obtener asesoramiento legal específico.")
