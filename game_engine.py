import numpy as np

class GameEngine:
    def __init__(self, width=100, height=100, decay_rate=0.1):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=int)
        self.display_grid = np.zeros((width, height), dtype=float)
        self.decay_rate = decay_rate
        self.history = []
        self.step_count = 0

    def randomize(self, probability=0.2):
        """Randomize the grid with a given probability of live cells."""
        self.grid = (np.random.random((self.width, self.height)) < probability).astype(int)
        self.display_grid = self.grid.astype(float)
        self.history = []
        self.step_count = 0

    def step(self):
        """Evolve the grid by one step."""
        # Count neighbors using 2D convolution via rolling
        # Roll allows us to sum up neighbors efficiently without a loop
        # N, S, E, W, NE, NW, SE, SW
        neighbors = (
            np.roll(self.grid, 1, axis=0) + 
            np.roll(self.grid, -1, axis=0) + 
            np.roll(self.grid, 1, axis=1) + 
            np.roll(self.grid, -1, axis=1) + 
            np.roll(self.grid, 1, axis=0) + np.roll(np.roll(self.grid, 1, axis=0), 1, axis=1) + # Wait, diagonal logic needs care
            np.roll(np.roll(self.grid, 1, axis=0), -1, axis=1) +
            np.roll(np.roll(self.grid, -1, axis=0), 1, axis=1) +
            np.roll(np.roll(self.grid, -1, axis=0), -1, axis=1)
        )
        
        # Actually easier to use scipy.signal.convolve2d but avoiding scipy import in engine for raw speed if numpy suffices.
        # Let's simple check sum of 8 neighbors.
        # Shift approach:
        # Padded version? Toroidal (wrap-around) is standard for display.
        
        shifted_grids = [
            np.roll(np.roll(self.grid, i, axis=0), j, axis=1)
            for i in (-1, 0, 1) for j in (-1, 0, 1)
            if (i != 0 or j != 0)
        ]
        
        neighbors = sum(shifted_grids)

        # Game of Life Rules
        # 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # 2. Any live cell with two or three live neighbours lives on to the next generation.
        # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        
        new_grid = (neighbors == 3) | ((self.grid == 1) & (neighbors == 2))
        self.grid = new_grid.astype(int)
        self.step_count += 1
        
        # Update display grid (decay effect)
        # Verify where cells are alive, set to 1. Where dead, decrease by decay_rate.
        self.display_grid = np.where(self.grid == 1, 1.0, np.maximum(0, self.display_grid - self.decay_rate))
        
        # Record stats
        self._record_history()

    def _record_history(self):
        population = np.sum(self.grid)
        self.history.append({
            "step": self.step_count,
            "population": int(population),
            "entropy": self._calculate_entropy()
        })

    def _calculate_entropy(self):
        # A simple spatial entropy approximation
        return float(np.std(self.grid))

    def get_stats(self):
        if not self.history:
            return {}
        return self.history[-1]

    def get_full_history(self):
        return self.history
