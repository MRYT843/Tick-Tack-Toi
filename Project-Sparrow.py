import streamlit as st
import json
import base64
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Flappy Sparrow",
    page_icon="🐦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 25px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    h1 {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5em;
    }
    .game-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Load and encode the MP3 sound file
def load_sound_file(file_path):
    """Load MP3 file and convert to base64 data URI"""
    try:
        with open(file_path, 'rb') as f:
            audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            return f"data:audio/mp3;base64,{audio_base64}"
    except FileNotFoundError:
        st.error(f"Sound file not found: {file_path}")
        return None
    except Exception as e:
        st.error(f"Error loading sound file: {e}")
        return None

# Load and encode the bird image file
def load_image_file(file_path):
    """Load image file and convert to base64 data URI"""
    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()
            # Determine file type from extension
            if file_path.lower().endswith('.png'):
                mime_type = 'image/png'
            elif file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                mime_type = 'image/jpeg'
            else:
                mime_type = 'image/png'  # default
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            return f"data:{mime_type};base64,{image_base64}"
    except FileNotFoundError:
        st.warning(f"Image file not found: {file_path}")
        return None
    except Exception as e:
        st.warning(f"Error loading image file: {e}")
        return None

# Load the sound file
SOUND_FILE_PATH = r"c:\Users\l4-pc6\Downloads\sparrow_s_ouch.mp3"
audio_data_uri = load_sound_file(SOUND_FILE_PATH)

# If sound file not found, use empty string (fallback to no sound)
if audio_data_uri is None:
    audio_data_uri = ""

# Load the bird image file
BIRD_IMAGE_PATH = r"C:\Users\l4-pc6\.cursor\projects\c-Users-l4-pc6-Desktop-frontEND\assets\c__Users_l4-pc6_AppData_Roaming_Cursor_User_workspaceStorage_106f870de8ddd84d8df24245f29c36f8_images_download-a612f97e-3f32-43aa-89a5-0863474e973d.png"
bird_image_data_uri = load_image_file(BIRD_IMAGE_PATH)

# If image file not found, use empty string (fallback to drawn bird)
if bird_image_data_uri is None:
    bird_image_data_uri = ""

# High-level game HTML with advanced features
GAME_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Flappy Sparrow</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden;
        }
        #gameContainer {
            position: relative;
            width: 500px;
            height: 700px;
            margin: 20px auto;
        }
        #gameCanvas {
            border: 4px solid #fff;
            border-radius: 15px;
            background: linear-gradient(to bottom, #87CEEB 0%, #98D8E8 40%, #B8E6B8 100%);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            display: block;
        }
        #ui {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10;
        }
        #score {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 36px;
            font-weight: bold;
            color: white;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.7);
            z-index: 11;
        }
        #highScore {
            position: absolute;
            top: 70px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 18px;
            font-weight: bold;
            color: #FFD700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            z-index: 11;
        }
        #instructions {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            z-index: 11;
            text-align: center;
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas" width="500" height="700"></canvas>
        <div id="ui">
            <div id="score">0</div>
            <div id="highScore">Best: 0</div>
            <div id="instructions">Click or Press Space to Fly</div>
        </div>
    </div>
    
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const highScoreElement = document.getElementById('highScore');
        const instructionsElement = document.getElementById('instructions');
        
        // Load high score from localStorage
        let highScore = parseInt(localStorage.getItem('flappySparrowHighScore')) || 0;
        highScoreElement.textContent = 'Best: ' + highScore;
        
        // Game state
        let gameState = 'menu'; // menu, playing, paused, gameOver
        let frameCount = 0;
        let particles = [];
        let stars = [];
        
        // Initialize stars for background
        for (let i = 0; i < 50; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 2 + 1,
                speed: Math.random() * 0.5 + 0.2,
                opacity: Math.random()
            });
        }
        
        // Bird object with advanced properties
        let bird = {
            x: 150,
            y: 350,
            width: 60,
            height: 80,
            velocity: 0,
            gravity: 0.6,
            jumpPower: -10,
            rotation: 0,
            wingFlap: 0,
            trail: []
        };
        
        // Load bird image
        const birdImage = new Image();
        birdImage.src = '{BIRD_IMAGE_DATA_URI}';
        let birdImageLoaded = false;
        birdImage.onload = function() {
            birdImageLoaded = true;
            // Adjust bird size based on image dimensions if needed
            if (birdImage.width > 0 && birdImage.height > 0) {
                const aspectRatio = birdImage.width / birdImage.height;
                bird.width = 60;
                bird.height = 60 / aspectRatio;
            }
        };
        birdImage.onerror = function() {
            birdImageLoaded = false;
            console.log('Bird image failed to load, using drawn sprite');
        };
        
        // Pipes array
        let pipes = [];
        let pipeGap = 180;
        let pipeWidth = 80;
        let pipeSpeed = 4;
        let score = 0;
        let nextPipeDistance = 0;
        
        // Parallax layers
        let clouds = [];
        for (let i = 0; i < 5; i++) {
            clouds.push({
                x: Math.random() * canvas.width,
                y: Math.random() * 200 + 50,
                width: 80 + Math.random() * 40,
                height: 40 + Math.random() * 20,
                speed: 0.3 + Math.random() * 0.3
            });
        }
        
        // Load the "Ouch Ouch" sound file
        const ouchSound = new Audio();
        ouchSound.src = '{AUDIO_DATA_URI}';
        ouchSound.preload = 'auto';
        ouchSound.volume = 0.7;
        
        // Function to play "Ouch Ouch" sound
        function playOuchSound() {
            try {
                // Clone and play the audio to allow overlapping sounds
                const soundClone = ouchSound.cloneNode();
                soundClone.volume = 0.7;
                soundClone.play().catch(e => {
                    // Handle autoplay restrictions
                    console.log('Audio play failed:', e);
                });
            } catch (e) {
                console.log('Audio not available:', e);
            }
        }
        
        // Create particle effect
        function createParticles(x, y, color) {
            for (let i = 0; i < 8; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 8,
                    vy: (Math.random() - 0.5) * 8,
                    life: 30,
                    maxLife: 30,
                    size: Math.random() * 4 + 2,
                    color: color
                });
            }
        }
        
        // Draw advanced sparrow with animations
        function drawSparrow() {
            ctx.save();
            const centerX = bird.x + bird.width / 2;
            const centerY = bird.y + bird.height / 2;
            
            // Add to trail
            bird.trail.push({x: centerX, y: centerY});
            if (bird.trail.length > 8) bird.trail.shift();
            
            // Draw trail
            bird.trail.forEach((point, index) => {
                const alpha = index / bird.trail.length * 0.2;
                ctx.fillStyle = `rgba(100, 100, 100, ${alpha})`;
                ctx.beginPath();
                ctx.arc(point.x, point.y, 20, 0, Math.PI * 2);
                ctx.fill();
            });
            
            ctx.translate(centerX, centerY);
            
            // Rotation based on velocity (subtle rotation)
            bird.rotation = Math.max(-Math.PI / 8, Math.min(Math.PI / 8, bird.velocity * 0.05));
            ctx.rotate(bird.rotation);
            
            // Draw shadow
            ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
            ctx.beginPath();
            ctx.ellipse(3, bird.height/2 + 3, bird.width/2, bird.height/6, 0, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw bird image if loaded, otherwise draw fallback sprite
            if (birdImageLoaded && birdImage.complete) {
                // Draw the image
                ctx.drawImage(
                    birdImage,
                    -bird.width / 2,
                    -bird.height / 2,
                    bird.width,
                    bird.height
                );
            } else {
                // Fallback: draw simple sprite if image not loaded
                ctx.fillStyle = '#8B4513';
                ctx.beginPath();
                ctx.ellipse(0, 0, bird.width/2, bird.height/2, 0, 0, Math.PI * 2);
                ctx.fill();
                
                // Simple head
                ctx.fillStyle = '#A0522D';
                ctx.beginPath();
                ctx.arc(-5, -8, 8, 0, Math.PI * 2);
                ctx.fill();
            }
            
            ctx.restore();
        }
        
        // Create pipe
        function createPipe() {
            const minHeight = 80;
            const maxHeight = canvas.height - pipeGap - minHeight;
            const topHeight = Math.random() * (maxHeight - minHeight) + minHeight;
            
            pipes.push({
                x: canvas.width,
                topHeight: topHeight,
                bottomY: topHeight + pipeGap,
                width: pipeWidth,
                passed: false,
                scored: false
            });
        }
        
        // Draw pipes with advanced graphics
        function drawPipes() {
            pipes.forEach(pipe => {
                // Pipe gradient
                const pipeGradient = ctx.createLinearGradient(pipe.x, 0, pipe.x + pipe.width, 0);
                pipeGradient.addColorStop(0, '#228B22');
                pipeGradient.addColorStop(0.5, '#32CD32');
                pipeGradient.addColorStop(1, '#228B22');
                
                // Top pipe
                ctx.fillStyle = pipeGradient;
                ctx.fillRect(pipe.x, 0, pipe.width, pipe.topHeight);
                
                // Top pipe cap
                ctx.fillStyle = '#006400';
                ctx.fillRect(pipe.x - 8, pipe.topHeight - 25, pipe.width + 16, 25);
                ctx.strokeStyle = '#004400';
                ctx.lineWidth = 2;
                ctx.strokeRect(pipe.x - 8, pipe.topHeight - 25, pipe.width + 16, 25);
                
                // Top pipe highlight
                ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.fillRect(pipe.x + 5, 5, 10, pipe.topHeight - 10);
                
                // Bottom pipe
                ctx.fillStyle = pipeGradient;
                ctx.fillRect(pipe.x, pipe.bottomY, pipe.width, canvas.height - pipe.bottomY);
                
                // Bottom pipe cap
                ctx.fillStyle = '#006400';
                ctx.fillRect(pipe.x - 8, pipe.bottomY, pipe.width + 16, 25);
                ctx.strokeStyle = '#004400';
                ctx.lineWidth = 2;
                ctx.strokeRect(pipe.x - 8, pipe.bottomY, pipe.width + 16, 25);
                
                // Bottom pipe highlight
                ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.fillRect(pipe.x + 5, pipe.bottomY + 5, 10, canvas.height - pipe.bottomY - 10);
                
                // Pipe shadow
                ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                ctx.fillRect(pipe.x + pipe.width, 0, 3, canvas.height);
            });
        }
        
        // Draw parallax background
        function drawBackground() {
            // Sky gradient
            const skyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            skyGradient.addColorStop(0, '#87CEEB');
            skyGradient.addColorStop(0.4, '#98D8E8');
            skyGradient.addColorStop(0.7, '#B8E6B8');
            skyGradient.addColorStop(1, '#90EE90');
            ctx.fillStyle = skyGradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Animated stars
            stars.forEach(star => {
                star.y += star.speed;
                if (star.y > canvas.height) {
                    star.y = -5;
                    star.x = Math.random() * canvas.width;
                }
                ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
                ctx.fill();
            });
            
            // Animated clouds
            clouds.forEach(cloud => {
                cloud.x -= cloud.speed;
                if (cloud.x + cloud.width < 0) {
                    cloud.x = canvas.width;
                    cloud.y = Math.random() * 200 + 50;
                }
                
                ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
                ctx.beginPath();
                ctx.arc(cloud.x, cloud.y, cloud.height/2, 0, Math.PI * 2);
                ctx.arc(cloud.x + cloud.width/3, cloud.y, cloud.height/2, 0, Math.PI * 2);
                ctx.arc(cloud.x + cloud.width*2/3, cloud.y, cloud.height/2, 0, Math.PI * 2);
                ctx.arc(cloud.x + cloud.width, cloud.y, cloud.height/2, 0, Math.PI * 2);
                ctx.fill();
            });
        }
        
        // Draw particles
        function drawParticles() {
            particles = particles.filter(p => {
                p.x += p.vx;
                p.y += p.vy;
                p.life--;
                p.vy += 0.2; // gravity
                
                const alpha = p.life / p.maxLife;
                ctx.fillStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${alpha})`;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
                
                return p.life > 0;
            });
        }
        
        // Update game
        function update() {
            if (gameState !== 'playing') return;
            
            frameCount++;
            
            // Update bird
            bird.velocity += bird.gravity;
            bird.y += bird.velocity;
            
            // Create pipes
            if (pipes.length === 0 || pipes[pipes.length - 1].x < canvas.width - 300) {
                createPipe();
            }
            
            // Update pipes
            pipes.forEach(pipe => {
                pipe.x -= pipeSpeed;
                
                // Score point
                if (!pipe.scored && pipe.x + pipe.width < bird.x) {
                    pipe.scored = true;
                    score++;
                    scoreElement.textContent = score;
                    createParticles(pipe.x + pipe.width, canvas.height / 2, {r: 255, g: 215, b: 0});
                    
                    if (score > highScore) {
                        highScore = score;
                        highScoreElement.textContent = 'Best: ' + highScore;
                        localStorage.setItem('flappySparrowHighScore', highScore);
                    }
                }
                
                // Collision detection
                if (bird.x < pipe.x + pipe.width &&
                    bird.x + bird.width > pipe.x &&
                    (bird.y < pipe.topHeight || bird.y + bird.height > pipe.bottomY)) {
                    gameState = 'gameOver';
                    createParticles(bird.x + bird.width/2, bird.y + bird.height/2, {r: 255, g: 0, b: 0});
                }
            });
            
            // Remove off-screen pipes
            pipes = pipes.filter(pipe => pipe.x + pipe.width > 0);
            
            // Boundary check
            if (bird.y + bird.height > canvas.height || bird.y < 0) {
                gameState = 'gameOver';
                createParticles(bird.x + bird.width/2, bird.y + bird.height/2, {r: 255, g: 0, b: 0});
            }
        }
        
        // Draw everything
        function draw() {
            // Clear canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw background
            drawBackground();
            
            if (gameState === 'menu') {
                drawPipes();
                drawSparrow();
                drawParticles();
                
                // Menu overlay
                ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = 'white';
                ctx.font = 'bold 48px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('FLAPPY SPARROW', canvas.width/2, canvas.height/2 - 100);
                
                
                ctx.font = '20px Arial';
                ctx.fillText('Click or Press SPACE to Start', canvas.width/2, canvas.height/2 + 50);
                
                ctx.font = '16px Arial';
                ctx.fillText('Use mouse or spacebar to fly', canvas.width/2, canvas.height/2 + 100);
                
                instructionsElement.style.display = 'none';
                return;
            }
            
            if (gameState === 'gameOver') {
                drawPipes();
                drawSparrow();
                drawParticles();
                
                // Game over overlay
                ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#FF6B6B';
                ctx.font = 'bold 42px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('GAME OVER', canvas.width/2, canvas.height/2 - 80);
                
                ctx.fillStyle = 'white';
                ctx.font = 'bold 32px Arial';
                ctx.fillText('Score: ' + score, canvas.width/2, canvas.height/2 - 20);
                
                ctx.font = '24px Arial';
                ctx.fillText('Best: ' + highScore, canvas.width/2, canvas.height/2 + 30);
                
                ctx.font = '20px Arial';
                ctx.fillText('Click or Press SPACE to Restart', canvas.width/2, canvas.height/2 + 100);
                
                instructionsElement.style.display = 'none';
                return;
            }
            
            if (gameState === 'playing') {
                drawPipes();
                drawSparrow();
                drawParticles();
                instructionsElement.style.display = 'none';
            }
        }
        
        // Game loop
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        // Input handlers
        function handleInput() {
            if (gameState === 'menu' || gameState === 'gameOver') {
                // Reset game
                gameState = 'playing';
                bird.y = 350;
                bird.velocity = 0;
                bird.rotation = 0;
                bird.trail = [];
                pipes = [];
                score = 0;
                scoreElement.textContent = '0';
                frameCount = 0;
                instructionsElement.style.display = 'block';
            } else if (gameState === 'playing') {
                bird.velocity = bird.jumpPower;
                playOuchSound();
                createParticles(bird.x + bird.width/2, bird.y + bird.height/2, {r: 139, g: 69, b: 19});
            }
        }
        
        canvas.addEventListener('click', handleInput);
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                handleInput();
            }
        });
        
        // Start game loop
        gameLoop();
    </script>
</body>
</html>
"""

# Replace the placeholders with actual data URIs
GAME_HTML = GAME_HTML_TEMPLATE.replace('{AUDIO_DATA_URI}', audio_data_uri)
GAME_HTML = GAME_HTML.replace('{BIRD_IMAGE_DATA_URI}', bird_image_data_uri if bird_image_data_uri else '')

def main():
    st.title("🐦 Flappy Sparrow 🐦")
    st.markdown("---")
    
    
    # Display the game
    st.components.v1.html(GAME_HTML, height=750)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p style="font-size: 14px;">
            <strong>Controls:</strong> Click or Press SPACE to fly<br>
            <strong>Goal:</strong> Navigate through pipes and achieve the highest score!
        </p>
        <p style="margin-top: 10px; font-size: 12px;">
            Made with ❤️ using Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
