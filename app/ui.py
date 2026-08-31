import requests
import streamlit as st

st.set_page_config(
    page_title="DevOps Docs Assistant",
    page_icon="🤖"
)

st.title("🤖 DevOps Docs Assistant")
st.write("Ask questions about the DevOps documentation.")


query = st.text_input(
    "Ask your question:"
)


if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        response = requests.get(
            "http://127.0.0.1:8000/ask",
            params={"query": query}
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources")

            for source in data["sources"]:
                st.write(f"- {source}")

        else:
            st.error("Something went wrong.")