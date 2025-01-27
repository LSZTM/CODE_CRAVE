def quiz_maker():
    add_custom_styles()

    # Quiz Title and other details
    st.title("Quiz Maker")
    st.text_input("Enter Quiz Title", key="quiz_title")
    st.selectbox("Select Semester", ["1", "2", "3", "4"], key="quiz_semester")
    st.number_input("Number of Questions", min_value=1, max_value=20, step=1, key="num_questions")

    if st.session_state["num_questions"] > 0:
        for i in range(st.session_state["num_questions"]):
            with st.expander(f"Question {i + 1}"):

                st.text_area(f"Enter Question {i + 1}", key=f"new_question_{i}")
                question_type = st.selectbox("Select Question Type", ["Multiple Choice", "True or False"], key=f"question_type_{i}")

                if question_type == "True or False":
                    st.session_state[f"options_count_{i}"] = 2
                else:
                    st.number_input(f"Number of Options for Question {i + 1}", min_value=2, max_value=4, step=1, key=f"options_count_{i}")

                options = []
                num_options = st.session_state.get(f"options_count_{i}", 0)
                for j in range(num_options):
                    options.append(st.text_input(f"Option {j + 1} for Question {i + 1}", key=f"options_{i}_{j}"))

                correct_option = st.selectbox(f"Select Correct Option for Question {i + 1}", options=[f"Option {j + 1}" for j in range(num_options)], index=0, key=f"correct_option_{i}")
                uploaded_file = st.file_uploader(f"Upload Image for Question {i + 1}", type=["jpg", "png", "jpeg"], key=f"image_{i}")

                if uploaded_file is not None:
                    st.image(uploaded_file, caption=f"Uploaded Image for Question {i + 1}", use_column_width=True)

                time_limit = st.number_input(f"Time Limit (seconds) for Question {i + 1}", min_value=10, max_value=300, step=10, key=f"time_limit_{i}")
                st.session_state["question_times"].append(time_limit)

                if st.button(f"Save Question {i + 1}", key=f"save_button_{i}"):

                    question = {
                        "question": st.session_state[f"new_question_{i}"],
                        "options": options,
                        "correct_option": int(correct_option.split()[1]) - 1,
                        "image": uploaded_file.name if uploaded_file else None,
                        "time_limit": time_limit
                    }
                    st.session_state["questions"].append(question)
                    reset_question_form()

    if st.button(f"Preview Quiz", key="preview_quiz_button"):
        st.subheader("Quiz Preview:")
        for idx, question in enumerate(st.session_state["questions"]):
            with st.expander(f"Question {idx + 1}"):
                st.write(f"**Question**: {question['question']}")
                if question["image"]:
                    st.image(question["image"], caption=f"Image for Question {idx + 1}", use_column_width=True)
                for i, option in enumerate(question["options"]):
                    st.write(f"Option {i + 1}: {option}")
                st.write(f"Time Limit: {question['time_limit']} seconds")

    if st.button(f"Save Entire Quiz", key=f"save_quiz_button"):
        quiz = {
            "title": st.session_state["quiz_title"],
            "semester": st.session_state["quiz_semester"],
            "num_questions": st.session_state["num_questions"],
            "questions": st.session_state["questions"]
        }
        with open("quiz.json", "w") as f:
            json.dump(quiz, f)
        st.success("Quiz saved successfully!")