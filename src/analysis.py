import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
import torch
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def plot_parameter_sizes(model_name: str, filename: str):

    model = torch.load(f"./models/{model_name}/final_weights.pt")
    
    # Get parameters
    params = [x.data for x in model.parameters()]
    
    # Average over all weights for each channel to give array of length num_channels
    weights = np.abs(params[2][:, :, 0, 0].mean(dim = 1).numpy())

    # Categories and numbers
    categories = list(range(1, model.model_channels+1))

    # Bar chart
    x = np.arange(len(categories))  # Label locations

    fig, ax = plt.subplots()
    rects = ax.bar(x[:model.model_channels], weights[:model.model_channels], label='Model channels')

    # Special label for the last category
    if model.env_channels > 0 and model.env_output == True:
        rects_last = ax.bar(x[-1], weights[-1], label='Environment channel')

    # Add some text for labels, title and custom x-axis tick labels
    ax.set_ylabel('Parameter size', fontsize = 13)
    ax.set_xlabel('Channels', fontsize = 13)
    ax.set_title('Mean size of parameters for each channel', fontsize = 16)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation = 0)
    ax.legend()

    plt.savefig(filename)
    plt.show()

def cluster_hidden_units(model: nn.Module, filename: str = None):
    
    """
    Perform PCA on weights of each hidden unit and cluster 
    """

    params = [i for i in model.parameters()]
    X = params[0].squeeze(-2, -1).detach().numpy()


    # assume X is your data

    # Apply PCA for dimensionality reduction (optional)
    pca = PCA(n_components=30);  # or another number less than 54
    X_pca = pca.fit_transform(X)

    # Create a kmeans model
    kmeans = KMeans(n_clusters=2); # you can change the number of clusters
    kmeans.fit(X_pca)

    # Get the cluster assignments for each data point
    clusters = kmeans.predict(X_pca)


    plt.figure(figsize=(10, 7))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis')

    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.title('Visualization of clustered data', fontweight='bold')
    plt.colorbar()
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    
    return clusters, X_pca

def find_hox_units(hidden_unit_history: dict, early: bool = True) -> np.ndarray:
    
    """
    Takes in dictionary of hidden unit histories as input. Set early = True to find early hox genes.
    Returns array of hidden unit indices sorted from most hox-like to least.
    """

    # Get temporal profiles across all pixels
    temporal_profiles = sum(list(hidden_unit_history.values()))

    # Normalise temporal profiles
    temporal_profiles -= temporal_profiles[0]
    development_profiles = np.abs(temporal_profiles[:60])

    if early == True:
        # Find units that have highest cumulative activity before iteration 20
        early_exp = development_profiles[:20].sum(axis=0)
        early_sorted = early_exp.argsort()[::-1]
        return development_profiles, early_sorted
    else:
        
        late_exp = development_profiles[20:].sum(axis=0)
        late_sorted = late_exp.argsort()[::-1]
        return development_profiles, late_sorted
    
    
def plot_expression_profiles(development_profiles: np.ndarray, sorted_list: np.ndarray, filename: str):
    plt.figure(figsize = (10, 8))

    # Find hox genes
    for i in sorted_list[:20]:
        
        plt.plot(development_profiles[:,i]);

    plt.legend(sorted_list[:20], fontsize = 16)
    plt.xlabel("Iterations", fontsize = 18)
    plt.ylabel("Unit activity", fontsize = 18)
    plt.yticks(fontsize=18)
    plt.xticks(fontsize = 18)
    plt.axvline(20, color = 'black', linestyle = 'dashed')
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()
    
    