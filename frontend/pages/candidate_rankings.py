import streamlit as st
import requests
import pandas as pd


def show_candidate_rankings():

    st.title("Candidate Rankings")

    headers = {
        "Authorization":
        f"Bearer {st.session_state.get('token','')}"
    }

    response = requests.get(
        "http://127.0.0.1:8000/candidate-rankings",
        headers=headers
    )

    if response.status_code == 200:

        rankings = response.json()

        if len(rankings) == 0:

            st.warning(
                "No rankings available"
            )

        else:

            df = pd.DataFrame(rankings)

            st.dataframe(
                df,
                width="stretch"
            )

    else:

        st.error(
            "Failed to load rankings"
        )

        st.write(
            "Status:",
            response.status_code
        )

        st.json(
            response.json()
        )