import streamlit as st
import requests

st.title("🔍 LLM-based RAG Search")
st.markdown("Ask anything and get an AI-generated answer based on real web data.")

# Input for user query
query = st.text_input("Enter your query:")

if st.button("Search"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        try:
            st.write("⏳ Searching and generating answer...")
            response = requests.post(
                "http://localhost:5001/query",  # Flask backend endpoint
                json={"query": query}
            )

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                st.success("✅ Answer:")
                st.write(answer)
            else:
                st.error(f"❌ Error from backend: {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.error(f"Exception occurred: {e}")