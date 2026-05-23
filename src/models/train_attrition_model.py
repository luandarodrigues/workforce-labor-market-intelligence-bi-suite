from __future__ import annotations

from sklearn.linear_model import LogisticRegression


def train_baseline_model(features, target):
    model = LogisticRegression(max_iter=1000)
    model.fit(features, target)
    return model
