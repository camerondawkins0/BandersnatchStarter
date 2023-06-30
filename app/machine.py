from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

import joblib
import pytz


class Machine:

    def __init__(self, df: DataFrame):
        self.name = "Random Forest"
        self.model = RandomForestClassifier(n_estimators=200,
                                            max_depth=25,
                                            min_samples_split=2,
                                            n_jobs=-1,
                                            random_state=42)
        self.timestamp = datetime.now(
            pytz.timezone('US/Pacific')
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.target = "Rarity"

        self.X = df.drop(columns=self.target)
        self.y = df[self.target]

        self.model.fit(self.X, self.y)

    def __call__(self, feature_basis: DataFrame):
        prediction, *_ = self.model.predict(feature_basis)
        confidence = self.model.predict_proba(feature_basis).max()
        return prediction, confidence

    def save(self, filepath):
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath):
        model = joblib.load(filepath)
        return model

    def info(self):
        print(f'Model:{self.name}')
        print(f'Model Initialization Timestamp: {self.timestamp}')
