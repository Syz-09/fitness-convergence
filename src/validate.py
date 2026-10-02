import pandas as pd

ALIASES = {
    "video_id": ["video_id", "video id"],
    "title": ["title", "video_title", "video title"],
    "country": ["country", "region", "country_code"],
    "views": ["views", "view_count", "view count"],
    "likes": ["likes", "like_count", "like count"],
    "comments": ["comments", "comment_count", "comment count"],
    "publish_time": ["publish_time", "published_at", "publish date", "published date"],
}


def normalized_columns(df):
    return {str(c).strip().lower(): c for c in df.columns}


def match_column(df, canonical):
    cols = normalized_columns(df)
    for a in ALIASES[canonical]:
        if a in cols:
            return cols[a]
    return None


def validate_frame(df, name="data"):
    found = {k: match_column(df, k) for k in ALIASES}
    required = ["title", "views", "likes", "comments"]
    missing = [k for k in required if found[k] is None]
    if missing:
        raise ValueError(f"{name}: missing required columns {missing}; columns={list(df.columns)}")
    return found


def validate_files(paths):
    report = []
    for p in paths:
        df = pd.read_csv(p, nrows=200)
        found = validate_frame(df, str(p))
        report.append({"file": str(p), "rows_checked": len(df), **{f"col_{k}": v for k,v in found.items()}})
    return pd.DataFrame(report)
