import streamlit as st
import pandas as pd
import random

# Title
st.title("📚 Flashcard App")

# Load flashcards from CSV
@st.cache_data
def load_flashcards():
    try:
        df = pd.read_csv("flashcards.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error loading flashcards: {e}")
        return []

flashcards = load_flashcards()

# Session State to track flashcard index
if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.show_answer = False

# Show Flashcard Question
if flashcards:
    card = flashcards[st.session_state.index]
    st.subheader(f"Q: {card['question']}")

    if st.session_state.show_answer:
        st.write(f"**A: {card['answer']}**")

    # Buttons for interaction
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show Answer"):
            st.session_state.show_answer = True
    with col2:
        if st.button("Next Card"):
            st.session_state.index = (st.session_state.index + 1) % len(flashcards)
            st.session_state.show_answer = False
else:
    st.warning("No flashcards found! Please upload a CSV file.")

# Upload CSV file option
st.sidebar.header("Upload Custom Flashcards")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    flashcards.extend(df.to_dict(orient="records"))
    st.sidebar.success("Flashcards added successfully!")
