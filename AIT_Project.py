import streamlit as st
import pandas as pd

# ============== OOP Classes ==============

class Question:
    """Class to represent a single quiz question"""
    
    def __init__(self, question_text, options, correct_answer):
        """Initialize a question with text, options, and correct answer"""
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
    
    def check_answer(self, selected_answer):
        """Check if the selected answer is correct"""
        return selected_answer == self.correct_answer


class Quiz:
    """Class to manage the quiz"""
    
    def __init__(self, list_of_questions):
        """Initialize quiz with a list of questions"""
        self.list_of_questions = list_of_questions
        self.score = 0
    
    def get_question(self, question_index):
        """Get a question by its index"""
        if question_index < len(self.list_of_questions):
            return self.list_of_questions[question_index]
        return None
    
    def calculate_score(self, answers):
        """Calculate the final score based on answers"""
        self.score = 0
        for i, selected_answer in enumerate(answers):
            if self.list_of_questions[i].check_answer(selected_answer):
                self.score += 1
        return self.score
    
    def get_review_data(self, answers):
        """Generate review data for all questions and answers"""
        review_data = []
        for i, question in enumerate(self.list_of_questions):
            user_answer = answers[i] if i < len(answers) else "Not answered"
            correct_answer = question.correct_answer
            is_correct = question.check_answer(user_answer)
            
            review_data.append({
                "Q#": i + 1,
                "Question": question.question_text,
                "Your Answer": user_answer,
                "Correct Answer": correct_answer,
                "Status": "✅ Correct" if is_correct else "❌ Incorrect"
            })
        return review_data
    
    def reset_quiz(self):
        """Reset the quiz"""
        self.score = 0


# ============== Quiz Questions ==============

questions_data = [
    # Beginner Level (Python Basics)
    Question("What is Python?", 
             ["A) Low-level language", "B) High-level programming language", "C) Machine code", "D) Markup language"],
             "B) High-level programming language"),
    
    Question("Which keyword is used to define a function in Python?",
             ["A) function", "B) def", "C) fun", "D) define"],
             "B) def"),
    
    Question("Which data type is used to store text in Python?",
             ["A) int", "B) float", "C) str", "D) bool"],
             "C) str"),
    
    Question("What is the output of: print(2 + 3 * 4)?",
             ["A) 20", "B) 14", "C) 24", "D) 10"],
             "B) 14"),
    
    Question("Which symbol is used for comments in Python?",
             ["A) //", "B) <!-- -->", "C) #", "D) /* */"],
             "C) #"),
    
    Question("Which function is used to take input from the user?",
             ["A) input()", "B) scan()", "C) read()", "D) get()"],
             "A) input()"),
    
    Question("What does len() function do?",
             ["A) Adds numbers", "B) Counts characters/items", "C) Converts data type", "D) Prints output"],
             "B) Counts characters/items"),
    
    Question("Which loop is used to iterate over a sequence?",
             ["A) while", "B) for", "C) do-while", "D) repeat"],
             "B) for"),
    
    Question("Which of the following is a mutable data type?",
             ["A) tuple", "B) string", "C) list", "D) int"],
             "C) list"),
    
    Question("What is the correct file extension for Python files?",
             ["A) .pt", "B) .python", "C) .py", "D) .p"],
             "C) .py"),
    
    # OOP Level (Python OOP Concepts)
    Question("What is OOP?",
             ["A) A programming error", "B) Object-Oriented Programming", "C) Only Optional Programming", "D) Operating Output Program"],
             "B) Object-Oriented Programming"),
    
    Question("Which keyword is used to create a class in Python?",
             ["A) class", "B) define", "C) object", "D) struct"],
             "A) class"),
    
    Question("What is an object?",
             ["A) Blueprint of a class", "B) Instance of a class", "C) A function", "D) A module"],
             "B) Instance of a class"),
    
    Question("What does __init__ method do?",
             ["A) Deletes object", "B) Initializes object", "C) Stops program", "D) Prints data"],
             "B) Initializes object"),
    
    Question("What is self in Python?",
             ["A) Global variable", "B) Reference to current object", "C) Keyword", "D) Data type"],
             "B) Reference to current object"),
    
    Question("Which concept allows using the same function name with different behavior?",
             ["A) Inheritance", "B) Polymorphism", "C) Encapsulation", "D) Abstraction"],
             "B) Polymorphism"),
    
    Question("Which OOP concept hides data from direct access?",
             ["A) Polymorphism", "B) Inheritance", "C) Encapsulation", "D) Overloading"],
             "C) Encapsulation"),
    
    Question("Which symbol is used to access class members?",
             ["A) :", "B) ->", "C) .", "D) ,"],
             "C) ."),
    
    Question("What is inheritance used for?",
             ["A) Code repetition", "B) Code reuse", "C) Data hiding", "D) Error handling"],
             "B) Code reuse"),
    
    Question("Which keyword is used to inherit a class?",
             ["A) inherit", "B) extends", "C) super", "D) class"],
             "D) class"),
    
    Question("What is abstraction?",
             ["A) Showing all details", "B) Hiding implementation details", "C) Copying objects", "D) Removing classes"],
             "B) Hiding implementation details"),
    
    Question("Which function returns all attributes of an object?",
             ["A) list()", "B) dir()", "C) type()", "D) id()"],
             "B) dir()"),
    
    Question("Can a class have multiple objects?",
             ["A) No", "B) Yes"],
             "B) Yes"),
    
    Question("What happens if a method name is same in parent and child class?",
             ["A) Error", "B) Method overriding", "C) Program stops", "D) No effect"],
             "B) Method overriding"),
    
    Question("Which OOP concept improves code security?",
             ["A) Inheritance", "B) Polymorphism", "C) Encapsulation", "D) Looping"],
             "C) Encapsulation"),
]


# ============== Streamlit App ==============

def initialize_session_state():
    """Initialize session state variables"""
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "quiz_object" not in st.session_state:
        st.session_state.quiz_object = Quiz(questions_data)
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = [None] * len(questions_data)
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "show_review" not in st.session_state:
        st.session_state.show_review = False


def display_results_summary():
    """Display summary of quiz results"""
    quiz = st.session_state.quiz_object
    score = quiz.calculate_score(st.session_state.user_answers)
    total = len(questions_data)
    percentage = (score / total) * 100
    incorrect = total - score
    
    st.success("🎉 Quiz Submitted!")
    
    # Display results metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", total)
    with col2:
        st.metric("Correct ✅", score)
    with col3:
        st.metric("Incorrect ❌", incorrect)
    with col4:
        st.metric("Score", f"{percentage:.1f}%")
    
    st.divider()
    
    # Performance message
    st.subheader("Performance Assessment:")
    if percentage >= 70:
        st.success(f"✅ **PASS!** Great job! You scored {score}/{total} ({percentage:.1f}%)")
    else:
        st.warning(f"⚠️ **TRY AGAIN!** You scored {score}/{total} ({percentage:.1f}%). Keep practicing!")


def display_detailed_review():
    """Display detailed review of all questions and answers"""
    quiz = st.session_state.quiz_object
    score = quiz.calculate_score(st.session_state.user_answers)
    total = len(questions_data)
    
    st.subheader("📋 Detailed Answer Review")
    
    # Generate review data
    review_data = quiz.get_review_data(st.session_state.user_answers)
    
    # Create DataFrame for better display
    df = pd.DataFrame(review_data)
    
    # Display as table
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Display individual questions with detailed feedback
    st.subheader("Question-by-Question Breakdown")
    
    for i, item in enumerate(review_data):
        question_num = item["Q#"]
        question_text = item["Question"]
        user_answer = item["Your Answer"]
        correct_answer = item["Correct Answer"]
        status = item["Status"]
        
        # Create expander for each question
        with st.expander(f"{status} Question {question_num}: {question_text}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Your Answer:**")
                if "✅" in status:
                    st.success(user_answer)
                else:
                    st.error(user_answer)
            with col2:
                st.write("**Correct Answer:**")
                st.success(correct_answer)


def main():
    """Main function to run the Streamlit app"""
    st.set_page_config(page_title="Quiz App", layout="wide")
    st.title("🎯 Quiz App - Python & OOP Concepts")
    
    # Initialize session state
    initialize_session_state()
    
    # Quiz not started
    if not st.session_state.quiz_started:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("Welcome to the **Python & OOP Quiz App**!")
            st.write("Test your knowledge with 25 carefully curated questions covering:")
            st.write("✨ Python Basics (Questions 1-10)")
            st.write("✨ Python OOP Concepts (Questions 11-25)")
            st.write(f"\n**Total Questions:** 25 | **Passing Score:** 70%")
            
            st.divider()
            
            if st.button("🚀 Start Quiz", use_container_width=True):
                st.session_state.quiz_started = True
                st.rerun()
    
    # Quiz is running
    elif st.session_state.quiz_started and not st.session_state.quiz_submitted:
        quiz = st.session_state.quiz_object
        current_idx = st.session_state.current_question
        current_q = quiz.get_question(current_idx)
        
        # Progress bar
        progress = (current_idx + 1) / len(questions_data)
        st.progress(progress)
        st.write(f"**Question {current_idx + 1} of {len(questions_data)}**")
        
        # Display question
        st.subheader(current_q.question_text)
        
        # Radio buttons for options
        selected_option = st.radio(
            "Select an option:",
            options=current_q.options,
            key=f"question_{current_idx}",
            label_visibility="collapsed"
        )
        
        # Store the selected answer
        st.session_state.user_answers[current_idx] = selected_option
        
        st.divider()
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        
        # Previous button
        if current_idx > 0:
            with col1:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        # Question indicator in middle
        with col2:
            st.write(f"")
        
        # Next button
        if current_idx < len(questions_data) - 1:
            with col3:
                if st.button("Next ➡️", use_container_width=True):
                    st.session_state.current_question += 1
                    st.rerun()
        
        # Submit button (on last question)
        if current_idx == len(questions_data) - 1:
            with col2:
                if st.button("✅ Submit Quiz", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    st.rerun()
    
    # Results screen
    elif st.session_state.quiz_submitted:
        # Summary section
        display_results_summary()
        
        # Detailed review section
        display_detailed_review()
        
        st.divider()
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Restart Quiz", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.quiz_submitted = False
                st.session_state.current_question = 0
                st.session_state.user_answers = [None] * len(questions_data)
                st.session_state.quiz_object = Quiz(questions_data)
                st.rerun()


if __name__ == "__main__":
    main()
