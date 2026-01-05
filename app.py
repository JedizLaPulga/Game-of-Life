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

# Header
st.title("🧬 Game of Life: Project Genesis")
st.caption("A cellular automaton simulation exploring the emergence of complexity.")

# Simulation Container
sim_container = st.empty()
stats_container = st.empty()

# Control Deck
with st.container():
    st.markdown("### 🎛️ Control Deck")
    
    with st.expander("Simulation Parameters", expanded=True):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.caption("🌍 World Gen")
            width = st.slider("Grid Width", 50, 200, 100)
            height = st.slider("Grid Height", 50, 200, 100)
            prob = st.slider("Life Probability", 0.0, 1.0, 0.15)
            
        with c2:
            st.caption("⏳ Time Physics")
            duration = st.slider("Epoch Duration", 10, 500, 100)
            speed = st.slider("Simulation Speed (FPS)", 1, 60, 30)
            decay = st.slider("Visual Decay", 0.01, 0.5, 0.1)
            
        with c3:
            st.caption("🎨 Optics & Action")
            colormap = st.selectbox("Thermal Profile", ["magma", "viridis", "plasma", "inferno", "ocean", "gist_earth"])
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("🚀 Initialize Sequence", type="primary", use_container_width=True):
                st.session_state.run_sim = True
                st.session_state.rerun_trigger = time.time()

# Analysis Dialog Function (Polyfill-ish)
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
            
    st.balloons()

# Main Logic
if 'game' not in st.session_state:
    st.session_state.game = GameEngine(width, height, decay)
    st.session_state.game.randomize(prob)

# Reset if dimensions changed or requested
if 'run_sim' in st.session_state and st.session_state.run_sim:
    # Re-init game with new params
    st.session_state.game = GameEngine(width, height, decay)
    st.session_state.game.randomize(prob)
    
    progress_bar = st.progress(0)
    step_delay = 1.0 / speed
    
    # Run Simulation Loop
    for i in range(duration):
        st.session_state.game.step()
        
        # Render
        img = grid_to_image(st.session_state.game.display_grid, colormap)
        
        # Upscale for verify (optional, helps blurriness if too small)
        # But st.image with use_container_width=True works well.
        
        sim_container.image(img, caption=f"Generation: {st.session_state.game.step_count}", use_container_width=True, output_format="JPEG")
        
        progress_bar.progress((i + 1) / duration)
        time.sleep(step_delay)
    
    # Analysis
    history = st.session_state.game.get_full_history()
    analysis = analyze_simulation(history)
    
    st.session_state.run_sim = False # Stop running
    st.session_state.last_analysis = analysis
    
    # Trigger Dialog
    show_analysis(analysis)

elif 'last_analysis' in st.session_state:
    # Persist the last state image
    img = grid_to_image(st.session_state.game.display_grid, colormap)
    sim_container.image(img, caption="Simulation Ended", use_container_width=True)
    
    # Option to re-open analysis
    st.info("Simulation complete. Check the Control Deck to restart.")
    with st.expander("Last Session Analysis", expanded=True):
        st.subheader(st.session_state.last_analysis['title'])
        st.write(st.session_state.last_analysis['description'])

else:
    # Idle State
    img = grid_to_image(st.session_state.game.display_grid, colormap)
    sim_container.image(img, caption="Ready to Initialize", use_container_width=True)
