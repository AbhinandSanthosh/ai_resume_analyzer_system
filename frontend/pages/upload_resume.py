import streamlit as st
import requests


def show_upload_resume():

    headers = {
        "Authorization":
        f"Bearer {st.session_state.get('token','')}"
    }

    st.title("Upload Resume")

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    job_description = st.session_state.get(
        "job_description",
        ""
    )

    job_description = st.text_area(
        "Enter Job Description",
        value=job_description,
        height=150
    )

    if st.button("Analyze Resume"):

        if uploaded_file is None:

            st.warning(
                "Please upload a resume"
            )

            return

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        # ---------- Upload Resume ----------

        upload_response = requests.post(
            f"http://127.0.0.1:8000/upload-resume?user_id={user_id}",
            files=files,
            headers=headers
        )

        if upload_response.status_code != 200:

            st.error(
                "Resume upload failed"
            )

            try:

                st.json(
                    upload_response.json()
                )

            except:

                st.write(
                    upload_response.text
                )

            return

        upload_data = upload_response.json()

        auto_job_description = upload_data.get(
            "suggested_job_description"
        )

        if auto_job_description:

            st.session_state[
                "job_description"
            ] = auto_job_description

            st.success(
                f"Suggested Role: {upload_data['suggested_role']}"
            )

        # ---------- Match Job ----------

        match_response = requests.post(
            "http://127.0.0.1:8000/match-job",
            json={
                "job_description":
                auto_job_description
            },
            headers=headers
        )

        if match_response.status_code != 200:

            st.error(
                "Job matching failed"
            )

            try:

                st.json(
                    match_response.json()
                )

            except:

                st.write(
                    match_response.text
                )

            return

        match_data = match_response.json()

        st.success(
            "Resume analyzed successfully"
        )

        st.subheader(
            "Analysis Results"
        )

        for candidate in match_data["candidate_matches"]:

            if (
                candidate["resume_id"]
                ==
                upload_data["resume_id"]
            ):

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Match Score",
                        f"{candidate['match_score']}%"
                    )

                with col2:

                    st.metric(
                        "Matched Skills",
                        len(candidate["matched_skills"])
                    )

                with col3:

                    st.metric(
                        "Missing Skills",
                        len(candidate["missing_skills"])
                    )

                with col4:

                    st.metric(
                        "Recommendations",
                        len(candidate["recommendations"])
                    )

                st.divider()

                st.subheader(
                    "Match Score"
                )

                st.progress(
                    int(candidate["match_score"])
                )

                st.write(
                    f"{candidate['match_score']}%"
                )

                st.divider()

                st.subheader(
                    "Matched Skills"
                )

                for skill in candidate["matched_skills"]:

                    st.success(
                        skill
                    )

                st.divider()

                st.subheader(
                    "Missing Skills"
                )

                for skill in candidate["missing_skills"]:

                    st.warning(
                        skill
                    )

                st.divider()

                st.subheader(
                    "💡 Recommendations"
                )

                for recommendation in candidate["recommendations"]:

                    st.info(
                        recommendation
                    )