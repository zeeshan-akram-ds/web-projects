def render_constellation_creator():
    """
    Create a highly customizable and interactive constellation creator
    that allows Faryal to create personalized star constellations.
    """
    import numpy as np
    import pandas as pd
    from PIL import Image
    from io import BytesIO
    import base64
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as path_effects
    
    st.markdown("""
    <h2 style='text-align: center; color: #8A2BE2;'>
      <span style='margin-right: 10px'>✨</span>
      Starlight Constellation Creator
      <span style='margin-left: 10px'>✨</span>
    </h2>
    """, unsafe_allow_html=True)
    
    # Initialize session state variables if they don't exist
    if 'constellation_stars' not in st.session_state:
        st.session_state.constellation_stars = pd.DataFrame({
            'x': [], 'y': [], 'size': [], 'color': [], 'name': [], 'description': []
        })
    
    if 'constellation_lines' not in st.session_state:
        st.session_state.constellation_lines = []
    
    if 'last_constellation_action' not in st.session_state:
        st.session_state.last_constellation_action = None
    
    if 'constellation_active_name' not in st.session_state:
        st.session_state.constellation_active_name = "Our Love Story"
    
    if 'constellation_saved' not in st.session_state:
        st.session_state.constellation_saved = {}
    
    if 'drawing_mode' not in st.session_state:
        st.session_state.drawing_mode = "stars"  # stars, lines, or text
    
    if 'background_style' not in st.session_state:
        st.session_state.background_style = "Midnight Blue"
    
    # Custom CSS
    st.markdown("""
    <style>
    .constellation-container {
        background: linear-gradient(180deg, #0a0a2a 0%, #1a1a4a 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    
    .star-button {
        background: none;
        border: none;
        color: yellow;
        font-size: 20px;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .star-button:hover {
        transform: scale(1.5);
    }
    
    .constellation-controls {
        background: rgba(10, 10, 42, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
    }
    
    .control-title {
        color: #9370DB;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .constellation-description {
        background: rgba(20, 20, 50, 0.6);
        border-radius: 8px;
        padding: 10px;
        color: #E6E6FA;
        margin-top: 10px;
        font-style: italic;
    }
    
    .constellation-tab {
        background: rgba(30, 30, 70, 0.6);
        border-radius: 8px 8px 0 0;
        padding: 8px 15px;
        color: #B0C4DE;
        display: inline-block;
        margin-right: 5px;
        cursor: pointer;
    }
    
    .constellation-tab.active {
        background: rgba(70, 70, 120, 0.8);
        color: white;
    }
    
    .star-glow {
        filter: drop-shadow(0 0 6px rgba(255, 255, 100, 0.8));
    }
    
    @keyframes twinkle {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }
    
    .background-star {
        position: absolute;
        background-color: white;
        border-radius: 50%;
        animation: twinkle 3s infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Background style selector
    st.sidebar.markdown("## ✨ Constellation Settings")
    
    background_options = {
        "Midnight Blue": "#0a0a2a",
        "Deep Space": "#000020",
        "Cosmic Purple": "#2d0a42",
        "Northern Lights": "#0a2a1a",
        "Sunset Horizon": "#2a0a1a",
        "Dawn Sky": "#1a0a2a"
    }
    
    selected_bg = st.sidebar.selectbox(
        "Background Theme",
        options=list(background_options.keys()),
        index=list(background_options.keys()).index(st.session_state.background_style)
    )
    
    st.session_state.background_style = selected_bg
    
    # Star customization
    st.sidebar.markdown("### ⭐ Star Style")
    star_color = st.sidebar.color_picker("Star Color", "#FFD700")
    star_size = st.sidebar.slider("Star Size", 1, 15, 5)
    
    # Create tabs for different modes
    tabs_col1, tabs_col2, tabs_col3, tabs_col4 = st.columns(4)
    
    with tabs_col1:
        stars_tab_class = "constellation-tab active" if st.session_state.drawing_mode == "stars" else "constellation-tab"
        stars_tab = st.markdown(f"<div class='{stars_tab_class}' id='stars-tab'>✨ Add Stars</div>", unsafe_allow_html=True)
        if stars_tab:
            st.session_state.drawing_mode = "stars"
    
    with tabs_col2:
        lines_tab_class = "constellation-tab active" if st.session_state.drawing_mode == "lines" else "constellation-tab"
        lines_tab = st.markdown(f"<div class='{lines_tab_class}' id='lines-tab'>🔗 Connect Stars</div>", unsafe_allow_html=True)
        if lines_tab:
            st.session_state.drawing_mode = "lines"
            
    with tabs_col3:
        text_tab_class = "constellation-tab active" if st.session_state.drawing_mode == "text" else "constellation-tab"
        text_tab = st.markdown(f"<div class='{text_tab_class}' id='text-tab'>📝 Add Text</div>", unsafe_allow_html=True)
        if text_tab:
            st.session_state.drawing_mode = "text"
            
    with tabs_col4:
        template_tab_class = "constellation-tab active" if st.session_state.drawing_mode == "template" else "constellation-tab"
        template_tab = st.markdown(f"<div class='{template_tab_class}' id='template-tab'>💫 Templates</div>", unsafe_allow_html=True)
        if template_tab:
            st.session_state.drawing_mode = "template"
    
    # Main constellation canvas
    canvas_col, controls_col = st.columns([3, 1])
    
    # Function to render the constellation
    def render_constellation(stars_df, lines, background_color, figsize=(10, 6)):
        fig, ax = plt.subplots(figsize=figsize, facecolor=background_color)
        ax.set_facecolor(background_color)
        
        # Hide axes
        ax.set_axis_off()
        
        # Set plot limits
        ax.set_xlim(-10, 110)
        ax.set_ylim(-10, 110)
        
        # Add background stars (random smaller stars)
        np.random.seed(42)  # for reproducibility
        bg_stars_x = np.random.uniform(0, 100, 200)
        bg_stars_y = np.random.uniform(0, 100, 200)
        bg_stars_size = np.random.uniform(0.1, 0.8, 200)
        
        ax.scatter(bg_stars_x, bg_stars_y, s=bg_stars_size, color='white', alpha=0.5)
        
        # Draw connecting lines
        for line in lines:
            if len(line) >= 2:
                line_stars = stars_df.loc[stars_df.index.isin(line)]
                if not line_stars.empty and len(line_stars) >= 2:
                    x_vals = line_stars['x'].values
                    y_vals = line_stars['y'].values
                    ax.plot(x_vals, y_vals, '-', color='rgba(255, 255, 255, 0.5)', linewidth=1.5, alpha=0.7)
        
        # Add the custom stars
        if not stars_df.empty:
            for idx, star in stars_df.iterrows():
                # Main star
                main_star = ax.scatter(star['x'], star['y'], s=star['size']*20, color=star['color'], 
                              alpha=0.9, edgecolor='white', linewidth=0.5)
                
                # Glow effect
                main_star.set_path_effects([
                    path_effects.SimpleLineShadow(offset=(0, 0), shadow_color=star['color'], alpha=0.6),
                    path_effects.Normal()
                ])
                
                # Add star name if present
                if star['name']:
                    text = ax.text(star['x'], star['y'] - 3, star['name'], 
                                  ha='center', va='top', color='white', fontsize=8)
                    text.set_path_effects([
                        path_effects.withStroke(linewidth=2, foreground=background_color)
                    ])
        
        # Add constellation name
        if st.session_state.constellation_active_name:
            title_text = ax.text(50, 95, st.session_state.constellation_active_name, 
                               ha='center', va='top', color='white', fontsize=16, weight='bold')
            title_text.set_path_effects([
                path_effects.withStroke(linewidth=3, foreground=background_color)
            ])
        
        plt.tight_layout()
        
        # Convert plot to image
        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        # Encode the image to base64 string
        img_str = base64.b64encode(buf.read()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    # Create templates
    def get_template_stars(template_name):
        templates = {
            "Faryal Name": [
                # F
                {'x': 20, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 20, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 20, 'y': 60, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 20, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 25, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 30, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 25, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 30, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                # A
                {'x': 40, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 45, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 50, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 42, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 48, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                # R
                {'x': 60, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 60, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 60, 'y': 60, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 60, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 65, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 70, 'y': 75, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 65, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 65, 'y': 60, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 70, 'y': 55, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                # Y
                {'x': 80, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 85, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 90, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 85, 'y': 60, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 85, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                # A
                {'x': 100, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 105, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 110, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 102, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 108, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                # L
                {'x': 120, 'y': 80, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 120, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 120, 'y': 60, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 120, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 125, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 130, 'y': 50, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
            ],
            "Heart": [
                {'x': 50, 'y': 70, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 40, 'y': 80, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 30, 'y': 70, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 35, 'y': 60, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 40, 'y': 50, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 50, 'y': 40, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 60, 'y': 50, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 65, 'y': 60, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 70, 'y': 70, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
                {'x': 60, 'y': 80, 'size': 5, 'color': '#FF69B4', 'name': '', 'description': ''},
            ],
            "Infinity": [
                {'x': 30, 'y': 60, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 20, 'y': 50, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 20, 'y': 70, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 40, 'y': 50, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 40, 'y': 70, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 50, 'y': 60, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 60, 'y': 50, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 60, 'y': 70, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 70, 'y': 50, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 70, 'y': 70, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
                {'x': 80, 'y': 60, 'size': 5, 'color': '#00BFFF', 'name': '', 'description': ''},
            ],
            "Crown": [
                {'x': 50, 'y': 80, 'size': 7, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 30, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 40, 'y': 75, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 50, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 60, 'y': 75, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 70, 'y': 70, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 35, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 65, 'y': 65, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
                {'x': 50, 'y': 60, 'size': 5, 'color': '#FFD700', 'name': '', 'description': ''},
            ],
            "Our Story": [
                {'x': 30, 'y': 80, 'size': 7, 'color': '#9370DB', 'name': 'First Date', 'description': 'When we first met'},
                {'x': 45, 'y': 75, 'size': 6, 'color': '#FF69B4', 'name': 'First Kiss', 'description': 'Under the stars'},
                {'x': 60, 'y': 70, 'size': 8, 'color': '#00BFFF', 'name': 'Proposal', 'description': 'When I asked...'},
                {'x': 75, 'y': 65, 'size': 7, 'color': '#FFD700', 'name': 'Wedding', 'description': 'Our special day'},
                {'x': 90, 'y': 60, 'size': 5, 'color': '#FF4500', 'name': 'Anniversary', 'description': 'Every year together'},
                {'x': 30, 'y': 50, 'size': 5, 'color': '#32CD32', 'name': 'First Home', 'description': 'Our sanctuary'},
                {'x': 50, 'y': 40, 'size': 6, 'color': '#FF8C00', 'name': 'Future', 'description': 'Dreams ahead'},
            ]
        }
        
        if template_name in templates:
            return templates[template_name]
        return []
    
    # Create template lines
    def get_template_lines(template_name):
        # Each line is a list of indices in the stars dataframe
        templates = {
            "Faryal Name": [
                # F
                [0, 1, 2, 3],  # Vertical line
                [0, 5, 6],      # Top horizontal
                [2, 7, 8],      # Middle horizontal
                # A
                [9, 10, 11],    # Left diagonal
                [11, 12, 10],   # Right diagonal
                [13, 14],       # Middle horizontal
                # R
                [15, 16, 17, 18],  # Vertical line
                [15, 19, 20],      # Top curve
                [17, 21, 22, 23],  # Bottom curve
                # Y
                [24, 25, 26],      # Top V
                [25, 27, 28],      # Bottom stem
                # A
                [29, 30, 31],      # Left and right diagonal
                [32, 33],          # Middle horizontal
                # L
                [34, 35, 36, 37, 38, 39]  # L shape
            ],
            "Heart": [
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
            ],
            "Infinity": [
                [0, 1, 2, 0, 3, 4, 5, 6, 7, 5, 8, 9, 10]
            ],
            "Crown": [
                [1, 2, 0, 4, 5],  # Top of crown
                [1, 6, 8, 7, 5],  # Bottom of crown
                [2, 3, 4]         # Middle connection
            ],
            "Our Story": [
                [0, 1, 2, 3, 4],  # Main storyline
                [0, 5, 6, 4]      # Alternative path
            ]
        }
        
        if template_name in templates:
            return templates[template_name]
        return []
    
    # Draw the constellation in the canvas column
    with canvas_col:
        st.markdown("<div class='constellation-container'>", unsafe_allow_html=True)
        
        # Preview the constellation using matplotlib
        if not st.session_state.constellation_stars.empty or st.session_state.constellation_lines:
            bg_color = background_options[st.session_state.background_style]
            img_data = render_constellation(
                st.session_state.constellation_stars, 
                st.session_state.constellation_lines,
                bg_color
            )
            
            st.markdown(f"""
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <img src="{img_data}" style="max-width: 100%; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.3);">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="height: 300px; display: flex; justify-content: center; align-items: center; color: #aaa;">
                <div style="text-align: center;">
                    <div style="font-size: 40px;">✨</div>
                    <div>Create your constellation by adding stars or selecting a template</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Interactive canvas for clicking
        if st.session_state.drawing_mode in ["stars", "lines", "text"]:
            st.markdown("<div class='constellation-controls'>", unsafe_allow_html=True)
            
            # Create a clickable canvas
            click_col1, click_col2 = st.columns([3, 1])
            
            with click_col1:
                st.write("📌 Click below to place stars:")
                
                # Create a placeholder for the clickable area
                canvas_placeholder = st.empty()
                canvas_placeholder.markdown("""
                <div id="clickable-canvas" style="height: 200px; background: rgba(10, 10, 30, 0.5); 
                     border-radius: 8px; position: relative; cursor: crosshair;"></div>
                """, unsafe_allow_html=True)
                
                # Create buttons for adding stars at coordinate positions
                col1, col2 = st.columns(2)
                
                with col1:
                    x_coord = st.number_input("X Position (0-100)", min_value=0, max_value=100, value=50, step=5)
                
                with col2:
                    y_coord = st.number_input("Y Position (0-100)", min_value=0, max_value=100, value=50, step=5)
                
                if st.session_state.drawing_mode == "stars":
                    if st.button("Add Star at Position"):
                        new_star = {
                            'x': x_coord,
                            'y': y_coord,
                            'size': star_size,
                            'color': star_color,
                            'name': '',
                            'description': ''
                        }
                        
                        # Add the star to the dataframe
                        st.session_state.constellation_stars = pd.concat([
                            st.session_state.constellation_stars,
                            pd.DataFrame([new_star])
                        ], ignore_index=True)
                        
                        st.session_state.last_constellation_action = "added_star"
                        st.experimental_rerun()
                
                elif st.session_state.drawing_mode == "lines":
                    # Select stars to connect
                    if not st.session_state.constellation_stars.empty:
                        star_options = [f"Star {i} at ({row['x']}, {row['y']})" + (f" - {row['name']}" if row['name'] else "") 
                                         for i, row in st.session_state.constellation_stars.iterrows()]
                        
                        star1 = st.selectbox("Connect from:", ["Select a star"] + star_options)
                        star2 = st.selectbox("Connect to:", ["Select a star"] + star_options)
                        
                        if st.button("Connect Stars") and star1 != "Select a star" and star2 != "Select a star":
                            # Extract indices from selection strings
                            idx1 = int(star1.split(" ")[1])
                            idx2 = int(star2.split(" ")[1])
                            
                            # Check if we should start a new line or continue an existing one
                            new_line = True
                            for i, line in enumerate(st.session_state.constellation_lines):
                                if line[-1] == idx1:
                                    # Continue this line
                                    st.session_state.constellation_lines[i].append(idx2)
                                    new_line = False
                                    break
                            
                            if new_line:
                                st.session_state.constellation_lines.append([idx1, idx2])
                            
                            st.session_state.last_constellation_action = "added_line"
                            st.experimental_rerun()
                
                elif st.session_state.drawing_mode == "text":
                    # Add labels/names to stars
                    if not st.session_state.constellation_stars.empty:
                        star_options = [f"Star {i} at ({row['x']}, {row['y']})" + (f" - {row['name']}" if row['name'] else "") 
                                        for i, row in st.session_state.constellation_stars.iterrows()]
                        
                        selected_star = st.selectbox("Select star to label:", ["Select a star"] + star_options)
                        
                        if selected_star != "Select a star":
                            idx = int(selected_star.split(" ")[1])
                            star_name = st.text_input("Star name:", 
                                                    value=st.session_state.constellation_stars.iloc[idx]['name'] 
                                                    if idx < len(st.session_state.constellation_stars) else "")
                            
                            star_desc = st.text_area("Star description (memory/meaning):", 
                                                    value=st.session_state.constellation_stars.iloc[idx]['description']
                                                    if idx < len(st.session_state.constellation_stars) else "")
                            
                            if st.button("Save Star Information"):
                                st.session_state.constellation_stars.at[idx, 'name'] = star_name
                                st.session_state.constellation_stars.at[idx, 'description'] = star_desc
                                st.session_state.last_constellation_action = "updated_star_info"
                                st.experimental_rerun()
            
            with click_col2:
                # Controls for managing the constellation
                st.markdown("<div class='control-title'>Constellation Name</div>", unsafe_allow_html=True)
                constellation_name = st.text_input("", value=st.session_state.constellation_active_name, key="constellation_name_input")
                
                if constellation_name != st.session_state.constellation_active_name:
                    st.session_state.constellation_active_name = constellation_name
                    st.experimental_rerun()
                
                st.markdown("<div class='control-title'>Actions</div>", unsafe_allow_html=True)
                
                # Clear button
                if st.button("✨ Clear All"):
                    st.session_state.constellation_stars = pd.DataFrame({
                        'x': [], 'y': [], 'size': [], 'color': [], 'name': [], 'description': []
                    })
                    st.session_state.constellation_lines = []
                    st.session_state.last_constellation_action = "cleared"
                    st.experimental_rerun()
                
                # Remove last star or line
                if st.button("↩️ Undo Last"):
                    if st.session_state.last_constellation_action == "added_star" and not st.session_state.constellation_stars.empty:
                        st.session_state.constellation_stars = st.session_state.constellation_stars.iloc[:-1]
                    elif st.session_state.last_constellation_action == "added_line" and st.session_state.constellation_lines:
                        st.session_state.constellation_lines = st.session_state.constellation_lines[:-1]
                    st.experimental_rerun()
                
                # Save constellation
                if st.button("💾 Save Constellation"):
                    if not st.session_state.constellation_stars.empty:
                        st.session_state.constellation_saved[st.session_state.constellation_active_name] = {
                            'stars': st.session_state.constellation_stars.copy(),
                            'lines': st.session_state.constellation_lines.copy(),
                            'bg_style': st.session_state.background_style
                        }
                        st.success(f"Saved constellation '{st.session_state.constellation_active_name}'!")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Template selection mode
        elif st.session_state.drawing_mode == "template":
            st.markdown("<div class='constellation-controls'>", unsafe_allow_html=True)
            
            template_options = ["Faryal Name", "Heart", "Infinity", "Crown", "Our Story"]
            selected_template = st.selectbox("Choose a template:", template_options)
            
            if st.button("Apply Template"):
                # Get template stars and lines
                template_stars = get_template_stars(selected_template)
                template_lines = get_template_lines(selected_template)
                
                # Convert to DataFrame
                stars_df = pd.DataFrame(template_stars)
                
                # Update session state
                st.session_state.constellation_stars = stars_df
                st.session_state.constellation_lines = template_lines
                st.session_state.constellation_active_name = selected_template
                st.session_state.last_constellation_action = "applied_template"
                
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Controls column
    with controls_col:
        st.markdown("<div class='constellation-controls'>", unsafe_allow_html=True)
        
        # Load saved constellations
        if st.session_state.constellation_saved:
            st.markdown("<div class='control-title'>Your Saved Constellations</div>", unsafe_allow_html=True)
            saved_options = list(st.session_state.constellation_saved.keys())
            selected_saved = st.selectbox("Load constellation:", ["Select..."] + saved_options)
            
            if selected_saved != "Select..." and st.button("Load"):
                saved_data = st.session_state.constellation_saved[selected_saved]
                st.session_state.constellation_stars = saved_data['stars']
                st.session_state.constellation_lines = saved_data['lines']
                st.session_state.constellation_active_name = selected_saved
                st.session_state.background_style = saved_data['bg_style']
                st.session_state.last_constellation_action = "loaded_saved"
                st.experimental_rerun()
        
        # Export options
        st.markdown("<div class='control-title'>Export Your Constellation</div>", unsafe_allow_html=True)
        
        # Generate image for download
        if not st.session_state.constellation_stars.empty:
            bg_color = background_options[st.session_state.background_style]
            img_data = render_constellation(
                st.session_state.constellation_stars, 
                st.session_state.constellation_lines,
                bg_color,
                figsize=(8, 5)
            )
            
            download_btn = st.download_button(
                label="📥 Download as Image",
                data=base64.b64decode(img_data.split(',')[1]),
                file_name=f"{st.session_state.constellation_active_name.replace(' ', '_')}_constellation.png",
                mime="image/png"
            )
        
        # Display star information if available
        if not st.session_state.constellation_stars.empty:
            stars_with_info = st.session_state.constellation_stars[st.session_state.constellation_stars['name'] != '']
            
            if not stars_with_info.empty:
                st.markdown("<div class='control-title'>Star Information</div>", unsafe_allow_html=True)
                
                for _, star in stars_with_info.iterrows():
                    if star['name']:
                        st.markdown(f"""
                        <div class="constellation-description">
                            <div style="color: {star['color']}; font-weight: bold;">⭐ {star['name']}</div>
                            <div>{star['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Meaning of your constellation
        st.markdown("<div class='constellation-controls' style='margin-top: 15px;'>", unsafe_allow_html=True)
        st.markdown("<div class='control-title'>The Meaning of Your Stars</div>", unsafe_allow_html=True)
        
        meaning_text = st.text_area(
            "What does this constellation mean to you?",
            value="This constellation represents our love story and the journey we've shared together. Each star is a memory, each connection a thread in the tapestry of our relationship. Like the stars, our love is eternal and bright.",
            height=150
        )
        
        # Display a special message for Faryal
        st.markdown("""
        <div style='text-align: center; margin-top: 15px; font-style: italic; color: #e6e6fa;'>
            Like this constellation, my love for you, Faryal, is written in the stars.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Help text at the bottom
    st.markdown("""
    <div style='opacity: 0.7; text-align: center; margin-top: 20px; font-size: 14px;'>
        Create your own constellation by adding stars, connecting them, and naming them after special moments in your relationship. 
        You can also choose from templates or save your creations to revisit later.
    </div>
    """, unsafe_allow_html=True)
    
    # Add a special surprise for Faryal that appears occasionally
    if random.random() < 0.2:  # 20% chance to show on each load
        st.balloons()
        st.markdown("""
        <div style='text-align: center; margin-top: 20px; color: #ff69b4; font-size: 18px; animation: twinkle 2s infinite;'>
            ✨ I love you to the stars and beyond, Faryal! ✨
        </div>
        """, unsafe_allow_html=True)
