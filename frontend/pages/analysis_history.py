import streamlit as st
import requests
import pandas as pd


def show_analysis_history():

    headers = {
    "Authorization":
    f"Bearer {st.session_state.get('token','')}"
    }

    st.title("Analysis History")

    response = requests.get(
        "http://127.0.0.1:8000/analysis-history",
        headers=headers
    )

    if response.status_code == 200:

        history = response.json()

        if len(history) == 0:

            st.warning(
                "No analysis history found"
            )

        else:

            df = pd.DataFrame(history)

            st.dataframe(
                df,
                width="stretch"
            )

    else:

        st.error(
            "Failed to load history"
        )