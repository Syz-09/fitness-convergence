import itertools
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .config import PROCESSED, RESULTS, TOPICS

TOPIC_COLS = list(TOPICS)


def country_summary(df):
    g = df.groupby("country")
    out = g.agg(
        videos=("title", "size"),
        fitness_videos=("fitness_related", "sum"),
        mean_views=("views", "mean"),
        mean_engagement=("engagement_rate", "mean"),
    ).reset_index()
    out["fitness_share"] = out["fitness_videos"] / out["videos"]
    out.to_csv(PROCESSED / "country_summary.csv", index=False)
    return out


def topic_profile(df):
    fit = df[df["fitness_related"] == 1].copy()
    if fit.empty:
        raise ValueError("No fitness-related videos were detected. Expand TOPICS in src/config.py.")
    prof = fit.groupby("country")[TOPIC_COLS].mean()
    prof.to_csv(PROCESSED / "topic_profile.csv")
    return prof


def similarity_matrix(profile):
    sim = pd.DataFrame(cosine_similarity(profile), index=profile.index, columns=profile.index)
    sim.to_csv(PROCESSED / "country_similarity.csv")
    return sim


def bootstrap_similarity(df, n_boot=300, random_state=42):
    rng = np.random.default_rng(random_state)
    countries = sorted(df.loc[df.fitness_related == 1, "country"].dropna().unique())
    records=[]
    for a,b in itertools.combinations(countries,2):
        da=df[(df.country==a)&(df.fitness_related==1)]
        db=df[(df.country==b)&(df.fitness_related==1)]
        if len(da)<2 or len(db)<2:
            continue
        scores=[]
        for _ in range(n_boot):
            sa=da.iloc[rng.integers(0,len(da),len(da))][TOPIC_COLS].mean().to_numpy().reshape(1,-1)
            sb=db.iloc[rng.integers(0,len(db),len(db))][TOPIC_COLS].mean().to_numpy().reshape(1,-1)
            scores.append(float(cosine_similarity(sa,sb)[0,0]))
        records.append({
            "country_a":a,"country_b":b,"n_a":len(da),"n_b":len(db),
            "mean_similarity":float(np.mean(scores)),
            "ci_low":float(np.quantile(scores,.025)),
            "ci_high":float(np.quantile(scores,.975)),
        })
    RESULTS.mkdir(parents=True, exist_ok=True)
    out=pd.DataFrame(records)
    out.to_csv(RESULTS / "bootstrap_similarity.csv",index=False)
    return out
