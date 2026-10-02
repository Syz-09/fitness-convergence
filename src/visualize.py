import numpy as np
import matplotlib.pyplot as plt
from .config import FIGURES


def save_country_share(summary):
    FIGURES.mkdir(parents=True,exist_ok=True)
    s=summary.sort_values("fitness_share")
    fig,ax=plt.subplots(figsize=(7,4))
    ax.barh(s["country"],s["fitness_share"])
    ax.set_xlabel("Fitness-related share")
    ax.set_ylabel("Country")
    ax.set_title("Fitness-related share among trending videos")
    fig.tight_layout(); fig.savefig(FIGURES/"fitness_share.png",dpi=160); plt.close(fig)


def save_topic_profile(profile):
    FIGURES.mkdir(parents=True,exist_ok=True)
    ax=profile.plot(kind="bar",figsize=(8,4))
    ax.set_ylabel("Share within fitness-related videos")
    ax.set_title("Fitness topic profile by country")
    ax.legend(title="Topic")
    fig=ax.get_figure(); fig.tight_layout(); fig.savefig(FIGURES/"topic_profile.png",dpi=160); plt.close(fig)


def save_similarity(sim):
    FIGURES.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(5,4))
    im=ax.imshow(sim.values,vmin=0,vmax=1,cmap="viridis")
    ax.set_xticks(range(len(sim.columns)),sim.columns)
    ax.set_yticks(range(len(sim.index)),sim.index)
    for i in range(len(sim.index)):
        for j in range(len(sim.columns)):
            ax.text(j,i,f"{sim.iloc[i,j]:.2f}",ha="center",va="center",color="white" if sim.iloc[i,j]<.6 else "black")
    ax.set_title("Cosine similarity of fitness topic profiles")
    fig.colorbar(im,ax=ax,label="Cosine similarity")
    fig.tight_layout(); fig.savefig(FIGURES/"country_similarity.png",dpi=160); plt.close(fig)
