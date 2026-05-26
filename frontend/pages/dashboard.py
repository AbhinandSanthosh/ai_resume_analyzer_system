import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def show_dashboard():

    st.title("AI Resume Analytics Dashboard")

    headers = {
        "Authorization":
        f"Bearer {st.session_state.get('token','')}"
        }

    history_response = requests.get(
        "http://127.0.0.1:8000/analysis-history",
        headers=headers
        )

    if history_response.status_code == 200:

        history = history_response.json()

        df = pd.DataFrame(history)

        total_resumes = len(df)

        average_score = (
            round(df["score"].mean(), 2)
            if total_resumes > 0
            else 0
        )

        all_skills = []

        if (
            total_resumes > 0
            and
            "strengths" in df.columns
        ):

            for strengths in df["strengths"]:

                if strengths:

                    all_skills.extend(
                        strengths.split(",")
                    )

        top_skill = (
            all_skills[0]
            if len(all_skills) > 0
            else "N/A"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Analyses",
                total_resumes
            )

        with col2:
            st.metric(
                "Average Score",
                f"{average_score}%"
            )

        with col3:
            st.metric(
                "Top Skill",
                top_skill
            )

        st.divider()

        if total_resumes > 0:

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:

                score_chart = px.bar(
                    df,
                    x="resume_id",
                    y="score",
                    text="score",
                    title="Resume Scores"
                )

                st.plotly_chart(
                    score_chart,
                    width="stretch"
                )

            with chart_col2:

                if len(all_skills) > 0:

                    skill_df = pd.DataFrame(
                        {"skill": all_skills}
                    )

                    skill_count = (
                        skill_df["skill"]
                        .value_counts()
                        .reset_index()
                    )

                    skill_count.columns = [
                        "skill",
                        "count"
                    ]

                    pie_chart = px.pie(
                        skill_count,
                        names="skill",
                        values="count",
                        title="Skills Distribution"
                    )

                    st.plotly_chart(
                        pie_chart,
                        width="stretch"
                    )

        st.divider()

        st.subheader("Analysis History")

        st.dataframe(
            df,
            height=350,
            width="stretch"
        )

    else:

        st.error(
            "Failed to load dashboard data"
        )

        st.write(
            history_response.text
        )