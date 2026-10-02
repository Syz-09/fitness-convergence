from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"

SOURCE_REPO = "https://github.com/DataWithAkaasha/youtube-trending-mini-project.git"

TOPICS = {
    "workout": [
        "workout", "gym", "fitness", "training", "exercise", "cardio",
        "strength", "abs", "squat", "push up", "pushup", "running"
    ],
    "body": [
        "weight loss", "lose weight", "fat loss", "slim", "muscle",
        "bodybuilding", "six pack", "body transformation", "burn fat"
    ],
    "nutrition": [
        "protein", "creatine", "supplement", "diet", "meal prep",
        "calorie", "nutrition", "healthy food"
    ],
    "wellness": [
        "yoga", "pilates", "stretch", "meditation", "wellness", "mobility"
    ],
}
