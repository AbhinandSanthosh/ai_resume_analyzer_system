import streamlit as st
from streamlit_option_menu import option_menu
import jwt

from pages.login import show_login
from pages.dashboard import show_dashboard
from pages.upload_resume import show_upload_resume
from pages.analysis_history import show_analysis_history
from pages.skill_search import show_skill_search
from pages.candidate_rankings import show_candidate_rankings


SECRET_KEY = "your_secret_key"


st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.markdown(
    """
    <style>

    #MainMenu {
        visibility:hidden;
    }

    footer {
        visibility:hidden;
    }

    header {
        visibility:hidden;
    }

    [data-testid="stSidebarNav"] {
        display:none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -------- LOGIN CHECK --------

if "token" not in st.session_state:

    show_login()
    st.stop()


# -------- GET USER ROLE --------

token = st.session_state["token"]

decoded = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"]
)

role = decoded["role"]


# -------- SIDEBAR --------

with st.sidebar:

    menu_options = [
        "Dashboard",
        "Upload Resume"
    ]

    # Recruiter/Admin only
    if role in ["admin", "recruiter"]:

        menu_options.extend(
            [
                "Analysis History",
                "Candidate Rankings",
                "Skill Search"
            ]
        )

    page = option_menu(
        "AI Resume Analyzer",
        menu_options
    )

    st.markdown("---")

    if st.button("Logout"):
        
        st.session_state.clear()
        
        st.rerun()


# -------- PAGE ROUTING --------

if page == "Dashboard":

    show_dashboard()

elif page == "Upload Resume":

    show_upload_resume()

elif page == "Analysis History":

    show_analysis_history()

elif page == "Candidate Rankings":

    show_candidate_rankings()

elif page == "Skill Search":

    show_skill_search()