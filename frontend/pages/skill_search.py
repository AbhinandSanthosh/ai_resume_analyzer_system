import streamlit as st
import requests
import pandas as pd


def show_skill_search():

    st.title("Skill Search")

    skill = st.text_input(
        "Enter Skill"
    )

    if st.button("Search"):

        response = requests.get(
            f"http://127.0.0.1:8000/search-by-skill?skill={skill}"
        )

        if response.status_code == 200:

            data = response.json()

            if len(data) == 0:

                st.warning(
                    "No candidates found"
                )

            else:

                st.success(
                    f"Found {len(data)} candidates"
                )

                df = pd.DataFrame(data)

                st.dataframe(
                    df,
                    width="stretch"
                )

        else:

            st.error(
                "Search failed"
            )