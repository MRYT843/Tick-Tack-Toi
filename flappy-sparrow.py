import streamlit as st
import base64
import os
import glob
import json
from datetime import datetime


# Page configuration with custom CSS
st.set_page_config(
    page_title="Flappy Sparrow",
    page_icon="🐦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for high-level GUI
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .game-container {
        background: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        margin: 20px 0;
    }
    .title-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .title-container h1 {
        color: white;
        font-size: 3rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }
    .title-container p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title with better styling
st.markdown("""
    <div class="title-container">
        <h1>🐦 Flappy Sparrow</h1>
        <p>Click to fly! Avoid the pipes!</p>
    </div>
""", unsafe_allow_html=True)

# Automatically find bird/player image file
image_path = None
image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']

# First, check for temp_bird.png specifically (common temporary name for player image)
if os.path.exists('temp_bird.png'):
    image_path = 'temp_bird.png'
else:
    # Try common names
    for ext in image_extensions:
        possible_names = ['bird', 'sparrow', 'player', 'character']
        for name in possible_names:
            if os.path.exists(f'{name}{ext}'):
                image_path = f'{name}{ext}'
                break
        if image_path:
            break

# If still not found, search for any image file (but exclude background)
if image_path is None:
    for ext in image_extensions:
        files = glob.glob(f'*{ext}')
        # Exclude only background images, but include temp_bird and other player images
        files = [f for f in files if 'download' not in f.lower() and 'background' not in f.lower() and f != 'download.jpg' and f != 'download.png']
        if files:
            # Prefer files with 'bird', 'player', 'character', 'sparrow' in name
            preferred = [f for f in files if any(name in f.lower() for name in ['bird', 'player', 'character', 'sparrow', 'temp'])]
            if preferred:
                image_path = preferred[0]
            else:
                image_path = files[0]
            break

# Automatically find background image
background_path = None
background_names = ['background', 'download', 'bg']
for ext in image_extensions:
    for name in background_names:
        if os.path.exists(f'{name}{ext}'):
            background_path = f'{name}{ext}'
            break
    if background_path:
        break

# If not found with specific names, look for download.jpg specifically
if background_path is None:
    if os.path.exists('download.jpg'):
        background_path = 'download.jpg'
    elif os.path.exists('download.png'):
        background_path = 'download.png'

# Automatically find sound file
sound_path = None
sound_extensions = ['.mp3', '.wav', '.ogg']
for ext in sound_extensions:
    if os.path.exists(f'sparrow_s_ouch{ext}'):
        sound_path = f'sparrow_s_ouch{ext}'
        break

# If not found, try any sound file
if sound_path is None:
    for ext in sound_extensions:
        files = glob.glob(f'*{ext}')
        if files:
            sound_path = files[0]
            break

# If files not found, allow uploads
if image_path is None:
    st.warning("⚠️ Player image not found. Please upload an image file or place it in the repository.")
    uploaded_image = st.file_uploader("Upload Player Image (bird/character)", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="player_image")
    if uploaded_image is not None:
        # Save uploaded image temporarily
        with open("temp_player_image.png", "wb") as f:
            f.write(uploaded_image.getbuffer())
        image_path = "temp_player_image.png"
    else:
        st.info("💡 For Streamlit Cloud: Add your image files (bird.png, sparrow.png, etc.) to your GitHub repository.")
        st.stop()

if sound_path is None:
    st.warning("⚠️ Sound file not found. Please upload a sound file or place it in the repository.")
    uploaded_sound = st.file_uploader("Upload Sound File", type=['mp3', 'wav', 'ogg'], key="sound_file")
    if uploaded_sound is not None:
        # Save uploaded sound temporarily
        sound_ext = uploaded_sound.name.split('.')[-1].lower()
        sound_filename = f"temp_sound.{sound_ext}"
        with open(sound_filename, "wb") as f:
            f.write(uploaded_sound.getbuffer())
        sound_path = sound_filename
    else:
        st.info("💡 For Streamlit Cloud: Add your sound file (sparrow_s_ouch.mp3) to your GitHub repository.")
        st.stop()

# Encode image and sound to base64
def encode_file(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        st.error(f"Error reading file {file_path}: {e}")
        st.stop()

image_base64 = encode_file(image_path)
sound_base64 = encode_file(sound_path)

# Handle background image (optional)
background_base64 = None
background_mime = 'image/jpeg'
if background_path:
    try:
        background_base64 = encode_file(background_path)
        bg_ext = os.path.splitext(background_path)[1].lower()
        background_mime = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }.get(bg_ext, 'image/jpeg')
    except Exception as e:
        st.warning(f"Could not load background image: {e}")
        background_base64 = None
else:
    # Allow background image upload if not found
    uploaded_bg = st.file_uploader("Upload Background Image (Optional)", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key="bg_image")
    if uploaded_bg is not None:
        bg_ext = uploaded_bg.name.split('.')[-1].lower()
        bg_filename = f"temp_bg.{bg_ext}"
        with open(bg_filename, "wb") as f:
            f.write(uploaded_bg.getbuffer())
        try:
            background_base64 = encode_file(bg_filename)
            background_mime = {
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }.get(bg_ext, 'image/jpeg')
        except Exception as e:
            st.warning(f"Could not load uploaded background image: {e}")
            background_base64 = None

# Get file extension for proper MIME type
image_ext = os.path.splitext(image_path)[1].lower()
image_mime = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.webp': 'image/webp'
}.get(image_ext, 'image/png')

sound_ext = os.path.splitext(sound_path)[1].lower()
sound_mime = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg'
}.get(sound_ext, 'audio/mpeg')

# Build background image loading code
if background_base64:
    background_load_code = f"backgroundImage.src = 'data:{background_mime};base64,{background_base64}';"
else:
    background_load_code = "// No background image - will use gradient fallback"

# Enhanced HTML/JavaScript game code with high-level GUI
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }}
        
        .game-wrapper {{
            background: white;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
        }}
        
        #gameCanvas {{
            border: 4px solid #667eea;
            background: #87CEEB;
            display: block;
            margin: 0 auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border-radius: 10px;
        }}
        
        #score {{
            position: absolute;
            top: 30px;
            left: 50%;
            transform: translateX(-50%);
            color: #667eea;
            font-size: 32px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
            background: rgba(255,255,255,0.9);
            padding: 10px 20px;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 10;
        }}
        
        #gameOver {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            display: none;
            z-index: 100;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            animation: fadeIn 0.3s ease-in;
            min-width: 350px;
        }}
        
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.8);
            }}
            to {{
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }}
        }}
        
        #gameOver h2 {{
            font-size: 36px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        #gameOver p {{
            font-size: 24px;
            margin-bottom: 25px;
        }}
        
        #finalScore {{
            font-size: 48px;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        #restartBtn {{
            padding: 15px 40px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            margin-top: 10px;
        }}
        
        #restartBtn:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            background: #f0f0f0;
        }}
        
        #restartBtn:active {{
            transform: scale(0.95);
        }}
        
        #startScreen {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(102, 126, 234, 0.95);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            z-index: 50;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        #startScreen h3 {{
            font-size: 28px;
            margin-bottom: 15px;
        }}
        
        #startScreen p {{
            font-size: 18px;
            margin: 10px 0;
        }}
        
        .cloud {{
            position: absolute;
            background: rgba(255,255,255,0.8);
            border-radius: 50px;
            opacity: 0.7;
        }}
        
        .cloud:before,
        .cloud:after {{
            content: '';
            position: absolute;
            background: rgba(255,255,255,0.8);
            border-radius: 50px;
        }}
    </style>
</head>
<body>
    <div class="game-wrapper">
        <canvas id="gameCanvas" width="450" height="650"></canvas>
        <div id="score">Score: 0</div>
        <div id="startScreen">
            <h3>🎮 Flappy Sparrow</h3>
            <p>Click or Press Space to Fly!</p>
            <p style="font-size: 14px; margin-top: 15px; opacity: 0.9;">Avoid the pipes and ground</p>
        </div>
        <div id="gameOver">
            <h2>💥 Game Over!</h2>
            <p>Your Score:</p>
            <div id="finalScore">0</div>
            <button id="restartBtn" onclick="restartGame()" style="margin-top: 20px;">🔄 Play Again</button>
        </div>
    </div>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const gameOverElement = document.getElementById('gameOver');
        const finalScoreElement = document.getElementById('finalScore');
        const startScreen = document.getElementById('startScreen');
        
        // Game variables
        let bird = {{
            x: 80,
            y: canvas.height / 2,
            width: 50,
            height: 50,
            velocity: 0,
            gravity: 0.6,
            jumpStrength: -9,
            rotation: 0
        }};
        
        let pipes = [];
        let score = 0;
        let gameRunning = false;
        let gameStarted = false;
        let highScore = localStorage.getItem('highScore') || 0;
        
        // Load bird image
        const birdImage = new Image();
        birdImage.src = 'data:{image_mime};base64,{image_base64}';
        
        // Load background image
        const backgroundImage = new Image();
        {background_load_code}
        
        // Load sound
        const jumpSound = new Audio('data:{sound_mime};base64,{sound_base64}');
        jumpSound.volume = 0.6;
        let soundPlaying = false;
        
        // Enhanced Pipe class
        class Pipe {{
            constructor() {{
                this.x = canvas.width;
                this.width = 70;
                this.gap = 220;
                this.topHeight = Math.random() * (canvas.height - this.gap - 250) + 80;
                this.bottomY = this.topHeight + this.gap;
                this.speed = 3.5;
                this.passed = false;
            }}
            
            update() {{
                this.x -= this.speed;
            }}
            
            draw() {{
                // Top pipe with gradient
                const gradientTop = ctx.createLinearGradient(this.x, 0, this.x + this.width, 0);
                gradientTop.addColorStop(0, '#2E7D32');
                gradientTop.addColorStop(1, '#4CAF50');
                ctx.fillStyle = gradientTop;
                ctx.fillRect(this.x, 0, this.width, this.topHeight);
                
                // Top pipe cap
                ctx.fillStyle = '#1B5E20';
                ctx.fillRect(this.x - 8, this.topHeight - 40, this.width + 16, 40);
                ctx.fillRect(this.x - 5, this.topHeight - 35, this.width + 10, 10);
                
                // Bottom pipe with gradient
                const gradientBottom = ctx.createLinearGradient(this.x, this.bottomY, this.x + this.width, this.bottomY);
                gradientBottom.addColorStop(0, '#2E7D32');
                gradientBottom.addColorStop(1, '#4CAF50');
                ctx.fillStyle = gradientBottom;
                ctx.fillRect(this.x, this.bottomY, this.width, canvas.height - this.bottomY);
                
                // Bottom pipe cap
                ctx.fillStyle = '#1B5E20';
                ctx.fillRect(this.x - 8, this.bottomY, this.width + 16, 40);
                ctx.fillRect(this.x - 5, this.bottomY + 5, this.width + 10, 10);
            }}
            
            collides(bird) {{
                return bird.x < this.x + this.width &&
                       bird.x + bird.width > this.x &&
                       (bird.y < this.topHeight || bird.y + bird.height > this.bottomY);
            }}
        }}
        
        // Jump function
        function jump() {{
            if (!gameStarted) {{
                gameStarted = true;
                gameRunning = true;
                startScreen.style.display = 'none';
            }}
            if (gameRunning) {{
                bird.velocity = bird.jumpStrength;
                // Stop any currently playing sound
                jumpSound.pause();
                jumpSound.currentTime = 0;
                jumpSound.play().catch(e => console.log("Sound play failed:", e));
                soundPlaying = true;
            }}
        }}
        
        // Event listeners
        canvas.addEventListener('click', jump);
        document.addEventListener('keydown', (e) => {{
            if (e.code === 'Space' || e.key === ' ') {{
                e.preventDefault();
                jump();
            }}
        }});
        
        // Update game
        function update() {{
            if (!gameRunning) return;
            
            // Update bird with rotation
            bird.velocity += bird.gravity;
            bird.y += bird.velocity;
            bird.rotation = Math.min(Math.max(bird.velocity * 3, -30), 90);
            
            // Check boundaries
            if (bird.y + bird.height > canvas.height - 20 || bird.y < 0) {{
                gameOver();
            }}
            
            // Update pipes
            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 280) {{
                pipes.push(new Pipe());
            }}
            
            for (let i = pipes.length - 1; i >= 0; i--) {{
                pipes[i].update();
                
                // Check collision
                if (pipes[i].collides(bird)) {{
                    gameOver();
                }}
                
                // Update score
                if (!pipes[i].passed && pipes[i].x + pipes[i].width < bird.x) {{
                    pipes[i].passed = true;
                    score++;
                    scoreElement.textContent = 'Score: ' + score;
                    if (score > highScore) {{
                        highScore = score;
                        localStorage.setItem('highScore', highScore);
                    }}
                }}
                
                // Remove off-screen pipes
                if (pipes[i].x + pipes[i].width < 0) {{
                    pipes.splice(i, 1);
                }}
            }}
        }}
        
        // Draw game with enhanced graphics
        function draw() {{
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw background image if loaded
            if (backgroundImage.complete && backgroundImage.width > 0) {{
                // Draw background image, scaled to fit canvas
                ctx.drawImage(backgroundImage, 0, 0, canvas.width, canvas.height);
            }} else {{
                // Fallback: draw gradient background
                const bgGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
                bgGradient.addColorStop(0, '#87CEEB');
                bgGradient.addColorStop(0.5, '#98D8C8');
                bgGradient.addColorStop(1, '#90EE90');
                ctx.fillStyle = bgGradient;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw clouds (background decoration) only if no background image
                drawClouds();
            }}
            
            // Draw pipes
            pipes.forEach(pipe => pipe.draw());
            
            // Draw bird with rotation
            ctx.save();
            ctx.translate(bird.x + bird.width / 2, bird.y + bird.height / 2);
            ctx.rotate(bird.rotation * Math.PI / 180);
            if (birdImage.complete) {{
                ctx.drawImage(birdImage, -bird.width / 2, -bird.height / 2, bird.width, bird.height);
            }} else {{
                // Fallback rectangle if image not loaded
                ctx.fillStyle = '#FFD700';
                ctx.fillRect(-bird.width / 2, -bird.height / 2, bird.width, bird.height);
            }}
            ctx.restore();
            
            // Draw ground with texture
            const groundGradient = ctx.createLinearGradient(0, canvas.height - 20, 0, canvas.height);
            groundGradient.addColorStop(0, '#8B4513');
            groundGradient.addColorStop(1, '#654321');
            ctx.fillStyle = groundGradient;
            ctx.fillRect(0, canvas.height - 20, canvas.width, 20);
            
            // Grass on ground
            ctx.fillStyle = '#7CB342';
            ctx.fillRect(0, canvas.height - 20, canvas.width, 8);
            
            // Draw grass details
            ctx.fillStyle = '#558B2F';
            for (let i = 0; i < canvas.width; i += 15) {{
                ctx.fillRect(i, canvas.height - 20, 3, 12);
            }}
        }}
        
        // Draw decorative clouds
        function drawClouds() {{
            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            // Cloud 1
            drawCloud(100, 100, 60);
            // Cloud 2
            drawCloud(300, 150, 50);
            // Cloud 3
            drawCloud(200, 80, 45);
        }}
        
        function drawCloud(x, y, size) {{
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.arc(x + size * 0.6, y, size * 0.8, 0, Math.PI * 2);
            ctx.arc(x + size * 1.2, y, size * 0.7, 0, Math.PI * 2);
            ctx.arc(x + size * 0.6, y - size * 0.5, size * 0.6, 0, Math.PI * 2);
            ctx.fill();
        }}
        
        // Game over - STOP SOUND
        function gameOver() {{
            gameRunning = false;
            // Stop the sound immediately when player dies
            jumpSound.pause();
            jumpSound.currentTime = 0;
            soundPlaying = false;
            
            finalScoreElement.textContent = score;
            gameOverElement.style.display = 'block';
            
            // Show high score
            if (score === highScore && score > 0) {{
                finalScoreElement.textContent = score + ' 🏆';
            }}
        }}
        
        // Restart game
        function restartGame() {{
            bird.y = canvas.height / 2;
            bird.velocity = 0;
            bird.rotation = 0;
            pipes = [];
            score = 0;
            gameRunning = false;
            gameStarted = false;
            scoreElement.textContent = 'Score: 0';
            gameOverElement.style.display = 'none';
            startScreen.style.display = 'block';
            // Ensure sound is stopped
            jumpSound.pause();
            jumpSound.currentTime = 0;
            soundPlaying = false;
        }}
        
        // Game loop
        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        
        // Start game loop
        gameLoop();
    </script>
</body>
</html>
"""

# Display the game in a styled container
st.markdown('<div class="game-container">', unsafe_allow_html=True)

# Create the HTML component
game_component = st.components.v1.html(
    game_html, 
    height=750, 
    scrolling=False
)

st.markdown('</div>', unsafe_allow_html=True)
