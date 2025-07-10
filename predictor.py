import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import json
import os

HISTORY_FILE = 'history.json'

class Predictor:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.history = self.load_history()
        self.is_trained = False
        self.train_model()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_record(self, match_id, features, result):
        self.history[match_id] = {'features': features, 'result': result}
        self.save_history()
        self.train_model()

    def train_model(self):
        if not self.history:
            return
        X = []
        y = []
        for rec in self.history.values():
            X.append(rec['features'])
            y.append(rec['result'])
        if len(X) > 5:  # Минимум данных для обучения
            self.model.fit(X, y)
            self.is_trained = True

    def predict(self, features):
        if not self.is_trained:
            return []
        proba = self.model.predict_proba([features])[0]
        classes = self.model.classes_
        predictions = list(zip(classes, proba))
        predictions.sort(key=lambda x: x[1], reverse=True)
        return predictions[:3]  # Топ 3 прогноза
