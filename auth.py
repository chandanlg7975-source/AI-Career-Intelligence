import streamlit as st

from database.database import register_user, login_user


def show_auth_page():
    st.title("🔐 AI Career Intelligence")

    st.subheader("Welcome!")

    tab1, tab2 = st.tabs([
        "🔑 Login",
        "📝 Register"
    ])

    # ---------------- LOGIN ----------------
    with tab1:
        st.markdown("### Login to your account")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔑 Login",
            use_container_width=True
        ):
            if not email or not password:
                st.warning("Please enter your email and password.")

            else:
                user = login_user(
                    email,
                    password
                )

                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user

                    st.success(
                        f"Welcome, {user['name']}!"
                    )

                    st.rerun()

                else:
                    st.error(
                        "Invalid email or password."
                    )

    # ---------------- REGISTER ----------------
    with tab2:
        st.markdown("### Create a new account")

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):
            if not name or not email or not password:
                st.warning(
                    "Please fill in all fields."
                )

            elif password != confirm_password:
                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:
                st.error(
                    "Password must contain at least 6 characters."
                )

            else:
                success, message = register_user(
                    name,
                    email,
                    password
                )

                if success:
                    st.success(message)
                    st.info(
                        "Your account has been created. "
                        "You can now login."
                    )

                else:
                    st.error(message)


def logout():
    st.session_state["logged_in"] = False
    st.session_state.pop("user", None)
    st.rerun()