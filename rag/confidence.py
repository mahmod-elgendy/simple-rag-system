import numpy as np

def compute_confidence(results):
    scores = [r["score"] for r in results]
    return round(float(np.mean(scores)), 3)
