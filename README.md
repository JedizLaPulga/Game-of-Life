# Game of Life - Project Genesis

A **Streamlit** based visualization of Conway's Game of Life, featuring "Beautiful Animation" and reality-based post-simulation analysis.

## Features

- **High-Performance Engine**: NumPy-based grid simulation.
- **Visuals**: glowing trail effects and customizable heatmaps (Magma, Inferno, etc.).
- **Interactive Control**: Tweak simulation speed, duration, grid size, and decay rates.
- **Narrative Analysis**: After each run, the system analyzes population trends, volatility, and entropy to generate a "story" about the civilization's fate (e.g., "The Great Filter", "Golden Age").

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
streamlit run app.py
```

## Structure

- `app.py`: Main application UI and loop.
- `game_engine.py`: Core logic with decay/trail features.
- `analysis.py`: Statistical analysis and narrative generator.
