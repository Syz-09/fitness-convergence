import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score, confusion_matrix
from .config import RESULTS


def train_engagement_model(df, random_state=42):
    data=df.copy()
    if len(data) < 20:
        metrics={"status":"skipped","reason":"fewer than 20 usable rows"}
    else:
        # Define high engagement relative to the country's own median, reducing scale differences.
        med=data.groupby("country")["engagement_rate"].transform("median")
        data["high_engagement"]=(data["engagement_rate"]>med).astype(int)
        features=["country","fitness_related","title_length","title_words"]
        X=data[features]
        y=data["high_engagement"]
        if y.nunique()<2 or y.value_counts().min()<3:
            metrics={"status":"skipped","reason":"target classes are too small"}
        else:
            Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.3,random_state=random_state,stratify=y)
            pre=ColumnTransformer([
                ("country",OneHotEncoder(handle_unknown="ignore"),["country"]),
                ("num",StandardScaler(),["fitness_related","title_length","title_words"]),
            ])
            model=Pipeline([("pre",pre),("clf",LogisticRegression(max_iter=1000))])
            model.fit(Xtr,ytr)
            pred=model.predict(Xte)
            prob=model.predict_proba(Xte)[:,1]
            metrics={
                "status":"ok",
                "n_train":int(len(Xtr)),"n_test":int(len(Xte)),
                "accuracy":float(accuracy_score(yte,pred)),
                "balanced_accuracy":float(balanced_accuracy_score(yte,pred)),
                "roc_auc":float(roc_auc_score(yte,prob)),
                "confusion_matrix":confusion_matrix(yte,pred).tolist(),
                "note":"Exploratory model only; high engagement is defined relative to each country's median."
            }
    RESULTS.mkdir(parents=True,exist_ok=True)
    (RESULTS/"model_metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    return metrics
