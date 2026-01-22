import streamlit as st

# ------------------ Page Config ------------------
st.set_page_config(page_title="Rock Paper Scissors", page_icon="✊", layout="centered")

# ------------------ Session State Init ------------------
if "started" not in st.session_state:
    st.session_state.started = False

if "p1_choice" not in st.session_state:
    st.session_state.p1_choice = None

if "p2_choice" not in st.session_state:
    st.session_state.p2_choice = None

if "scores" not in st.session_state:
    st.session_state.scores = {"p1": 0, "p2": 0, "draw": 0}

# ------------------ Helper Functions ------------------
def decide_winner(p1, p2):
    if p1 == p2:
        return "draw"
    rules = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }
    if rules[p1] == p2:
        return "p1"
    return "p2"


def reset_round():
    st.session_state.p1_choice = None
    st.session_state.p2_choice = None


def reset_all():
    st.session_state.started = False
    st.session_state.p1_choice = None
    st.session_state.p2_choice = None
    st.session_state.scores = {"p1": 0, "p2": 0, "draw": 0}

# ------------------ UI ------------------
st.title("✊ Rock Paper Scissors")
st.caption("A simple 2-player game built with Streamlit")

# ------------------ Welcome Screen ------------------
if not st.session_state.started:
    st.info("Click **Start Game** to begin 🎮")
    if st.button("🚀 Start Game"):
        st.session_state.started = True
    st.stop()

# ------------------ Game Interface ------------------
st.subheader("Game Arena")

col1, col2 = st.columns(2)

# Player 1
with col1:
    st.markdown("### Player 1")
    if st.session_state.p1_choice is None:
        if st.button("✊ Rock", key="p1_rock"):
            st.session_state.p1_choice = "Rock"
        if st.button("📄 Paper", key="p1_paper"):
            st.session_state.p1_choice = "Paper"
        if st.button("✂️ Scissors", key="p1_scissors"):
            st.session_state.p1_choice = "Scissors"
    else:
        st.success(f"Choice locked: **{st.session_state.p1_choice}**")

# Player 2
with col2:
    st.markdown("### Player 2")
    if st.session_state.p1_choice is None:
        st.warning("Waiting for Player 1…")
    else:
        if st.session_state.p2_choice is None:
            if st.button("✊ Rock", key="p2_rock"):
                st.session_state.p2_choice = "Rock"
            if st.button("📄 Paper", key="p2_paper"):
                st.session_state.p2_choice = "Paper"
            if st.button("✂️ Scissors", key="p2_scissors"):
                st.session_state.p2_choice = "Scissors"
        else:
            st.success(f"Choice locked: **{st.session_state.p2_choice}**")

# ------------------ Result Section ------------------
if st.session_state.p1_choice and st.session_state.p2_choice:
    st.divider()
    st.subheader("Result")

    # ensure score updates only once per round
    if "round_done" not in st.session_state:
        st.session_state.round_done = False

    winner = decide_winner(st.session_state.p1_choice, st.session_state.p2_choice)

    st.write(f"**Player 1:** {st.session_state.p1_choice}")
    st.write(f"**Player 2:** {st.session_state.p2_choice}")

    if not st.session_state.round_done:
        if winner == "draw":
            st.info("🤝 It's a Draw!")
            st.session_state.scores["draw"] += 1
        elif winner == "p1":
            st.success("🎉 Player 1 Wins!")
            st.session_state.scores["p1"] += 1
        else:
            st.success("🎉 Player 2 Wins!")
            st.session_state.scores["p2"] += 1
        st.session_state.round_done = True
    else:
        if winner == "draw":
            st.info("🤝 It's a Draw!")
        elif winner == "p1":
            st.success("🎉 Player 1 Wins!")
        else:
            st.success("🎉 Player 2 Wins!")

    if st.button("🔁 Play Next Round"):
        st.session_state.p1_choice = None
        st.session_state.p2_choice = None
        st.session_state.round_done = False

# ------------------ Scoreboard ------------------
st.divider()
st.subheader("Scoreboard")

s1, s2, s3 = st.columns(3)
with s1:
    st.metric("Player 1 Wins", st.session_state.scores["p1"])
with s2:
    st.metric("Player 2 Wins", st.session_state.scores["p2"])
with s3:
    st.metric("Draws", st.session_state.scores["draw"])

# ------------------ Reset ------------------
st.divider()
if st.button("🧹 Reset Game & Scores"):
    reset_all()
    st.rerun()
