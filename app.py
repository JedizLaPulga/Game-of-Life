import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
from game_engine import GameEngine
from analysis import analyze_simulation

# Page Configuration
st.set_page_config(
    page_title="Conway's Game of Life",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Beautiful" look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #464b5d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(75, 108, 183, 0.4);
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        .stButton>button {
            width: 100%;
            padding: 0.75rem !important;
            margin-top: 10px;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 auto !important;
            min-width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Helper function to convert grid to RGB image
def grid_to_image(grid_data, colormap_name='magma'):
    # grid_data is float 0.0 to 1.0 (display_grid)
    # Using matplotlib colormap
    cmap = plt.get_cmap(colormap_name)
    # Apply colormap (returns RGBA), drop alpha, convert to uint8
    colored_grid = (cmap(grid_data)[:, :, :3] * 255).astype(np.uint8)
    # Resize for better visibility if grid is small? 
    # Actually streamlit st.image handles interpolation well.
    return colored_grid

# State Initialization for Parameters (Must be global for visibility across reruns)
if 'params' not in st.session_state:
    st.session_state.params = {
        'width': 100,
        'height': 100,
        'prob': 0.15,
        'duration': 100,
        'speed': 30,
        'decay': 0.1,
        'colormap': 'magma'
    }

# Analysis Dialog
@st.dialog("Simulation Result")
def show_analysis(analysis_data):
    st.header(analysis_data['title'])
    st.write(analysis_data['description'])
    
    cols = st.columns(4)
    metrics = analysis_data['metrics']
    keys = list(metrics.keys())
    
    for i, col in enumerate(cols):
        if i < len(keys):
            col.metric(keys[i], metrics[keys[i]])
    
    st.markdown("---")
    if st.button("🔄 Rerun Simulation", type="primary", use_container_width=True):
        st.session_state.run_sim = True
        st.rerun()
        
    st.balloons()

# Configuration Dialog
@st.dialog("⚙️ Mission Control")
def configure_simulation():
    with st.form("config_form"):
        # Use tabs to reduce vertical height and clutter
        tab1, tab2, tab3 = st.tabs(["🌍 World", "⏳ Physics", "🎨 Visuals"])
        
        with tab1:
            c1, c2 = st.columns(2)
            width = c1.slider("Width", 50, 200, st.session_state.params['width'])
            height = c2.slider("Height", 50, 200, st.session_state.params['height'])
            prob = st.slider("Life Probability", 0.0, 1.0, st.session_state.params['prob'])
            
        with tab2:
            speed = st.slider("Speed (FPS)", 1, 60, st.session_state.params['speed'])
            duration = st.slider("Epoch Duration", 10, 500, st.session_state.params['duration'])
        
        with tab3:
            decay = st.slider("Trail Decay", 0.01, 0.5, st.session_state.params['decay'])
            # Find index for selectbox
            current_color = st.session_state.params['colormap']
            options = ["magma", "viridis", "plasma", "inferno", "ocean", "gist_earth"]
            idx = options.index(current_color) if current_color in options else 0
            colormap = st.selectbox("Color Theme", options, index=idx)

        st.write("") # Spacer
        
        # Form Actions
        c_submit, c_random = st.columns([2, 1])
        with c_submit:
            submitted = st.form_submit_button("🚀 Initialize Sequence", type="primary", use_container_width=True)
        with c_random:
            random_run = st.form_submit_button("🎲 Run Random", type="secondary", use_container_width=True)
        
        if submitted:
            st.session_state.params.update({
                'width': width, 'height': height, 'prob': prob, 
                'duration': duration, 'speed': speed, 'decay': decay, 
                'colormap': colormap
            })
            st.session_state.run_sim = True
            st.rerun()
            
        if random_run:
            colors = ["magma", "viridis", "plasma", "inferno", "ocean", "gist_earth"]
            st.session_state.params.update({
                'width': int(np.random.randint(50, 201)), 
                'height': int(np.random.randint(50, 201)), 
                'prob': float(np.random.uniform(0.05, 0.4)), 
                'duration': int(np.random.randint(50, 300)), 
                'speed': int(np.random.randint(10, 60)), 
                'decay': float(np.random.uniform(0.01, 0.3)), 
                'colormap': str(np.random.choice(colors))
            })
            st.session_state.run_sim = True
            st.rerun()

# Header Layout
col_title, col_btn = st.columns([6, 1])
with col_title:
    st.title("🧬 Game of Life: Project Genesis")
    st.caption("A cellular automaton simulation exploring the emergence of complexity.")

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer for alignment
    if st.button("⚙️ Setup", type="secondary"):
        configure_simulation()

# Simulation Container
sim_container = st.empty()
stats_container = st.empty()

# Main Logic
# Initialize with VOID if not present
if 'game' not in st.session_state:
    # Empty void init
    st.session_state.game = GameEngine(100, 100, 0.1)
    # Force grid to zeros (Void)
    st.session_state.game.grid = np.zeros((100, 100), dtype=int)
    st.session_state.game.display_grid = np.zeros((100, 100), dtype=float)

# Run Logic
if 'run_sim' in st.session_state and st.session_state.run_sim:
    # Retrieve latest params
    p = st.session_state.params
    
    # Re-init game with new params
    st.session_state.game = GameEngine(p['width'], p['height'], p['decay'])
    st.session_state.game.randomize(p['prob'])
    
    progress_bar = st.progress(0)
    step_delay = 1.0 / p['speed']
    
    # Run Simulation Loop
    for i in range(p['duration']):
        st.session_state.game.step()
        
        # Render
        img = grid_to_image(st.session_state.game.display_grid, p['colormap'])
        sim_container.image(img, caption=f"Generation: {st.session_state.game.step_count}", use_container_width=True, output_format="JPEG")
        
        progress_bar.progress((i + 1) / p['duration'])
        time.sleep(step_delay)
    
    # Analysis
    history = st.session_state.game.get_full_history()
    analysis = analyze_simulation(history)
    
    st.session_state.run_sim = False # Stop running
    st.session_state.last_analysis = analysis
    st.rerun() # Rerun to show analysis dialog cleanly

# Rendering Idle/Finished State
p = st.session_state.params
img = grid_to_image(st.session_state.game.display_grid, p['colormap'])

if 'last_analysis' in st.session_state and not st.session_state.get('run_sim', False):
    sim_container.image(img, caption="Simulation Ended", use_container_width=True)
    show_analysis(st.session_state.last_analysis)
    # Clear analysis so it doesn't pop up on refresh
    del st.session_state['last_analysis']
else:
    sim_container.image(img, caption="Waiting for Sequence Initialization...", use_container_width=True)


