import os
import uuid
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
for chat in ["messages_chat1", "messages_chat2", "messages_chat3"]:
    if chat not in st.session_state:
        st.session_state[chat] = []

def add_message(chat_key: str, role: str, content: str):
    """
    Ajoute un message à l'historique avec un identifiant unique.
    """
    msg = {
        "role": role,
        "content": content,
        "uid": str(uuid.uuid4())
    }
    st.session_state[chat_key].append(msg)

def chat_interface(chat_key: str, model: str):
    """
    Affiche l'interface de chat pour une instance identifiée par 'chat_key'
    et utilisant le modèle spécifié dans 'model'.
    """
    messages = st.session_state[chat_key]

    # Affichage de l'historique des messages avec une key unique pour chaque message.
    for msg in messages:
        # La key est composée du chat_key et de l'identifiant unique du message.
        with st.chat_message(msg["role"], key=f"{chat_key}_{msg['uid']}"):
            st.markdown(msg["content"])

    # Saisie de l'utilisateur avec une key unique pour cet input
    user_input = st.chat_input("Posez votre question :", key=f"{chat_key}_input")
    if user_input:
        # Ajout et affichage du message utilisateur
        add_message(chat_key, "user", user_input)
        with st.chat_message("user", key=f"{chat_key}_user_{len(messages)+1}"):
            st.markdown(user_input)

        # Préparation de la conversation pour l'appel à l'API
        conversation = [{"role": m["role"], "content": m["content"]} for m in st.session_state[chat_key]]

        response_text = ""
        placeholder = st.empty()  # Conteneur pour l'affichage progressif
        with st.chat_message("assistant", key=f"{chat_key}_assistant_{len(messages)+1}"):
            # Appel à l'API OpenAI en mode streaming
            response_stream = openai.ChatCompletion.create(
                model=model,
                messages=conversation,
                stream=True
            )
            # Affichage progressif de la réponse au fur et à mesure des chunks
            for chunk in response_stream:
                if "choices" in chunk:
                    delta = chunk["choices"][0]["delta"]
                    if "content" in delta:
                        chunk_text = delta["content"]
                        response_text += chunk_text
                        placeholder.markdown(response_text)
        # Ajout de la réponse complète à l'historique
        add_message(chat_key, "assistant", response_text)

# Création de trois onglets, chacun correspondant à un chat indépendant
tabs = st.tabs(["Chat 1", "Chat 2", "Chat 3"])

with tabs[0]:
    st.subheader("Chat 1")
    model_chat1 = st.selectbox("Choisissez le modèle pour Chat 1",
                               options=["gpt-4.1"],
                               key="model_chat1")
    chat_interface("messages_chat1", model_chat1)

with tabs[1]:
    st.subheader("Chat 2")
    model_chat2 = st.selectbox("Choisissez le modèle pour Chat 2",
                               options=["gpt-4.1-mini"],
                               key="model_chat2")
    chat_interface("messages_chat2", model_chat2)

with tabs[2]:
    st.subheader("Chat 3")
    model_chat3 = st.selectbox("Choisissez le modèle pour Chat 3",
                               options=["gpt-4.1-nano"],
                               key="model_chat3")
    chat_interface("messages_chat3", model_chat3)
