import numpy as np
import pandas as pd

def analyze_simulation(history):
    if not history:
        return {
            "title": "The Void",
            "description": "Nothing happened. Time stood still in an empty universe."
        }
    
    df = pd.DataFrame(history)
    start_pop = df['population'].iloc[0]
    end_pop = df['population'].iloc[-1]
    max_pop = df['population'].max()
    min_pop = df['population'].min()
    steps = len(df)
    
    # Calculate trends
    changes = df['population'].diff().fillna(0)
    volatility = changes.std()
    
    # Generate Narrative
    title = ""
    description = ""
    
    if end_pop == 0:
        title = "Total Extinction"
        description = (
            f"The civilization struggle for {steps} generations before succumbing to the harsh void. "
            "Despite reaching a peak of {max_pop} entities, resource scarcity (or perhaps loneliness) "
            "led to a complete collapse. Silence reigns once more."
        )
    elif end_pop == start_pop and volatility < 1.0:
        title = "Static Equilibrium"
        description = (
            "A remarkably stable society. Structure emerged instantly and refused to yield to time. "
            "These digital denizens found the perfect balance immediately, trapped in eternal stasis."
        )
    elif end_pop > start_pop * 1.5:
        title = "The Golden Age of Growth"
        description = (
            f"A thriving era! Starting from a humble {start_pop}, the population exploded to {end_pop}. "
            "Cooperation between cellular structures has led to a booming metropolis of automata."
        )
    elif end_pop < start_pop * 0.5:
        title = "The Great Filter"
        description = (
            f"Catastrophe. From an initial state of {start_pop}, the system degraded significantly to {end_pop}. "
            "Overpopulation in the early stages likely caused overcrowding deaths, thinning the herd to a bare minimum."
        )
    elif volatility > (start_pop * 0.1):
        title = "Chaotic Fluctuations"
        description = (
            "A turbulent history. Empires rose and fell in rapid succession. "
            f"The population swung wildly between {min_pop} and {max_pop}, indicating a highly unstable "
            "genetic configuration or a war-torn grid."
        )
    else:
        title = "Steady State Survival"
        description = (
            "Life found a way. Despite minor fluctuations, the system maintained a healthy consistence. "
            f"Ending with {end_pop} survivors, it represents a resilient, if unexciting, ecosystem."
        )
        
    return {
        "title": title,
        "description": description,
        "metrics": {
            "Peak Population": max_pop,
            "Final Population": end_pop,
            "Generations": steps,
            "Volatility Index": f"{volatility:.2f}"
        }
    }
