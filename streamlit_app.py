import streamlit as st
from get_feedback import general_feedback, similarity_feedback, correctness_feedback
from get_score import get_initial_score, get_final_score
from correctness import correctness_score
from marking_guide import similarity_score
from relevance import score_relevance
from structure import score_structure
from grammar import score_grammar

# Streamlit settings
st.set_page_config(
    page_title="AutoExam",
    page_icon="ACAD_AI_LOGO.png",
    layout="centered",
    initial_sidebar_state="auto"
)

st.get_option("theme.primaryColor")

# Streamlit UI

st.logo("ACAD_AI_LOGO.png",)
st.title("AutoExam")
st.markdown("By Acad AI")
st.info("This is only a demo that lets you see the potential of AI in grading theory exams. You can grade student answers based on a marking guide or without one. You can also customize the grading criteria to suit your needs.")

question = st.text_area("Enter a question", "")
answer = st.text_area("Enter the Student's Answer", "")

# Sidebar grading settings
st.sidebar.header("Grading Settings")

use_marking_guide = st.sidebar.toggle("Use Marking Guide", True,)

if use_marking_guide == True:
    marking_guide = st.sidebar.text_area("Enter the Marking Guide: ", "")
else:
    marking_guide = None

max_score = st.sidebar.number_input("Maximum Score for this Question", min_value=1, max_value=100, value=10)

st.sidebar.markdown("#### Customize Grading Rubrics")
grammar_weight = st.sidebar.slider("Grammar Weight", 0.0, 1.0, 0.0)
structure_weight = st.sidebar.slider("Structure Weight", 0.0, 1.0, 0.0)
relevance_weight = st.sidebar.slider("Relevance Weight", 0.0, 1.0, 0.3)

strictness = st.sidebar.slider("Strictness", 0.0, 1.0, 0.5)
further_instructions = st.sidebar.text_area("Further Instructions (optional): ", "")
if st.button("Grade Answer"):
    if  answer and question:
        initial_score = get_initial_score(question, answer, marking_guide, further_instructions, max_score, use_marking_guide, strictness)
        grammar_score = score_grammar(answer, strictness)
        structure_score = score_structure(answer, strictness)
        relevance_score = score_relevance(question, answer, strictness)
        final_score = get_final_score(initial_score, grammar_score, structure_score, relevance_score, grammar_weight, structure_weight, relevance_weight)

        st.write(f"### Final Score: {final_score}/{max_score}")
        if final_score == initial_score:
            if use_marking_guide:
                feedback = similarity_feedback(question, marking_guide, answer, further_instructions, strictness, initial_score, max_score)
            else:
                feedback = correctness_feedback(question, answer, further_instructions, strictness, initial_score, max_score)

        else:
            feedback = general_feedback(question, answer, marking_guide, initial_score, final_score, max_score, grammar_score, structure_score, relevance_score, grammar_weight, structure_weight, relevance_weight, strictness, further_instructions)

        st.markdown(f"### Feedback: \n\n{feedback}", unsafe_allow_html=True)
    else:
        st.warning("Please enter a question and student's answer to grade.")
