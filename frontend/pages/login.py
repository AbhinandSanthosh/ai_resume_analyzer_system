import streamlit as st
import requests


def show_login():

    st.title("Login")

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(
            "http://127.0.0.1:8000/login",
            json={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state[
                "token"
            ] = data[
                "access_token"
            ]

            st.success(
                "Login successful"
            )

            st.rerun()
        
        else:

            st.error(
                response.json()["detail"]
            )