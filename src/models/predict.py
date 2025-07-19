import joblib

def load_model(path="models/fraud_model.pkl"):

    return joblib.load(path)

def predict_instance(model, X):

    return model.predict(X), model.predict_proba(X)
