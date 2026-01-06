# Game of Life - Project Genesis 🧬

A premium, interactive cellular automaton simulation built with **Streamlit** and **NumPy**. This project offers a modernized take on Conway's Game of Life, featuring trail decay visuals, statistical narrative analysis, and a "Mission Control" interface for deep customization.

## ✨ Features

-   **High-Performance Engine**: Optimized NumPy-based grid simulation capable of running thousands of cells at high frame rates.
-   **Visuals**: 
    -   Glowing **Decay Trails** for a dynamic, biological feel.
    -   Multiple **Thermal Profiles** (Magma, Viridis, Inferno, etc.).
-   **Mission Control Dashboard**:
    -   **Detailed Configuration**: Tweak grid size, life probability, physics speed, epoch duration, and visual decay.
    -   **Run Random**: One-click chaos generator for unexpected results.
-   **Narrative Analysis**: Post-simulation reports that analyze population trends, entropy, and stability to generate unique stories about the civilization's fate (e.g., "The Great Filter", "Golden Age").
-   **Mobile Optimized**: Fully responsive interface that works great on phones and tablets.

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/JedizLaPulga/Game-of-Life.git
    cd Game-of-Life
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

Or just double-click `run_app.bat` if on Windows (after setting up the environment).

### How to Play
1.  **Start**: The simulation begins in a dormant "Void" state.
2.  **Configure**: Click the **⚙️ Setup** button in the top right.
3.  **Launch**: Adjust parameters manually and click **🚀 Initialize Sequence**, or just hit **🎲 Run Random** for a surprise.
4.  **Analyze**: Watch the civilization evolve. When the epoch ends, a report will detail the history of the world.
5.  **Rerun**: Want to see it again? Click **🔄 Rerun Simulation** in the report dialog.

## 🛠️ Tech Stack

-   **Frontend**: Streamlit
-   **Logic**: Python (NumPy for vectorization)
-   **Data Analysis**: Pandas
-   **Visualization**: Matplotlib (Colormaps)

## 📄 License

This project is open source and available under the MIT License.
