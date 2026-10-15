
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load the dataset
data = pd.read_csv("spam.csv")

# Check required columns
data = data.dropna(subset=["label", "message"])
data["label"] = data["label"].str.strip().str.lower()
data = data[data["label"].isin(["spam", "ham"])]

# Create the machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train the model
model.fit(data["message"], data["label"])

# Save the trained model
with open("spam_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained and saved successfully!")
