import os
import streamlit as st
import openai

# Titre principal de l'application
st.title("Application Multi-Chats : 3 Chatbots avec OpenAI et Streamlit")

# Charger la clé API depuis st.secrets ou la variable d'environnement
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialiser l'historique de conversation pour chaque chat
if "messages_chat1" not in st.session_state:
    st.session_state["messages_chat1"] = []
if "messages_chat2" not in st.session_state:
    st.session_state["messages_chat2"] = []
if "messages_chat3" not in st.session_state:
    st.session_state["messages_chat3"] = []

def chat_interface(chat_key: str, model: str):
    """
    Affiche l'interface de chat pour une instance donnée, identifiée par 'chat_key',
    et utilise le modèle OpenAI précisé.
    """
    messages = st.session_state[chat_key]

    # Affichage de l'historique des messages
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Saisie utilisateur
    user_input = st.chat_input("Posez votre question:")
    if user_input:
        # Ajout et affichage du message utilisateur
        messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Préparation de la conversation pour l'appel API
        conversation = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        response_text = ""
        placeholder = st.empty()
        with st.chat_message("assistant"):
            stream = openai.ChatCompletion.create(
                model=model,
                messages=conversation,
                stream=True
            )
            # Affichage en mode streaming
            for chunk in stream:
                if "choices" in chunk:
                    delta = chunk["choices"][0]["delta"]
                    if "content" in delta:
                        chunk_text = delta["content"]
                        response_text += chunk_text
                        placeholder.markdown(response_text)

        # Ajout de la réponse complète à l'historique
        messages.append({"role": "assistant", "content": response_text})

# Création de trois onglets, chacun correspondant à un chat indépendant
tabs = st.tabs(["Chat 1", "Chat 2", "Chat 3"])

# Onglet Chat 1
with tabs[0]:
    st.subheader("Chat 1")
    # Sélecteur pour choisir le modèle pour Chat 1
    model_chat1 = st.selectbox("Choisissez le modèle pour Chat 1", options=["gpt-4.1"], key="model_chat1")
    chat_interface("messages_chat1", model_chat1)

# Onglet Chat 2
with tabs[1]:
    st.subheader("Chat 2")
    # Sélecteur pour choisir le modèle pour Chat 2
    model_chat2 = st.selectbox("Choisissez le modèle pour Chat 2", options=["gpt-4.1-mini"], key="model_chat2")
    chat_interface("messages_chat2", model_chat2)

# Onglet Chat 3
with tabs[2]:
    st.subheader("Chat 3")
    # Sélecteur pour choisir le modèle pour Chat 3
    model_chat3 = st.selectbox("Choisissez le modèle pour Chat 3", options=["gpt-4.1-nano"], key="model_chat3")
    chat_interface("messages_chat3", model_chat3)
