
import streamlit as st


def init_session_state():
   
    defaults = {
        "repo_url": "",
        "repo_indexed": False,
        "repo_stats": None,  
        "chat_history": [],    
        "srs_document": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_repo_indexed(repo_url: str, stats) -> None:
    st.session_state.repo_url = repo_url
    st.session_state.repo_indexed = True
    st.session_state.repo_stats = stats
    st.session_state.chat_history = [] 
    st.session_state.srs_document = ""


def add_chat_message(
    role,
    content,
    sources=None,
    evidence=None,
):

    st.session_state.chat_history.append(
        {
            "role": role,
            "content": content,
            "sources": sources or [],
            "evidence": evidence or [],
        }
    )


def reset_repository() -> None:
    st.session_state.repo_url = ""
    st.session_state.repo_indexed = False
    st.session_state.repo_stats = None
    st.session_state.chat_history = []
    st.session_state.srs_document = ""