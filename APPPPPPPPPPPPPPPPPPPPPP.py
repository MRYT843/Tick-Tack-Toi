import streamlit as st
import base64
import os

# Set page configuration
st.set_page_config(
    page_title="Flappy Bird Streamlit",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Flappy Bird with Streamlit")

# Hide Streamlit Main Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write("Click or Press Space to Fly!")

# Function to encode files to base64
def get_base64_encoded_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load Assets
bird_b64 = get_base64_encoded_file("assets/3434.jpg")
bg_b64 = get_base64_encoded_file("assets/bg.jpg")
sound_b64 = get_base64_encoded_file("assets/fly_sound.mp3")

if not bird_b64 or not bg_b64 or not sound_b64:
    st.error("Assets missing! Please ensure 'assets/3434.jpg', 'assets/bg.jpg', and 'assets/fly_sound.mp3' exist.")
    st.stop()

# HTML/JS Game Code
game_html = f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Teko:wght@700&display=swap" rel="stylesheet">
<style>
    body {{
        margin: 0;
        padding: 0;
        display: flex;
        justify_content: center;
        align-items: center;
        height: 100vh;
        width: 100%; /* Ensure full width for centering */
        background-color: transparent; /* Fix white screen in dark mode */
        font-family: 'Teko', sans-serif;
    }}
    
    #game-container {{
        position: relative;
        width: 320px;
        height: 480px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5), 0 6px 6px rgba(0,0,0,0.5); /* Stronger shadow for dark mode */
        border-radius: 10px;
        overflow: hidden;
        border: 4px solid #333;
    }}

    canvas {{
        display: block;
        background-color: #70c5ce;
        width: 100%;
        height: 100%;
    }}
</style>
</head>
<body>

<div id="game-container">
    <canvas id="gameCanvas" width="320" height="480"></canvas>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // Game Variables
    let frames = 0;
    const DEGREE = Math.PI / 180;

    // Load Images
    const sprite = new Image();
    sprite.src = "data:image/jpeg;base64,{bird_b64}";
    
    const bg = new Image();
    bg.src = "data:image/jpeg;base64,{bg_b64}";

    // Load Sound
    const FLY_SOUND = new Audio("data:audio/mpeg;base64,{sound_b64}");

    // Game State
    const state = {{
        current: 0,
        getReady: 0,
        game: 1,
        over: 2
    }}

    // Controls
    function clickHandler() {{
        switch(state.current) {{
            case state.getReady:
                state.current = state.game;
                FLY_SOUND.play().catch(e => console.log("Audio play failed: ", e));
                break;
            case state.game:
                bird.flap();
                FLY_SOUND.currentTime = 0;
                FLY_SOUND.play().catch(e => console.log("Audio play failed: ", e));
                break;
            case state.over:
                pipes.reset();
                bird.speedReset();
                score.reset();
                state.current = state.getReady;
                frames = 0;
                break;
        }}
    }}
    
    document.addEventListener("click", clickHandler);
    document.addEventListener("keydown", function(e) {{
        if(e.code === "Space") {{
            e.preventDefault(); // Stop scrolling
            clickHandler();
        }}
    }});

    // Background
    const background = {{
        x: 0,
        y: 0,
        w: 320,
        h: 480,
        dx: 2,
        
        draw: function() {{
            ctx.drawImage(bg, this.x, this.y, this.w, this.h);
            ctx.drawImage(bg, this.x + this.w, this.y, this.w, this.h);
        }},
        
        update: function() {{
            if(state.current == state.game) {{
                this.x = (this.x - this.dx) % (this.w);
            }}
        }}
    }}

    // Bird
    const bird = {{
        animation: [0, 1, 2, 1],
        x: 50,
        y: 150,
        w: 34,
        h: 24,
        radius: 12,
        frame: 0,
        gravity: 0.25,
        jump: 4.6,
        speed: 0,
        rotation: 0,
        
        draw: function() {{
            let birdImg = sprite;
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation);
            ctx.drawImage(birdImg, -this.w/2, -this.h/2, this.w, this.h); 
            ctx.restore();
        }},
        
        flap: function() {{
            this.speed = -this.jump;
        }},
        
        update: function() {{
            this.period = state.current == state.getReady ? 10 : 5;
            this.frame += frames % this.period == 0 ? 1 : 0;
            this.frame = this.frame % this.animation.length;
            
            if(state.current == state.getReady) {{
                this.y = 150;
                this.rotation = 0 * DEGREE;
            }} else {{
                this.speed += this.gravity;
                this.y += this.speed;
                
                if(this.y + this.h/2 >= canvas.height) {{
                    this.y = canvas.height - this.h/2;
                    if(state.current == state.game) {{
                        state.current = state.over;
                        FLY_SOUND.pause();
                        FLY_SOUND.currentTime = 0;
                    }}
                }}
                
                if(this.speed < this.jump) {{
                    this.rotation = -25 * DEGREE;
                }} else {{
                    this.rotation = 90 * DEGREE;
                }}
            }}
        }},
        
        speedReset: function() {{
            this.speed = 0;
        }}
    }}

    // Pipes
    const pipes = {{
        position: [],
        w: 52,
        h: 400,
        dx: 2,
        maxYPos: -150,
        gap: 120, // increased gap
        
        draw: function() {{
            for(let i = 0; i < this.position.length; i++) {{
                let p = this.position[i];
                let topY = p.y;
                let bottomY = p.y + this.h + this.gap;
                
                // Top Pipe
                // Body
                let gradTop = ctx.createLinearGradient(p.x, topY, p.x + this.w, topY);
                gradTop.addColorStop(0, '#558c42');
                gradTop.addColorStop(0.5, '#92d56e');
                gradTop.addColorStop(1, '#558c42');
                ctx.fillStyle = gradTop;
                ctx.fillRect(p.x, topY, this.w, this.h);
                // Cap
                ctx.fillRect(p.x - 2, topY + this.h - 20, this.w + 4, 20);
                
                // Border
                ctx.strokeStyle = "#325c22";
                ctx.lineWidth = 2;
                ctx.strokeRect(p.x, topY, this.w, this.h); // body
                ctx.strokeRect(p.x - 2, topY + this.h - 20, this.w + 4, 20); // cap


                // Bottom Pipe
                // Body
                let gradBot = ctx.createLinearGradient(p.x, bottomY, p.x + this.w, bottomY);
                gradBot.addColorStop(0, '#558c42');
                gradBot.addColorStop(0.5, '#92d56e');
                gradBot.addColorStop(1, '#558c42');
                ctx.fillStyle = gradBot;
                ctx.fillRect(p.x, bottomY, this.w, this.h);
                // Cap
                ctx.fillRect(p.x - 2, bottomY, this.w + 4, 20);

                // Border
                ctx.strokeRect(p.x, bottomY, this.w, this.h); // body
                ctx.strokeRect(p.x - 2, bottomY, this.w + 4, 20); // cap
            }}
        }},
        
        update: function() {{
            if(state.current !== state.game) return;
            
            if(frames % 120 == 0) {{ // Slower generation
                this.position.push({{
                    x: canvas.width,
                    y: this.maxYPos * (Math.random() + 1)
                }});
            }}
            
            for(let i = 0; i < this.position.length; i++) {{
                let p = this.position[i];
                let bottomPipeY = p.y + this.h + this.gap;
                
                // Collision
                // Top Pipe
                if(bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                   bird.y - bird.radius < p.y + this.h && bird.y + bird.radius > p.y) {{
                    state.current = state.over;
                    FLY_SOUND.pause();
                    FLY_SOUND.currentTime = 0;
                }}
                // Bottom Pipe
                if(bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.w &&
                   bird.y + bird.radius > bottomPipeY && bird.y - bird.radius < bottomPipeY + this.h) {{
                    state.current = state.over;
                    FLY_SOUND.pause();
                    FLY_SOUND.currentTime = 0;
                }}
                
                p.x -= this.dx;
                
                if(p.x + this.w <= 0) {{
                    this.position.shift();
                    score.value += 1;
                    score.best = Math.max(score.value, score.best);
                    localStorage.setItem("best", score.best);
                }}
            }}
        }},
        
        reset: function() {{
            this.position = [];
        }}
    }}

    // Score
    const score = {{
        best: localStorage.getItem("best") || 0,
        value: 0,
        
        draw: function() {{
            ctx.fillStyle = "#FFF";
            ctx.strokeStyle = "#000";
            ctx.textAlign = "center"; // CENTER TEXT ALIGNMENT
            
            if(state.current == state.game) {{
                ctx.lineWidth = 2;
                ctx.font = "35px Teko";
                ctx.fillText(this.value, canvas.width/2, 50);
                ctx.strokeText(this.value, canvas.width/2, 50);
            }} else if(state.current == state.over) {{
                ctx.font = "25px Teko";
                
                // Dark Overlay for Game Over
                ctx.fillStyle = "rgba(0, 0, 0, 0.5)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Score Box Background
                ctx.fillStyle = "#e0c996";
                ctx.fillRect(canvas.width/2 - 60, 160, 120, 80);
                // Box border
                ctx.strokeStyle = "#543847";
                ctx.lineWidth = 2;
                ctx.strokeRect(canvas.width/2 - 60, 160, 120, 80);
                
                ctx.fillStyle = "#FFF"; // Reset text color
                ctx.strokeStyle = "#000";
                
                // Score Text (Centered)
                ctx.fillText("Score: " + this.value, canvas.width/2, 190);
                ctx.strokeText("Score: " + this.value, canvas.width/2, 190);
                
                ctx.fillText("Best: " + this.best, canvas.width/2, 220);
                ctx.strokeText("Best: " + this.best, canvas.width/2, 220);

                ctx.font = "50px Teko";
                ctx.lineWidth = 3;
                ctx.fillText("Game Over", canvas.width/2, 120);
                ctx.strokeText("Game Over", canvas.width/2, 120);
                
                ctx.lineWidth = 2;
                ctx.font = "20px Teko";
                ctx.fillText("Click to Restart", canvas.width/2, 300);
            }} else if(state.current == state.getReady) {{
                 ctx.font = "40px Teko";
                 ctx.lineWidth = 3;
                 ctx.fillText("Get Ready!", canvas.width/2, 200);
                 ctx.strokeText("Get Ready!", canvas.width/2, 200);
                 
                 ctx.lineWidth = 2;
                 ctx.font = "20px Teko";
                 ctx.fillText("Click to Fly", canvas.width/2, 240);
            }}
        }},
        
        reset: function() {{
            this.value = 0;
        }}
    }}

    function draw() {{
        ctx.fillStyle = "#70c5ce";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        background.draw();
        pipes.draw();
        bird.draw();
        score.draw();
    }}

    function update() {{
        background.update();
        bird.update();
        pipes.update();
    }}

    function loop() {{
        update();
        draw();
        frames++;
        requestAnimationFrame(loop);
    }}
    
    loop();

</script>
</body>
</html>
"""

# Render with Streamlit Components
import streamlit.components.v1 as components
components.html(game_html, height=550, scrolling=False)
