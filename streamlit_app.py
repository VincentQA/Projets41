import os
import uuid
import streamlit as st
from openai import OpenAI

# Titre principal de l'application
st.title("Application Multi-Chats - 3 Chatbots avec OpenAI (Nouvelle API)")

# Créer le client OpenAI
client = OpenAI()

# Initialiser les historiques de conversation pour chaque chat dans st.session_state
for chat in ["messages_chat1", "messages_chat2", "messages_chat3"]:
    if chat not in st.session_state:
        st.session_state[chat] = []

def add_message(chat_key: str, role: str, content: str):
    """
    Ajoute un message à l'historique identifié par chat_key avec un identifiant unique.
    """
    msg = {
        "role": role,
        "content": content,
        "uid": str(uuid.uuid4())
    }
    st.session_state[chat_key].append(msg)

def chat_interface(chat_key: str, model: str):
    """
    Affiche l'interface de chat pour une instance identifiée par chat_key,
    en utilisant le modèle OpenAI précisé.
    """
    messages = st.session_state[chat_key]

    # Affichage de l'historique des messages
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Zone de saisie utilisateur avec une key unique par chat
    user_input = st.chat_input("Posez votre question :", key=f"{chat_key}_input")
    if user_input:
        # Ajouter et afficher le message utilisateur
        add_message(chat_key, "user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        # Préparer la conversation pour l'appel à l'API OpenAI
        conversation = [{"role": m["role"], "content": m["content"]} for m in st.session_state[chat_key]]
        
        # Appel à l'API OpenAI en utilisant la nouvelle syntaxe
        completion = client.chat.completions.create(
            model=model,
            messages=conversation
        )
        # Récupérer la réponse complète
        response_text = completion.choices[0].message.content

        # Afficher la réponse de l'assistant
        with st.chat_message("assistant"):
            st.markdown(response_text)
        add_message(chat_key, "assistant", response_text)

# Création de trois onglets pour des chats indépendants
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
