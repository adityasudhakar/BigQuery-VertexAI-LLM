
import streamlit as st
from streamlit_chat import message as st_message
from bq_qna import bq_qna

def main():
    st.title("BigQuery QnA Chatbot")

    # Initialize session state variables for storing conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Input box for the question
    question = st.text_input("Enter your question:")

    if st.button("Send"):
        if question:
            try:
                # Call the bq_qna function with the user's question
                answer, intermediate_steps = bq_qna(question)

                # Append question, answer, and intermediate steps to the conversation history
                st.session_state.conversation.append((question, answer, intermediate_steps))

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a question")

    # Display the conversation history using streamlit_chat
    for i, (q, a, steps) in enumerate(st.session_state.conversation):
        st_message(q, is_user=True, key=str(i) + '_user')
        st_message(a, is_user=False, key=str(i) + '_bot')
        with st.expander(f"Intermediate Steps for Q {i+1}"):
            st.write(steps)

    # Button to clear the conversation history
    if st.button("Clear Conversation"):
        st.session_state.conversation = []

if __name__ == "__main__":
    main()
