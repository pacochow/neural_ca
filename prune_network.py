from helpers.helpers import *
import torch   
from src.standard_ca import *
from src.grid import *
from src.pruning import *
from helpers.visualizer import *

iterations = 400
nSeconds = 10
angle = 0.0


# Load model
model_name = 'env_circle_16_1'
model = torch.load(f"./models/{model_name}/final_weights.pt")


# Initialise grid
grid_size = model.grid_size
grid = Grid(grid_size, model.model_channels)

# Initialise environment
env = None
env = grid.init_env(model.env_channels)
env = grid.add_env(env, "circle", 0)

# Visualise progress animation
filename = f"./models/{model_name}/pruned_visualization.mp4"
visualize_pruning(model_name, grid, iterations, nSeconds, filename = filename, angle = angle, env = env)

# model_name_2 = 'env_circle_16_1'
# model2 = torch.load(f"./models/{model_name_2}/final_weights.pt")

# grid2 = Grid(grid_size, model2.model_channels)
# env2 = grid2.init_env(model2.env_channels)
# env2 = grid2.add_env(env2, "circle", 0)
# comparing_pruning_losses(model_name, grid, env, model_name_2, grid2, env2, "comparing_pruned_loss.png", iterations, angle)





# # Prune model
# percent = 23
# model_size, pruned_size, pruned_model = prune_by_percent(model, percent=percent)

# # Run model
# state_history = grid.run(pruned_model, iterations, destroy_type = 0, destroy = True, angle = angle, env = env)

# # Create animation
# filename = f"./models/{model_name}/pruned_run.mp4"
# create_animation(state_history, iterations, nSeconds, filename)