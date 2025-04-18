def create_surprise_timer():
    """
    Creates an impressive countdown timer in the sidebar that reveals a surprise celebration
    when it reaches zero. Includes animations, confetti, and a custom message.
    """
    # CSS for the timer and animations
    st.markdown("""
    <style>
    /* Timer Styling */
    .surprise-timer-container {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
        border: 2px solid #fff;
    }
    
    .timer-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: #333;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }
    
    .countdown-display {
        font-size: 2rem;
        font-weight: bold;
        color: #5a283d;
        background: rgba(255,255,255,0.5);
        border-radius: 10px;
        padding: 5px 10px;
        display: inline-block;
        min-width: 120px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        margin-bottom: 5px;
    }
    
    .timer-subtitle {
        font-size: 0.9rem;
        color: #5a283d;
        font-style: italic;
        margin-bottom: 5px;
    }
    
    /* Animated Background */
    .surprise-timer-container::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.3) 50%,
            rgba(255,255,255,0) 100%
        );
        transform: rotate(45deg);
        animation: shimmer 3s infinite linear;
        z-index: 1;
    }
    
    .timer-content {
        position: relative;
        z-index: 2;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-50%) translateY(-50%) rotate(45deg); }
        100% { transform: translateX(50%) translateY(50%) rotate(45deg); }
    }
    
    /* Floating Hearts Animation */
    .floating-heart {
        position: absolute;
        font-size: 1.2rem;
        animation: float-up 10s linear infinite;
        opacity: 0;
        z-index: 0;
    }
    
    @keyframes float-up {
        0% {
            transform: translateY(100%) translateX(0) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 0.7;
        }
        90% {
            opacity: 0.5;
        }
        100% {
            transform: translateY(-100%) translateX(var(--tx)) rotate(var(--rot-end));
            opacity: 0;
        }
    }
    
    /* Rose Animation */
    .rose-container {
        margin: 20px 0;
        text-align: center;
        height: 150px;
        position: relative;
        overflow: visible;
    }
    
    .rose {
        display: inline-block;
        font-size: 2.5rem;
        animation: grow-rose 3s ease-out forwards;
        opacity: 0;
        transform: scale(0);
        text-shadow: 0 0 10px rgba(255,0,128,0.5);
        position: relative;
        z-index: 10;
    }
    
    .rose-leaf {
        position: absolute;
        color: #4CAF50;
        font-size: 1.5rem;
        opacity: 0;
        z-index: 5;
        pointer-events: none;
    }
    
    @keyframes grow-rose {
        0% {
            opacity: 0;
            transform: scale(0) rotate(-45deg);
        }
        50% {
            opacity: 0.5;
            transform: scale(0.5) rotate(-20deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotate(0);
        }
    }
    
    @keyframes grow-leaf {
        0% {
            opacity: 0;
            transform: scale(0);
        }
        50% {
            opacity: 0.7;
            transform: scale(0.7);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Surprise Reveal Animation */
    .surprise-message {
        margin: 20px 0;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(45deg, #ff9a9e, #fad0c4, #fad0c4, #ff9a9e);
        background-size: 300% 300%;
        color: #5a283d;
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        opacity: 0;
        transform: translateY(20px);
        animation: reveal-message 1s ease-out forwards,
                   gradient-shift 5s ease infinite;
    }
    
    @keyframes reveal-message {
        0% {
            opacity: 0;
            transform: translateY(20px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Confetti Animation */
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background-color: var(--color);
        opacity: 0;
        animation: confetti-fall var(--fall-duration) linear forwards,
                   confetti-shake var(--shake-duration) ease-in-out infinite alternate;
        z-index: 1000;
        pointer-events: none;
    }
    
    @keyframes confetti-fall {
        0% {
            opacity: 1;
            top: -10%;
        }
        80% {
            opacity: 1;
        }
        100% {
            opacity: 0;
            top: 100%;
        }
    }
    
    @keyframes confetti-shake {
        0% {
            transform: translateX(0);
        }
        100% {
            transform: translateX(var(--shake-direction));
        }
    }
    
    /* Heartbeat Effect */
    .heartbeat {
        display: inline-block;
        animation: heartbeat 1s infinite;
    }
    
    @keyframes heartbeat {
        0% { transform: scale(1); }
        25% { transform: scale(1.1); }
        40% { transform: scale(1); }
        60% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Button Styling */
    .cute-button {
        background: linear-gradient(45deg, #ff9a9e, #fad0c4);
        color: #5a283d;
        border: none;
        border-radius: 20px;
        padding: 8px 15px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        display: inline-block;
        margin-top: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .cute-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 15px rgba(0,0,0,0.15);
    }
    
    .cute-button:active {
        transform: translateY(-1px);
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
    }
    
    .cute-button::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            to bottom right,
            rgba(255,255,255,0) 0%,
            rgba(255,255,255,0.3) 50%,
            rgba(255,255,255,0) 100%
        );
        transform: rotate(45deg);
        transition: all 0.3s ease;
        z-index: 1;
    }
    
    .cute-button:hover::after {
        animation: button-shimmer 1s forwards;
    }
    
    @keyframes button-shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .cute-button span {
        position: relative;
        z-index: 2;
    }
    
    /* Notification indicator that something is coming */
    .timer-indicator {
        padding: 10px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 10px;
        margin-top: 10px;
        border: 1px dashed #ff6b95;
        animation: pulse-border 2s infinite;
    }
    
    @keyframes pulse-border {
        0% { border-color: #ff6b95; }
        50% { border-color: #ff9cc3; }
        100% { border-color: #ff6b95; }
    }
    
    /* Timer preview animation */
    .coming-soon-hearts {
        height: 30px;
        position: relative;
        margin: 10px 0;
    }
    
    .preview-heart {
        position: absolute;
        font-size: 1rem;
        opacity: 0;
        left: 50%;
        animation: preview-beat 3s infinite;
    }
    
    .preview-heart:nth-child(1) {
        animation-delay: 0s;
    }
    
    .preview-heart:nth-child(2) {
        animation-delay: 1s;
    }
    
    .preview-heart:nth-child(3) {
        animation-delay: 2s;
    }
    
    @keyframes preview-beat {
        0% {
            opacity: 0;
            transform: translateY(0) translateX(-50%) scale(0.5);
        }
        20% {
            opacity: 1;
            transform: translateY(-10px) translateX(-50%) scale(1);
        }
        80% {
            opacity: 1;
            transform: translateY(-20px) translateX(-50%) scale(1);
        }
        100% {
            opacity: 0;
            transform: translateY(-30px) translateX(-50%) scale(0.5);
        }
    }
    
    /* Main notification panel for the surprise timer */
    .timer-notification {
        background: linear-gradient(135deg, #ffcdd2, #f8bbd0);
        border-radius: 15px;
        padding: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid #fff;
        animation: notification-glow 3s infinite alternate;
    }
    
    @keyframes notification-glow {
        0% { box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3); }
        100% { box-shadow: 0 4px 20px rgba(255, 105, 180, 0.7); }
    }
    
    .timer-notification-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #d81b60;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .timer-notification-content {
        font-size: 1rem;
        color: #5a283d;
        text-align: center;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = datetime.now()
        
    if 'timer_duration' not in st.session_state:
        st.session_state.timer_duration = 10  # Default 10 minutes
        
    if 'surprise_revealed' not in st.session_state:
        st.session_state.surprise_revealed = False
        
    if 'timer_expired' not in st.session_state:
        st.session_state.timer_expired = False
        
    if 'reset_counter' not in st.session_state:
        st.session_state.reset_counter = 0

    # Function to reset the timer
    def reset_timer():
        st.session_state.timer_start = datetime.now()
        st.session_state.surprise_revealed = False
        st.session_state.timer_expired = False
        st.session_state.reset_counter += 1

    # Function to generate floating hearts HTML
    def generate_floating_hearts(count=10):
        hearts = []
        for i in range(count):
            delay = random.uniform(0, 10)
            duration = random.uniform(7, 15)
            left = random.uniform(5, 95)
            tx = random.uniform(-100, 100)
            rot_start = random.uniform(-45, 45)
            rot_end = random.uniform(-180, 180)
            heart_type = random.choice(['❤️', '💕', '💗', '💓', '💖'])
            
            heart = f"""
            <div class="floating-heart" style="
                left: {left}%;
                animation-delay: {delay}s;
                animation-duration: {duration}s;
                --tx: {tx}px;
                --rot-end: {rot_end}deg;
                transform: rotate({rot_start}deg);
            ">{heart_type}</div>
            """
            hearts.append(heart)
        return ''.join(hearts)

    # Function to generate confetti HTML
    def generate_confetti(count=100):
        confetti_html = []
        for i in range(count):
            x = random.uniform(0, 100)
            fall_duration = random.uniform(3, 8)
            shake_duration = random.uniform(0.5, 2)
            shake_direction = f"{random.uniform(-100, 100)}px"
            color = random.choice([
                '#ff9a9e', '#fad0c4', '#f6d365', '#fda085', '#f6d365', 
                '#fbc2eb', '#a18cd1', '#fbc2eb', '#a6c1ee', '#fbc2eb'
            ])
            width = random.uniform(5, 15)
            height = random.uniform(5, 15)
            border_radius = random.choice(['50%', '0'])
            rotation = random.uniform(0, 360)

            confetti_piece = f"""
            <div class="confetti" style="
                left: {x}%;
                --fall-duration: {fall_duration}s;
                --shake-duration: {shake_duration}s;
                --shake-direction: {shake_direction};
                --color: {color};
                width: {width}px;
                height: {height}px;
                border-radius: {border_radius};
                transform: rotate({rotation}deg);
            "></div>
            """
            confetti_html.append(confetti_piece)
        return ''.join(confetti_html)

    # Function to generate rose animation - FIXED to ensure proper rendering
    def generate_rose_animation():
        # Simplified rose HTML with better positioning
        rose_html = """
        <div class="rose-container">
            <div class="rose" style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);">🌹</div>
        """
        
        # Add some leaves around the rose with simplified and more reliable positioning
        for i in range(6):
            angle = i * 60
            distance = 50 + i * 5  # More predictable distance
            delay = 0.5 + i * 0.2  # More predictable delay
            
            # Calculate positions with simpler math to avoid potential errors
            x = int(distance * math.cos(math.radians(angle)))
            y = int(distance * math.sin(math.radians(angle)))
            
            leaf_html = f"""
            <div class="rose-leaf" style="
                left: calc(50% + {x}px);
                top: calc(50% + {y}px);
                animation: grow-leaf 2s ease-out {delay}s forwards;
                transform: rotate({angle}deg);
            ">🍃</div>
            """
            rose_html += leaf_html
        
        rose_html += "</div>"
        return rose_html

    # Generate surprise messages
    surprise_messages = [
        "I've been waiting to tell you how special you are! 💕",
        "You make my heart smile every single day! 💖",
        "Just wanted to remind you that you're absolutely amazing! 💗",
        "Your love makes every moment magical! 💓",
        "I cherish every moment we spend together! 💘"
    ]
    
    # Calculate remaining time
    end_time = st.session_state.timer_start + timedelta(minutes=st.session_state.timer_duration)
    remaining = end_time - datetime.now()
    minutes, seconds = divmod(max(0, remaining.total_seconds()), 60)  # Prevent negative values
    
    # Check if timer has expired
    if remaining.total_seconds() <= 0 and not st.session_state.timer_expired:
        st.session_state.timer_expired = True
        st.session_state.surprise_revealed = True
    
    # Add a visible notification FIRST in the main content area
    st.markdown("""
    <div class="timer-notification">
        <div class="timer-notification-title">❤️ Special Surprise Coming! ❤️</div>
        <div class="timer-notification-content">
            A romantic surprise is waiting for you! Keep an eye on the timer in the sidebar. 
            When it reaches zero, something special will appear just for you!
        </div>
        <div class="coming-soon-hearts">
            <div class="preview-heart">❤️</div>
            <div class="preview-heart">💕</div>
            <div class="preview-heart">💖</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the timer in sidebar
    with st.sidebar:
        st.markdown('<div class="surprise-timer-container">', unsafe_allow_html=True)
        st.markdown('<div class="timer-content">', unsafe_allow_html=True)
        
        # Generate and add floating hearts
        st.markdown(generate_floating_hearts(15), unsafe_allow_html=True)
        
        st.markdown('<div class="timer-title"><span class="heartbeat">❤️</span> Surprise Timer <span class="heartbeat">❤️</span></div>', unsafe_allow_html=True)
        
        if remaining.total_seconds() > 0:
            st.markdown(f'<div class="countdown-display">{int(minutes):02}:{int(seconds):02}</div>', unsafe_allow_html=True)
            st.markdown('<div class="timer-subtitle">Something special is coming...</div>', unsafe_allow_html=True)
            
            # Add indicator of what's coming
            st.markdown("""
            <div class="timer-indicator">
                <div style="text-align: center; font-weight: bold; color: #d81b60;">
                    Wait for it...
                </div>
                <div class="coming-soon-hearts">
                    <div class="preview-heart">💖</div>
                    <div class="preview-heart">💝</div>
                    <div class="preview-heart">💓</div>
                </div>
                <div style="text-align: center; font-size: 0.9rem; color: #5a283d; margin-top: 5px;">
                    A romantic surprise just for you!
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="countdown-display">00:00</div>', unsafe_allow_html=True)
            st.markdown('<div class="timer-subtitle">Surprise is here!</div>', unsafe_allow_html=True)
        
        # Timer control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Reset Timer", key=f"reset_timer_{st.session_state.reset_counter}"):
                reset_timer()
        with col2:
            # Changed button label to be more obvious
            if st.button("Show Surprise Now", key=f"quick_test_{st.session_state.reset_counter}"):
                st.session_state.surprise_revealed = True
                st.session_state.timer_expired = True
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Display the surprise if timer has expired
        if st.session_state.surprise_revealed:
            # Add confetti
            st.markdown(generate_confetti(80), unsafe_allow_html=True)
            
            # Random selection of a surprise message
            surprise_message = random.choice(surprise_messages)
            
            # Display rose animation with fixed implementation
            st.markdown(generate_rose_animation(), unsafe_allow_html=True)
            
            # Display the surprise message
            st.markdown(f'<div class="surprise-message">{surprise_message}</div>', unsafe_allow_html=True)
            
            # Additional animated elements for extra charm
            st.markdown("""
            <div style="text-align: center; margin-top: 20px; animation: fadeIn 2s forwards;">
                <div style="font-size: 2rem; margin-bottom: 10px;">✨✨✨</div>
                <div style="font-size: 1.2rem; color: #5a283d; margin-bottom: 15px;">
                    Just a little reminder of how much you mean to me!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a cute button with event handler fix to avoid showing alert
            st.markdown("""
            <div style="text-align: center;">
                <button class="cute-button" id="special-message-btn">
                    <span>Click Me! 💖</span>
                </button>
                <script>
                    // Use a more secure approach with an event listener
                    document.addEventListener('DOMContentLoaded', function() {
                        const specialBtn = document.getElementById('special-message-btn');
                        if (specialBtn) {
                            specialBtn.addEventListener('click', function() {
                                // Create a cute message instead of an alert
                                const messageDiv = document.createElement('div');
                                messageDiv.style.padding = '10px';
                                messageDiv.style.background = 'rgba(255, 182, 193, 0.8)';
                                messageDiv.style.borderRadius = '10px';
                                messageDiv.style.marginTop = '10px';
                                messageDiv.style.textAlign = 'center';
                                messageDiv.style.animation = 'fadeIn 0.5s forwards';
                                messageDiv.innerHTML = '<span style="font-weight: bold; color: #d81b60;">I think you are amazing! 💖</span>';
                                
                                // Add message after the button
                                this.parentNode.appendChild(messageDiv);
                                
                                // Remove after 3 seconds
                                setTimeout(() => {
                                    messageDiv.style.animation = 'fadeOut 0.5s forwards';
                                    setTimeout(() => messageDiv.remove(), 500);
                                }, 3000);
                            });
                        }
                    });
                </script>
            </div>
            """, unsafe_allow_html=True)

    # Return whether the surprise is revealed (can be used by the main app)
    return st.session_state.surprise_revealed
