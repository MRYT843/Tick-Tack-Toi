import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Tic-Tac-Toe 🎮", page_icon="🎮", layout="centered")

# ---------------------
# Session State Setup
# ---------------------
if "started" not in st.session_state:
    st.session_state.started = False
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
if "player" not in st.session_state:
    st.session_state.player = "X"
if "winner" not in st.session_state:
    st.session_state.winner = None
if "win_combo" not in st.session_state:
    st.session_state.win_combo = []

# ---------------------
# Functions
# ---------------------
def check_winner(board):
    combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for c in combos:
        if board[c[0]] == board[c[1]] == board[c[2]] != "":
            st.session_state.win_combo = c
            return board[c[0]]
    if "" not in board:
        return "Draw"
    return None

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.player = "X"
    st.session_state.winner = None
    st.session_state.win_combo = []
    st.session_state.started = False

def draw_board():
    size = 300
    cell_size = size // 3
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    
    # Draw grid
    for i in range(1,3):
        draw.line((0, i*cell_size, size, i*cell_size), fill="black", width=4)
        draw.line((i*cell_size, 0, i*cell_size, size), fill="black", width=4)
    
    # Draw X and O
    font = ImageFont.load_default()
    for i, mark in enumerate(st.session_state.board):
        x = (i % 3) * cell_size + cell_size//2
        y = (i // 3) * cell_size + cell_size//2
        if mark == "X":
            draw.text((x-10, y-10), "X", fill="red", font=font)
        elif mark == "O":
            draw.text((x-10, y-10), "O", fill="blue", font=font)
    
    # Draw win line
    if st.session_state.win_combo:
        c = st.session_state.win_combo
        x1 = (c[0]%3)*cell_size + cell_size//2
        y1 = (c[0]//3)*cell_size + cell_size//2
        x2 = (c[2]%3)*cell_size + cell_size//2
        y2 = (c[2]//3)*cell_size + cell_size//2
        draw.line((x1, y1, x2, y2), fill="green", width=6)
    
    return img

# ---------------------
# Welcome Screen + Start
# ---------------------
if not st.session_state.started:
    st.markdown("<h1 style='text-align:center; color:darkblue;'>🎮 Welcome to Tic-Tac-Toe 🎮</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Click Start to begin 2-Player game!</p>", unsafe_allow_html=True)
    if st.button("Start Game 🕹️"):
        st.session_state.started = True
    st.stop()

# ---------------------
# Game Board Interaction
# ---------------------
cols = st.columns(3)
for i in range(9):
    if cols[i%3].button(st.session_state.board[i] if st.session_state.board[i] != "" else " ", key=i):
        if st.session_state.board[i] == "" and st.session_state.winner is None:
            st.session_state.board[i] = st.session_state.player
            st.session_state.winner = check_winner(st.session_state.board)
            st.session_state.player = "O" if st.session_state.player == "X" else "X"

# ---------------------
# Display Board
# ---------------------
st.image(draw_board(), use_column_width=True)

# ---------------------
# Winner Display & Celebration
# ---------------------
if st.session_state.winner:
    if st.session_state.winner == "Draw":
        st.markdown("<h2 style='text-align:center;'>It's a Draw! 🤝</h2>", unsafe_allow_html=True)
    else:
        winner_name = "Player X" if st.session_state.winner == "X" else "Player O"
        st.markdown(f"<h2 style='text-align:center; color:blue;'>🏆 {winner_name} Wins! 🏆</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:50px;'>🎉🎊🥳🎉🎊🥳</p>", unsafe_allow_html=True)

# ---------------------
# Reset Button
# ---------------------
st.button("Play Again 🔄", on_click=reset_game)
