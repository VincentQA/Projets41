import os
import streamlit as st
import openai

# Titre principal de l'application
st.title("Application Multi-Chats - 3 Chatbots avec OpenAI (API mise à jour)")

# Charger la clé API depuis st.secrets ou la variable d'environnement
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialisation des historiques de conversation pour chaque chat dans st.session_state
if "messages_chat1" not in st.session_state:
    st.session_state["messages_chat1"] = []
if "messages_chat2" not in st.session_state:
    st.session_state["messages_chat2"] = []
if "messages_chat3" not in st.session_state:
    st.session_state["messages_chat3"] = []

def chat_interface(chat_key: str, model: str):
    """
    Affiche l'interface de chat pour une instance donnée identifiée par 'chat_key',
    et utilise le modèle spécifié dans 'model'.
    """
    messages = st.session_state[chat_key]

    # Affichage de l'historique de conversation
    for idx, msg in enumerate(messages):
        # Ajout d'une key unique pour chaque message peut aussi aider
        with st.chat_message(msg["role"], key=f"{chat_key}_{msg['role']}_{idx}"):
            st.markdown(msg["content"])

    # Saisie de l'utilisateur avec une key unique
    user_input = st.chat_input("Posez votre question :", key=f"{chat_key}_input")
    if user_input:
        # Ajout et affichage du message utilisateur
        messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", key=f"{chat_key}_user_{len(messages)}"):
            st.markdown(user_input)

        # Préparation de la conversation pour l'appel à l'API OpenAI
        conversation = [{"role": m["role"], "content": m["content"]} for m in messages]

        response_text = ""
        placeholder = st.empty()
        with st.chat_message("assistant", key=f"{chat_key}_assistant_{len(messages)}"):
            # Appel à l'API OpenAI en mode streaming
            response_stream = openai.ChatCompletion.create(
                model=model,
                messages=conversation,
                stream=True
            )
            # Affichage progressif de la réponse
            for chunk in response_stream:
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

with tabs[0]:
    st.subheader("Chat 1")
    model_chat1 = st.selectbox("Choisissez le modèle pour Chat 1", options=["gpt-3.5-turbo", "gpt-4"], key="model_chat1")
    chat_interface("messages_chat1", model_chat1)

with tabs[1]:
    st.subheader("Chat 2")
    model_chat2 = st.selectbox("Choisissez le modèle pour Chat 2", options=["gpt-3.5-turbo", "gpt-4"], key="model_chat2")
    chat_interface("messages_chat2", model_chat2)

with tabs[2]:
    st.subheader("Chat 3")
    model_chat3 = st.selectbox("Choisissez le modèle pour Chat 3", options=["gpt-3.5-turbo", "gpt-4"], key="model_chat3")
    chat_interface("messages_chat3", model_chat3)
