import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Import backend functions directly
from backend.ai import generate_sql
from backend.db import run_query

st.set_page_config(
    page_title="Netflix AI",
    page_icon="🎬",
    layout="wide"
)

# ---------- GLASSMORPHISM CSS ----------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827);
    color:white;
}

section[data-testid="stSidebar"]{
    background: rgba(17,24,39,0.7);
    backdrop-filter: blur(20px);
    border-right:1px solid rgba(255,255,255,0.1);
}

.stTextInput input{
    background: rgba(255,255,255,0.05);
    color:white;
    border-radius:15px;
}

.stButton>button{
    background: rgba(59,130,246,0.3);
    color:white;
    border:none;
    border-radius:15px;
}

h1,h2,h3{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "saved_queries" not in st.session_state:
    st.session_state.saved_queries = []

if "current_sql" not in st.session_state:
    st.session_state.current_sql = ""

if "current_result" not in st.session_state:
    st.session_state.current_result = None

# ---------- SIDEBAR ----------
with st.sidebar:

    st.title("🎬 Netflix AI")

    selected = option_menu(
        menu_title=None,
        options=[
            "New Query",
            "Query History",
            "Saved Queries",
            "Documentation",
            "Settings"
        ],
        icons=[
            "plus-circle",
            "clock-history",
            "bookmark-star",
            "book",
            "gear"
        ],
        default_index=0
    )

# ---------- NEW QUERY ----------
if selected == "New Query":

    left, right = st.columns([3,1])

    with left:

        st.title("Ask Your Database")

        question = st.text_input(
            "Question",
            placeholder="Show movies released in 2018"
        )

        if st.button("Run Query"):

            if question:

                try:
                    sql = generate_sql(question)
                    results = run_query(sql)

                    st.session_state.current_sql = sql
                    st.session_state.current_result = results

                    st.session_state.history.append(
                        {
                            "question": question,
                            "sql": sql,
                            "result": results
                        }
                    )

                except Exception as e:
                    st.error(f"Error: {str(e)}")

        if st.session_state.current_result is not None:

            st.subheader("Generated SQL")

            st.code(
                st.session_state.current_sql,
                language="sql"
            )

            df = pd.DataFrame(
                st.session_state.current_result
            )

            st.subheader("Results")

            st.dataframe(
                df,
                use_container_width=True,
                height=500
            )

            csv = df.to_csv(index=False)

            st.download_button(
                "📥 Download CSV",
                csv,
                file_name="results.csv"
            )

    with right:

        st.subheader("Suggestions")

        st.info("Highest rated movies")
        st.info("Top 10 TV Shows")
        st.info("Movies released after 2020")
        st.info("Longest duration movies")
        st.info("Most common genres")

# ---------- QUERY HISTORY ----------
elif selected == "Query History":

    st.title("Query History")

    if len(st.session_state.history) == 0:
        st.info("No queries yet")

    else:

        for i, item in enumerate(
                reversed(st.session_state.history), 1):

            with st.expander(
                    f"{i}. {item['question']}"):

                st.subheader("Generated SQL")

                st.code(
                    item["sql"],
                    language="sql"
                )

                df = pd.DataFrame(
                    item["result"]
                )

                st.subheader("Results")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                if st.button(f"⭐ Save Query {i}", key=f"save_{i}"):

                    st.session_state.saved_queries.append(item)

# ---------- SAVED QUERIES ----------
elif selected == "Saved Queries":

    st.title("Saved Queries")

    if len(st.session_state.saved_queries) == 0:

        st.info("No saved queries")

    else:

        for i, item in enumerate(st.session_state.saved_queries):

            with st.expander(item["question"]):

                st.code(
                    item["sql"],
                    language="sql"
                )

                df = pd.DataFrame(
                    item["result"]
                )

                st.dataframe(
                    df,
                    use_container_width=True
                )

# ---------- DOCUMENTATION ----------
elif selected == "Documentation":

    st.title("Documentation")

    st.markdown("""
## Example Questions

- Show movies released in 2018
- Show top 10 TV Shows
- Show longest duration movies
- Count movies by genre
- Show documentaries
- Show movies after 2020

## Architecture

User  
↓  
Streamlit UI  
↓  
Gemini AI (NL → SQL)  
↓  
SQLite Database  
↓  
Results
""")

# ---------- SETTINGS ----------
elif selected == "Settings":

    st.title("Settings")

    if st.button("🗑 Clear History"):
        st.session_state.history = []

    if st.button("⭐ Clear Saved Queries"):
        st.session_state.saved_queries = []

    if st.button("♻ Reset Current Result"):
        st.session_state.current_result = None
        st.session_state.current_sql = ""