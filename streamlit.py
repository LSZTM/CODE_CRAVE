import streamlit as st
import json
import time
import requests
import pandas as pd

# Initialize session state for the quiz taker
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0

if "start_time" not in st.session_state:
    st.session_state["start_time"] = None

if "total_time" not in st.session_state:
    st.session_state["total_time"] = 0

if "answered_questions" not in st.session_state:
    st.session_state["answered_questions"] = set()

if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}

# Load quiz data from JSON file
if "quiz_data" not in st.session_state:
    try:
        with open("quiz.json", "r") as f:
            st.session_state["quiz_data"] = json.load(f)
    except FileNotFoundError:
        st.error("The quiz.json file was not found. Please create a quiz first.")
        st.session_state["quiz_data"] = None

# --- Custom Styling ---
def add_custom_styles():
    """Adds custom CSS styles to the Streamlit app."""
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://r4.wallpaperflare.com/wallpaper/142/751/831/landscape-anime-digital-art-fantasy-art-wallpaper-9b468c3dc3116f4905f43bc9cddc0cf0.jpg');
            background-size: cover;
            background-position: center center;
            color: white;
        }
        h1, h2, h3 {
            text-align: center;
            font-weight: bold;
            color: #FFFFFF;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        .stButton > button {
            background-color: #1C1C1C;
            color: white;
            border-radius: 12px;
            padding: 15px 30px;
            font-size: 20px;
            border: solid 2px #F9D539;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
            margin: 10px auto;
            display: block;
            cursor: pointer;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #333333;
        }
        .stExpander {
            background-color: rgba(62, 42, 71, 0.8);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4);
            color: #FFFFFF;
            width: 80%;
            margin: 10px auto;
        }
        .stExpander header {
            font-size: 1.2rem;
            font-weight: bold;
            color: #F9D539;
        }
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
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Airtable Configuration ---
AIRTABLE_API_KEY = "pat3iS2qBn8ieAsKb.c9f71a1d00093034e336d13e96ee87eacf14cc8fb8ca4cccd221d8184a302aa5"
BASE_ID = "appkzzJcyMwiRFMNp"
TABLE_NAME = "Leaderboard"

# --- Airtable Functions ---
def update_leaderboard(username, score, elapsed_time):
    """Adds a new player record to the Airtable leaderboard."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "records": [
            {
                "fields": {
                    "username": username,
                    "score": score,
                    "time": elapsed_time
                }
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        st.error(f"Failed to update leaderboard. Status: {response.status_code}")
        st.error(response.json())

def get_leaderboard():
    """Retrieves and returns the leaderboard from Airtable as a DataFrame."""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        records = response.json().get("records", [])
        leaderboard_data = [record.get("fields", {}) for record in records]
        
        if leaderboard_data:
            df = pd.DataFrame(leaderboard_data)
            # Ensure required columns exist before sorting
            if 'score' in df.columns and 'time' in df.columns:
                 df = df.sort_values(by=["score", "time"], ascending=[False, True])
            return df
    else:
        st.error(f"Failed to fetch leaderboard. Status: {response.status_code}")
    
    return pd.DataFrame(columns=["username", "score", "time"])


# --- Main Quiz Taker Application ---
def quiz_taker():
    add_custom_styles()

    if not st.session_state.get("quiz_data"):
        st.title("CAMPUS CODERS '25")
        st.warning("Quiz data is not available. Please contact the administrator.")
        return

    # Initialize session state variables for the quiz taker page
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "quiz_started" not in st.session_state:
        st.session_state["quiz_started"] = False
    if "leaderboard" not in st.session_state:
        st.session_state["leaderboard"] = get_leaderboard()

    def has_completed_quiz(username):
        """Check if a user has already completed the quiz."""
        if not st.session_state["leaderboard"].empty and 'username' in st.session_state["leaderboard"].columns:
            return username in st.session_state["leaderboard"]["username"].values
        return False

    # User details entry screen
    if not st.session_state["quiz_started"]:
        st.title("Enter Your Details")
        username = st.text_input("Enter your username:", key="username_input")

        if st.button("Start Quiz"):
            if not username.strip():
                st.warning("⚠️ Please enter a valid username.")
            elif has_completed_quiz(username):
                st.error("❌ You have already completed the quiz! You cannot retake it.")
            else:
                st.session_state["username"] = username
                st.session_state["current_question"] = 0
                st.session_state["user_answers"] = {}
                st.session_state["answered_questions"] = set()
                st.session_state["start_time"] = time.time()
                st.session_state["quiz_started"] = True
                st.rerun()
        return

    # --- Quiz Gameplay Screen ---
    quiz_data = st.session_state["quiz_data"]
    st.title(f"{quiz_data.get('title', 'Quiz Battle')}")
    st.write(f"**Username:** {st.session_state['username']}")

    questions = quiz_data.get("questions", [])
    if not questions:
        st.error("No questions found in the quiz data.")
        return

    current_question_idx = st.session_state["current_question"]
    num_questions_to_ask = min(len(questions), 15)

    # Quiz Completion Screen
    if len(st.session_state["answered_questions"]) == num_questions_to_ask or current_question_idx >= num_questions_to_ask:
        st.success("🎉 Quiz Completed! 🎉")

        correct_answers = sum(
            1 for i, q in enumerate(questions[:num_questions_to_ask])
            if st.session_state["user_answers"].get(i) == q["options"][q["correct_option"]]
        )
        score_percentage = int((correct_answers / num_questions_to_ask) * 100)
        elapsed_time = round(time.time() - st.session_state["start_time"], 2)

        st.subheader(f"Your Score: {score_percentage}% in {elapsed_time} seconds")

        if not has_completed_quiz(st.session_state["username"]):
            update_leaderboard(st.session_state["username"], score_percentage, elapsed_time)
            st.session_state["leaderboard"] = get_leaderboard()

        st.subheader("🏆 Leaderboard")
        leaderboard_df = st.session_state["leaderboard"]
        if not leaderboard_df.empty:
            leaderboard_df.index = range(1, len(leaderboard_df) + 1)
            st.dataframe(
                leaderboard_df,
                use_container_width=True,
                column_config={
                    "username": "👤 Username",
                    "score": st.column_config.ProgressColumn("🎯 Score (%)", min_value=0, max_value=100),
                    "time": "⏱ Time (s)"
                }
            )
        else:
            st.write("No players on the leaderboard yet.")

        with st.expander("📜 Your Answers Summary"):
            for i, q in enumerate(questions[:num_questions_to_ask]):
                user_ans = st.session_state["user_answers"].get(i, "Not Answered")
                correct_ans = q["options"][q["correct_option"]]
                is_correct = "✅" if user_ans == correct_ans else "❌"
                st.write(f"**Q{i+1}: {q['question']}**")
                st.write(f"  {is_correct} Your Answer: {user_ans}")
                if user_ans != correct_ans:
                    st.write(f"  Correct Answer: {correct_ans}")
                st.divider()
        return

    # Display Current Question
    question = questions[current_question_idx]
    with st.expander(f"❓ Question {current_question_idx + 1} of {num_questions_to_ask}", expanded=True):
        st.write(f"**{question['question']}**")

        options = question.get("options", [])
        user_answer = st.radio(
            "Select your answer:",
            options=options,
            key=f"answer_{current_question_idx}",
            index=None
        )

        if st.button("✅ Submit Answer", disabled=(user_answer is None)):
            st.session_state["user_answers"][current_question_idx] = user_answer
            st.session_state["answered_questions"].add(current_question_idx)
            st.session_state["current_question"] += 1
            st.rerun()

    st.markdown(
        f'<div class="questions-submitted-card">📌 Questions Submitted: {len(st.session_state["answered_questions"])} / {num_questions_to_ask}</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    quiz_taker()
