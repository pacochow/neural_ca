import torch   
from src.standard_ca import *
from src.grid import *
from helpers.visualizer import create_animation

# Parameters
grid_size = 40
iterations = 400
angle = 0.0

# Load model
model = torch.load("./model_params/env_model.pt")



# Initialise grid
grid = Grid(grid_size, model.model_channels)

# Initialise environment
env = grid.init_env(model.env_channels)
env = grid.add_env(env, "linear")

# Run model
state_history = grid.run(model, iterations, destroy_type = 0, destroy = True, angle = angle, env = env)

# Create animation
nSeconds = 10
filename = './media/env_run_regenerate.mp4'
create_animation(state_history, iterations, nSeconds, filename)