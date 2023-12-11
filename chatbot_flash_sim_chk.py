import streamlit as st
import spacy

st.title("Similarity Check Bot")

# Load spaCy medium model with word vectors
nlp = spacy.load("en_core_web_md")

#Create a question list and an answer list from the data file:
data_file=open("fc_data.txt","r")
content = data_file.readlines()
questions=content[0::2]
answers=content[1::2]
q_len= len(questions)

if "questions" not in st.session_state:
    st.session_state.questions = questions


if "answers" not in st.session_state:
    st.session_state.answers = answers

if "messages" not in st.session_state:
    st.session_state.messages = []    

# Initialize question index
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# Use st.form to organize layout
with st.form(key='user_input_form'):
    # Display user question in chat message container
    user_message_placeholder = st.empty()
    user_message_placeholder.chat_message("user").markdown(st.session_state.questions[st.session_state.question_index])

    # Wait for user input
    user_input = st.text_area("Your response:", key=f"user_input_{st.session_state.question_index}")

    # Check if the user provided a response
    if st.form_submit_button("Submit"):
        reference_answer = st.session_state.answers[st.session_state.question_index]
        similarity_score = nlp(user_input).similarity(nlp(reference_answer))

        # Generate a response based on similarity score
        if similarity_score > 0.7:
            response = "Your response is similar to the expected answer!"
        else:
            response = f"My expected answer was: {reference_answer}"

        # Display assistant response in chat message container
        assistant_message_placeholder = st.empty()
        assistant_message_placeholder.chat_message("assistant").markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Increment question index for the next iteration
        st.session_state.question_index += 1

# Display the next question if available
if st.session_state.question_index < len(st.session_state.questions):
    st.text("")  # Add an empty space for layout separation
    user_message_placeholder.chat_message("user").markdown(st.session_state.questions[st.session_state.question_index])

# Reset the question index if all questions are answered
if st.session_state.question_index == len(st.session_state.questions):
    st.session_state.question_index = 0
