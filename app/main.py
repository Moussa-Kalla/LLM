import streamlit as st
from chat import LLMs


def generate_conversation_name(prompt, max_len=30):


    text = prompt.replace("\n", " ").strip()
    if not text:
        return "Nouvelle conversation"

    words = text.split()
    if len(words) > 8:
        words = words[:8]  

    short_name = " ".join(words)

    if len(short_name) > max_len:
        short_name = short_name[:max_len] + "..."

    return short_name[0].upper() + short_name[1:] if short_name else "Conversation"


if "conversations" not in st.session_state:

    st.session_state["conversations"] = []

if "selected_conv_index" not in st.session_state:
    st.session_state["selected_conv_index"] = None


st.sidebar.title("Conversations")


if st.sidebar.button("Nouvelle conversation"):
    new_conv = {
        "name": f"Conversation {len(st.session_state['conversations']) + 1}",
        "messages": [
            {
                "role": "assistant",
                "content": "Bonjour, je suis un nouvel assistant !"
            }
        ],
    }
    st.session_state["conversations"].append(new_conv)
    st.session_state["selected_conv_index"] = len(st.session_state["conversations"]) - 1

conv_names = [conv["name"] for conv in st.session_state["conversations"]]
if conv_names:
    selected = st.sidebar.radio(
        "Sélectionnez une conversation",
        range(len(conv_names)),
        format_func=lambda i: conv_names[i],
        index=st.session_state["selected_conv_index"] if st.session_state["selected_conv_index"] is not None else 0
    )
    st.session_state["selected_conv_index"] = selected
else:
    st.sidebar.info("Aucune conversation disponible.")

st.title("Kalla 's Chat")

if st.session_state["selected_conv_index"] is not None and st.session_state["conversations"]:
    current_conv = st.session_state["conversations"][st.session_state["selected_conv_index"]]

    for msg in current_conv["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Posez votre question..."):

        current_conv["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if current_conv["name"].startswith("Conversation "):
            current_conv["name"] = generate_conversation_name(user_input)

        assistant_response = LLMs(current_conv["messages"])
        
        current_conv["messages"].append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
else:
    st.info("Créez ou sélectionnez une conversation dans la barre latérale pour commencer.")