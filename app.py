import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="EduSuite Web", layout="wide")

st.title("EduSuite Web — Public Edition")
st.subheader("Secondary Assessment & Instruction System")

# -----------------------------------------------------
# SESSION STORAGE
# -----------------------------------------------------

if "gradebook" not in st.session_state:
    st.session_state.gradebook = []

if "answer_keys" not in st.session_state:
    st.session_state.answer_keys = {}

# -----------------------------------------------------
# SUBJECT & CHAPTER SELECTION
# -----------------------------------------------------

subject = st.selectbox(
    "Select Subject",
    ["Advanced Physics", "Mathematics"]
)

chapter = st.selectbox(
    "Select Chapter / Topic",
    ["Chapter 1: Kinematics",
     "Chapter 2: Newton's Laws",
     "Chapter 3: Energy & Work"]
)

mode = st.radio(
    "Mode",
    ["Generate Test", "Grade Test"]
)

# -----------------------------------------------------
# ADVANCED PHYSICS QUESTION ENGINE
# -----------------------------------------------------

def physics_question():

    if "Kinematics" in chapter:
        v = random.randint(5, 30)
        t = random.randint(2, 10)
        correct = v * t
        return f"An object moves at {v} m/s for {t} seconds. How far does it travel?", correct

    elif "Newton" in chapter:
        m = random.randint(1, 20)
        a = random.randint(1, 10)
        correct = m * a
        return f"What force is required to accelerate a {m} kg mass at {a} m/s²?", correct

    else:
        m = random.randint(1, 20)
        v = random.randint(2, 15)
        correct = round(0.5 * m * v**2, 2)
        return f"What is the kinetic energy of a {m} kg object moving at {v} m/s?", correct

# -----------------------------------------------------
# GENERATE TEST
# -----------------------------------------------------

if mode == "Generate Test":

    if st.button("Generate Structured Test (Versions A/B/C)"):

        versions = ["A", "B", "C"]
        output = ""

        for version in versions:

            output += f"\n\n===== Version {version} =====\n\n"
            answer_key = []

            for i in range(1, 6):

                if subject == "Advanced Physics":
                    question, correct = physics_question()
                else:
                    a = random.randint(5, 25)
                    b = random.randint(5, 25)
                    correct = a + b
                    question = f"What is {a} + {b}?"

                options = [correct, correct+2, correct-3, correct+5]
                random.shuffle(options)
                letters = ["A", "B", "C", "D"]

                output += f"{i}. {question}\n"
                for letter, option in zip(letters, options):
                    output += f"   {letter}. {option}\n"

                correct_letter = letters[options.index(correct)]
                answer_key.append(correct_letter)

            output += "\nShort Response:\nExplain one principle used in solving the problems.\n"

            st.session_state.answer_keys[version] = answer_key

        st.text_area("Test (Copy / Print Ready)", output, height=600)

# -----------------------------------------------------
# GRADING MODE
# -----------------------------------------------------

elif mode == "Grade Test":

    student_name = st.text_input("Student Name")
    version = st.selectbox("Test Version", ["A", "B", "C"])

    if version not in st.session_state.answer_keys:
        st.warning("Generate a test first in this session.")
    else:

        correct_answers = st.session_state.answer_keys[version]
        student_answers = []

        for i in range(1, 6):
            ans = st.selectbox(f"Question {i}", ["A", "B", "C", "D"], key=f"q{i}")
            student_answers.append(ans)

        short_score = st.slider("Short Response Score (0–5)", 0, 5, 3)

        if st.button("Calculate Grade"):

            mc_score = sum(
                1 for i in range(5)
                if student_answers[i] == correct_answers[i]
            )

            total_score = mc_score + short_score
            max_score = 10
            percentage = round((total_score / max_score) * 100, 2)

            st.success(f"Score: {total_score}/10")
            st.success(f"Percentage: {percentage}%")

            st.session_state.gradebook.append(
                {
                    "Student": student_name,
                    "Version": version,
                    "Score": total_score,
                    "Percentage": percentage
                }
            )

# -----------------------------------------------------
# GRADEBOOK EXPORT
# -----------------------------------------------------

if st.session_state.gradebook:

    df = pd.DataFrame(st.session_state.gradebook)
    st.subheader("Gradebook")

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Gradebook CSV",
        data=csv,
        file_name="edusuite_gradebook.csv",
        mime="text/csv"
    )

st.divider()
st.caption("EduSuite Web — Public Edition v1")
