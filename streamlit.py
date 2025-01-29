import streamlit as st
import json
import time

# Initialize session state for keys that may not exist
if "questions" not in st.session_state:
    st.session_state["questions"] = []

if "quiz_title" not in st.session_state:
    st.session_state["quiz_title"] = ""

if "quiz_semester" not in st.session_state:
    st.session_state["quiz_semester"] = "1"

if "num_questions" not in st.session_state:
    st.session_state["num_questions"] = 0

if "question_times" not in st.session_state:
    st.session_state["question_times"] = []  # Initialize as an empty list to store time limits for questions

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0  # Keeps track of which question the user is attempting

if "start_time" not in st.session_state:
    st.session_state["start_time"] = None  # Track when the user starts the question

if "total_time" not in st.session_state:
    st.session_state["total_time"] = 0  # Track total time spent on the quiz

if "answered_questions" not in st.session_state:
    st.session_state["answered_questions"] = []  # List to track answered questions

if "quiz_data" not in st.session_state:
    # Load quiz from JSON (assuming quiz.json exists)
    try:
        with open("quiz.json", "r") as f:
            st.session_state["quiz_data"] = json.load(f)
    except:
        st.error("No quiz available to take!")
        st.session_state["quiz_data"] = {}

# Reset form data for a new question
def reset_question_form():
    st.session_state["question_times"] = []





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

# Quiz Taker functionality



# Initialize session state
if "quiz_data" not in st.session_state:
    try:
        with open("quiz.json", "r") as f:
            st.session_state["quiz_data"] = json.load(f)
    except FileNotFoundError:
        st.session_state["quiz_data"] = None

if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

if "answered_questions" not in st.session_state:
    st.session_state["answered_questions"] = []

if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}


# Add custom styles
def add_custom_styles():
    """
    Adds custom CSS styles to the Streamlit app for visual enhancements.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://r4.wallpaperflare.com/wallpaper/142/751/831/landscape-anime-digital-art-fantasy-art-wallpaper-9b468c3dc3116f4905f43bc9cddc0cf0.jpg');
            background-size: cover;
            background-position: center center;
            color: white;
            display: flex; /* Center content vertically */
            justify-content: center;
            align-items: center;
            min-height: 100vh; /* Make app take up full viewport height */
        }

        h1 {
            text-align: center;
            font-weight: bold;
            color: #FFFFFF; 
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            font-family: 'Mincho', serif; /* Or 'Shinobi', serif */
            font-size: 3rem; /* Increase heading size */
        }

        .option-button {
            background-color: #1C1C1C; /* Matte black background */
            color: white;
            border-radius: 12px;
            padding: 15px 30px; 
            font-size: 20px;
            transition: 0.3s ease;
            border: solid 2px #F9D539; /* Added solid border */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4); /* Added box-shadow for text */
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3); /* Added box-shadow to the button */
            width: 200px; /* Maintains original button width */
            margin: 10px auto;
            display: block;
            cursor: pointer;
        }

        .option-button:hover {
            background-color: #333333; /* Slightly lighter black on hover */
        }

        .landing-container {
            text-align: center;
            padding: 20px;
        }

        .stButton > button {
            background-color: #1C1C1C; /* Matte black background */
            color: white;
            border-radius: 12px;
            padding: 15px 30px; 
            font-size: 20px;
            transition: 0.3s ease;
            border: solid 2px #F9D539; /* Added solid border */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4); /* Added box-shadow for text */
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3); /* Added box-shadow to the button */
            margin: 10px auto;
            display: block;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #333333; /* Slightly lighter black on hover */
        }

        /* Re-aligned question button navigation */
        .question-nav {
            display: flex;
            justify-content: center; /* Center the buttons horizontally */
            align-items: center;
            margin-top: 20px;
        }

        .question-nav .stButton > button {
            margin: 0 10px; /* Add spacing between buttons */
        }

        .stExpander {
            background-color: #3E2A47;
            border-radius: 12px;
            padding: 20px; 
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4); 
            font-size: 1rem;
            color: #FFFFFF; 
            width: 80%; 
            margin: 10px auto; 
        }

        .stExpander header {
            font-size: 1.2rem; 
            font-weight: bold;
            color: #F9D539; 
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }

        .question-transition {
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .question-nav {
            display: flex;
            justify-content: center; /* Center the buttons horizontally */
            align-items: center;
            margin-top: 20px;
        }

        .question-nav button {
            font-size: 20px;
            background-color: #1C1C1C; /* Matte black background */
            color: white;
            border-radius: 10px;
            padding: 10px;
            transition: 0.3s ease;
            border: solid 2px #F9D539; /* Added solid border */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4); /* Added box-shadow for text */
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3); /* Added box-shadow to the button */
        }

        .question-nav button:hover {
            background-color: #333333; /* Slightly lighter black on hover */
        }

        /* Custom card style for question submission count */
        .questions-submitted-card {
            background-color: rgba(62, 42, 71, 0.8); 
            color: #F9D539; 
            padding: 20px; 
            border-radius: 12px;
            text-align: center;
            font-size: 1rem;
            font-weight: bold;
            margin: 20px auto;
            width: 80%; 
        }

        /* Optional: Add a subtle shadow to elements */
        .st-bw {
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        /* Optional: Smooth scrolling for better user experience */
        html, body {
            scroll-behavior: smooth;
        }
      </style>
      """,
      unsafe_allow_html=True
  )





# Quiz Taker functionality
def quiz_taker():
    add_custom_styles()  # Function to apply custom CSS styles

    quiz_data = st.session_state["quiz_data"]
    if not quiz_data:
        return

    if "username" not in st.session_state:
        st.session_state["username"] = ""

    if "quiz_started" not in st.session_state:
        st.session_state["quiz_started"] = False

    if not st.session_state["quiz_started"]:
        st.title("Enter Your Username")
        st.text_input("Username:", key="username")
        if st.button("Start Quiz"):
            if st.session_state["username"]:
                st.session_state["current_question"] = 0
                st.session_state["user_answers"] = {}
                st.session_state["answered_questions"] = set()
                st.session_state["start_time"] = time.time()
                st.session_state["quiz_started"] = True
                st.rerun()
            else:
                st.warning("Please enter a username.")
        return

    st.title(f"{quiz_data['title']}")

    current_question_idx = st.session_state["current_question"]
    questions = quiz_data["questions"]

    # ✅ Fix: Quiz only completes when all questions are answered
    if len(st.session_state["answered_questions"]) == len(questions):
        st.write(f"Username: {st.session_state['username']}")
        st.success("🎉 Quiz Completed! 🎉")

        correct_answers = sum(q["correct_option"] == a for q, a in zip(questions, st.session_state["user_answers"].values()))
        total_questions = len(questions)
        score_percentage = int((correct_answers / total_questions) * 100)
        elapsed_time = time.time() - st.session_state["start_time"]

        # ✅ Fix: Properly updating leaderboard
        if "leaderboard" not in st.session_state:
            st.session_state["leaderboard"] = []

        new_score = {
            "username": st.session_state["username"],
            "score": score_percentage,
            "time": elapsed_time
        }
        st.session_state["leaderboard"].append(new_score)
        st.session_state["leaderboard"].sort(key=lambda x: (-x["score"], x["time"]))

        # 🏆 Display leaderboard
        st.subheader("🏆 Leaderboard")

        if not st.session_state["leaderboard"]:
            st.info("No scores yet. Be the first to take the quiz!")
        else:
            leaderboard_md = """
            <style>
                .leaderboard-table { width: 100%; border-collapse: collapse; }
                .leaderboard-table th, .leaderboard-table td { 
                    border: 1px solid #ddd; 
                    padding: 8px; 
                    text-align: center; 
                    color: black;
                }
                .leaderboard-table th { background-color: #51789D; color: white; }
                .leaderboard-row:nth-child(odd) { background-color: #f2f2f2; }
            </style>
            <table class="leaderboard-table">
            <thead>
                <tr><th>🏅 Rank</th><th>👤 Username</th><th>🎯 Score (%)</th><th>⏱ Time (s)</th></tr>
            </thead>
            <tbody>  """

            for rank, entry in enumerate(st.session_state["leaderboard"][:5], start=1):
                leaderboard_md += f"""<tr class="leaderboard-row"><td><b>{rank}</b></td><td>{entry['username']}</td><td>{entry['score']}%</td><td>{entry['time']:.2f}</td></tr>"""

            leaderboard_md += """
            </tbody>  </table>
            """
            st.markdown(leaderboard_md, unsafe_allow_html=True)

            # 📜 Display Summary
            st.write(f"**Your Score:** {correct_answers}/{total_questions} ({score_percentage}%)")
            st.write(f"**Time Taken:** {elapsed_time:.2f} seconds")

            with st.expander("📜 Quiz Summary"):
                for i, q in enumerate(questions):
                    user_answer = st.session_state["user_answers"].get(i, "Not Answered")
                    correct_option = q["correct_option"]
                    correct_answer = questions[i]["options"][correct_option]
                    st.write(f"**Q{i + 1}:** {q['question']}")
                    st.write(f"**Your Answer:** {user_answer}")
                    st.write(f"✅ **Correct Answer:** {correct_answer}")

            return  # ✅ Exit early once quiz is complete

    # 📝 Display current question
    question = questions[current_question_idx]
    language = question.get("language", None)

    with st.expander(f"❓ Question {current_question_idx + 1}", expanded=True):
        if language:
            st.code(question['question'], language=language)
        else:
            st.write(f"**{question['question']}**")

        options = ["Select an answer"] + question["options"]
        user_answer = st.radio("Select an answer:", options=options, index=0, key=f"answer_{current_question_idx}")

    # 🚨 Prevent submission if "Select an answer" is chosen
    submit_disabled = user_answer == "Select an answer" or current_question_idx in st.session_state["answered_questions"]

    if submit_disabled:
        if user_answer == "Select an answer":
            st.warning("⚠️ Please select an option before submitting.")
        elif current_question_idx in st.session_state["answered_questions"]:
            st.info("✅ You have already submitted this question.")

    if st.button("✅ Submit Answer", disabled=submit_disabled):
        if user_answer != "Select an answer":
            st.session_state["user_answers"][current_question_idx] = user_answer
            st.session_state["answered_questions"].add(current_question_idx)

        # ✅ Move to next unanswered question
        next_question = next((i for i in range(len(questions)) if i not in st.session_state["answered_questions"]), None)
        st.session_state["current_question"] = next_question if next_question is not None else len(questions)

        st.rerun()

    # ⬅➡ Navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if current_question_idx > 0:
            if st.button("⬅ Previous Question"):
                st.session_state["current_question"] -= 1
                st.rerun()

    with col2:
        if current_question_idx < len(questions) - 1:
            if st.button("Next Question ➡"):
                st.session_state["current_question"] += 1
                st.rerun()

    # 📌 Track progress
    st.markdown(f'<div class="questions-submitted-card">📌 Questions Submitted: {len(st.session_state["answered_questions"])} / {len(questions)}</div>', unsafe_allow_html=True)

def add_landing_styles():
    """Adds custom CSS styles for the landing page with enhanced text effects and contrasting text colors."""
    st.markdown(
        """
        <style>
        body {
            background-color: #28282B; /* Set background color for the entire page */
            margin: 0; 
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh; 
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blink {
            50% { border-color: transparent; }
        }

        .landing-container {
            text-align: center;
            max-width: 800px;
            padding: 20px;
            color: #fff; 
            border: 2px solid #fff; /* Add a white border to the container */
            border-radius: 10px; /* Add rounded corners to the container */
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.2); /* Add a subtle shadow */
        }

        .instructions {
            font-size: 1.2rem; /* Increase font size for better visibility */
            color: #fff; /* Set text color to white for contrast */
            margin-bottom: 20px; 
        }

        .landing-title {
            font-size: 4rem;
            font-weight: bold;
            margin: 0;
            animation: fadeIn 2s ease forwards, typing 4s steps(40, end) 1s both, blink .5s step-end infinite;
            font-family: 'Montserrat', sans-serif;
            color: #FFFFFF;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
            white-space: nowrap;
            overflow: hidden;
            border-right: 2px solid #FFFFFF;
            text-align : center;
        }

        .landing-subtitle {
            font-size: 1.5rem;
            margin: 10px 0;
            animation: fadeIn 3s ease forwards;
            font-family: 'Montserrat', sans-serif;
            color: #E3E3E3;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            text-align: center;
        }

        .instructions {
            font-size: 1.2rem;
            margin-bottom: 15px;
        }

        .instructions li {
            margin-left: 20px; 
        }

        .instructions li span {
            font-weight: bold; /* Make points bold */
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def landing_page():
    add_landing_styles()
    st.markdown(
        """
        <h1 class="landing-title">CODE CRAVE '25</h1>
        <h3 class="landing-subtitle">AN ULTIMATE QUIZ BATTLE</h3>

        <div class="landing-container"> 
            <p class="instructions">General Instructions:</p>
            <ul class="instructions">
                <li><span>1)</span> Any 2 sections are to be attempted from the given 3 sections</li>
                <li><span>2)</span> From section 2 only one language is to be attempted</li>
                <li><span>3)</span> All questions of an attempted section will be considered for marking</li>
                <li><span>4)</span> If All 3 sections have been attempted, the best 2 will be considered</li>
                <li><span>5)</span> Every question carries a weightage of 1 point</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "landing_page"

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Landing Page", "Quiz Taker", "Quiz Maker"])
    if menu == "Landing Page":
        st.session_state["page"] = "landing_page"
    elif menu == "Quiz Taker":
        st.session_state["page"] = "quiz_taker"
    elif menu == "Quiz Maker":
        st.session_state["page"] = "quiz_maker"

    # Display the page based on the session state
    if st.session_state["page"] == "landing_page":
        landing_page()
    elif st.session_state["page"] == "quiz_taker":
        quiz_taker()
    elif st.session_state["page"] == "quiz_maker":
        quiz_maker()

if __name__ == "__main__":
    main()



