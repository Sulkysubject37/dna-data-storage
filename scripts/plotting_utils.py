import matplotlib.pyplot as plt
import os

def setup_plot(title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.7)
    return fig, ax

def save_plot(fig, output_path):
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")
    plt.close(fig)
