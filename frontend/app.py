
import streamlit as st

from config import APP_NAME, CSS_PATH, LOGO_PATH,LOGO_PATH2
from session_state import init_session_state
from components.sidebar import render_sidebar
from components.hero import render_hero
from components.repository_card import render_repository_card
from components.chat_interface import render_chat_interface
from components.stats_dashboard import render_stats_dashboard
from components.footer import render_footer



def load_css(path: str) -> None:
    try:
        with open(path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  


def main():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=LOGO_PATH2,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    load_css(CSS_PATH)
    init_session_state()

    render_sidebar()
    render_hero()

    render_repository_card()

    if st.session_state.repo_indexed:
        render_stats_dashboard()

    st.markdown("<br>", unsafe_allow_html=True)
    render_chat_interface()

    render_footer()


if __name__ == "__main__":
    main()