import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

# Constants
GRID_SIZE = 10
PLANT, HERBIVORE, CARNIVORE = "Plant", "Herbivore", "Carnivore"
SEASONS = ["Spring", "Summer", "Autumn", "Winter"]
CLIMATE_EFFECTS = {"Spring": 1.2, "Summer": 1.5, "Autumn": 1.0, "Winter": 0.5}

# Organism Class
class Organism:
    def __init__(self, type, energy):
        self.type = type
        self.energy = energy

# Ecosystem Class
class Ecosystem:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.current_season_index = 0
        self.population_stats = []  # Track population over time

    def has_living_organisms(self):
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    return True
        return False

    def get_population_counts(self):
        plant_count = sum(1 for x in range(self.size) for y in range(self.size)
                          if self.grid[x][y] and self.grid[x][y].type == PLANT)
        herbivore_count = sum(1 for x in range(self.size) for y in range(self.size)
                              if self.grid[x][y] and self.grid[x][y].type == HERBIVORE)
        carnivore_count = sum(1 for x in range(self.size) for y in range(self.size)
                              if self.grid[x][y] and self.grid[x][y].type == CARNIVORE)
        return plant_count, herbivore_count, carnivore_count

    def populate(self, num_plants, num_herbivores, num_carnivores):
        all_positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        random.shuffle(all_positions)
        for _ in range(num_plants):
            x, y = all_positions.pop()
            self.grid[x][y] = Organism(PLANT, energy=5)
        for _ in range(num_herbivores):
            x, y = all_positions.pop()
            self.grid[x][y] = Organism(HERBIVORE, energy=5)
        for _ in range(num_carnivores):
            x, y = all_positions.pop()
            self.grid[x][y] = Organism(CARNIVORE, energy=5)

    def apply_seasonal_effects(self):
        current_season = SEASONS[self.current_season_index]
        growth_rate = CLIMATE_EFFECTS[current_season]

        # Plants grow more or less depending on the season
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] is None and random.random() < 0.1 * growth_rate:
                    self.grid[x][y] = Organism(PLANT, energy=5)

    def update_season(self):
        self.current_season_index = (self.current_season_index + 1) % len(SEASONS)

    def track_population(self):
        self.population_stats.append(self.get_population_counts())

    def update(self):
        # Apply seasonal growth effects
        self.apply_seasonal_effects()

        # Progress to the next season
        if random.random() < 0.1:  # Change season every few turns
            self.update_season()

        # Track population statistics
        self.track_population()

# Visualization Functions
def visualize_simulation(ecosystem):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    grid_data = np.zeros((GRID_SIZE, GRID_SIZE))

    def update_frame(frame):
        if not ecosystem.has_living_organisms():
            ani.event_source.stop()  # Stop animation if all organisms are dead
            return

        # Update the ecosystem for one turn
        ecosystem.update()

        # Update grid visualization with the colors representing different organisms
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if ecosystem.grid[x][y] is None:
                    grid_data[x, y] = 0  # Empty cell (black)
                elif ecosystem.grid[x][y].type == PLANT:
                    grid_data[x, y] = 1  # Plants are green
                elif ecosystem.grid[x][y].type == HERBIVORE:
                    grid_data[x, y] = 2  # Herbivores are blue
                elif ecosystem.grid[x][y].type == CARNIVORE:
                    grid_data[x, y] = 3  # Carnivores are red
        ax1.clear()
        ax1.imshow(grid_data, cmap="viridis", vmin=0, vmax=3)
        current_season = SEASONS[ecosystem.current_season_index]
        ax1.set_title(f"Ecosystem Grid (Season: {current_season})")

        # Update population chart
        ax2.clear()
        turns = range(len(ecosystem.population_stats))
        populations = list(zip(*ecosystem.population_stats))
        ax2.plot(turns, populations[0], label="Plants", color="green")
        ax2.plot(turns, populations[1], label="Herbivores", color="blue")
        ax2.plot(turns, populations[2], label="Carnivores", color="red")
        ax2.set_title("Population Trends")
        ax2.set_xlabel("Turns")
        ax2.set_ylabel("Population")
        ax2.legend()

    # Animate
    ani = animation.FuncAnimation(fig, update_frame, interval=500)
    plt.show()

# Run the Simulation
ecosystem = Ecosystem(GRID_SIZE)
ecosystem.populate(30, 10, 5)  # 30 plants, 10 herbivores, 5 carnivores
visualize_simulation(ecosystem)
