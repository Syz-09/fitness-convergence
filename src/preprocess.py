from pathlib import Path
import re
import pandas as pd
import numpy as np
from .validate import validate_frame
from .config import TOPICS, PROCESSED

COUNTRY_HINTS = {
    "pakistan": "PK", "pak": "PK", "pk": "PK",
    "india": "IN", "ind": "IN", "in": "IN",
    "germany": "DE", "deutsch": "DE", "de": "DE",
}


def infer_country_from_path(path):
    text = str(path).lower().replace("_", " ").replace("-", " ")
    tokens = re.findall(r"[a-z]+", text)
    joined = " ".join(tokens)
    for key, code in COUNTRY_HINTS.items():
        if key in tokens or key in joined:
            return code
    return None


def _first_existing(df, found, key):
    c = found.get(key)
    if c is None:
        return pd.Series([np.nan] * len(df), index=df.index)
    return df[c]


def normalize_one(path):
    df = pd.read_csv(path)
    found = validate_frame(df, str(path))
    out = pd.DataFrame()
    out["video_id"] = _first_existing(df, found, "video_id").astype(str)
    out["title"] = _first_existing(df, found, "title").fillna("").astype(str)
    out["views"] = pd.to_numeric(_first_existing(df, found, "views"), errors="coerce")
    out["likes"] = pd.to_numeric(_first_existing(df, found, "likes"), errors="coerce")
    out["comments"] = pd.to_numeric(_first_existing(df, found, "comments"), errors="coerce")
    out["publish_time"] = pd.to_datetime(_first_existing(df, found, "publish_time"), errors="coerce", utc=True)
    if found.get("country") is not None:
        out["country"] = df[found["country"]].astype(str).str.upper().str.strip()
    else:
        out["country"] = infer_country_from_path(path)
    out["source_file"] = Path(path).name
    return out


def label_topics(title):
    text = title.lower()
    labels = {}
    for topic, words in TOPICS.items():
        labels[topic] = int(any(w in text for w in words))
    labels["fitness_related"] = int(any(labels.values()))
    return labels


def preprocess_files(paths):
    frames = [normalize_one(p) for p in paths]
    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["views", "likes", "comments"])
    df = df[(df["views"] > 0) & (df["likes"] >= 0) & (df["comments"] >= 0)].copy()
    # Trending snapshots can repeat the same video. Keep one observation per country/video/title.
    dedup_key = ["country", "video_id", "title"]
    df = df.drop_duplicates(subset=dedup_key, keep="last")
    labels = df["title"].apply(label_topics).apply(pd.Series)
    df = pd.concat([df.reset_index(drop=True), labels.reset_index(drop=True)], axis=1)
    df["engagement_rate"] = (df["likes"] + df["comments"]) / df["views"]
    df["title_length"] = df["title"].str.len()
    df["title_words"] = df["title"].str.split().str.len()
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "videos_clean.csv", index=False)
    return df
