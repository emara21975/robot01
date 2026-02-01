import os
import pickle
import numpy as np

# Directory to store face embeddings
# Adjust base path if needed
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES_DIR = os.path.join(BASE_DIR, "faces")

def ensure_faces_dir():
    if not os.path.exists(FACES_DIR):
        os.makedirs(FACES_DIR)

def load_faces():
    """
    Load all face embeddings from the faces directory.
    Returns a dict: {name: embedding}
    """
    ensure_faces_dir()
    db = {}
    
    try:
        for file in os.listdir(FACES_DIR):
            if file.endswith(".pkl"):
                name = file.replace(".pkl", "")
                path = os.path.join(FACES_DIR, file)
                try:
                    with open(path, "rb") as f:
                        embedding = pickle.load(f)
                        if embedding is not None:
                            db[name] = embedding
                except Exception as e:
                    print(f"Error loading face {file}: {e}")
    except Exception as e:
        print(f"Error accessing faces directory: {e}")
        
    return db

def save_face(name, embedding):
    """Save a face embedding to disk."""
    ensure_faces_dir()
    path = os.path.join(FACES_DIR, f"{name}.pkl")
    with open(path, "wb") as f:
        pickle.dump(embedding, f)
    print(f"Saved face for {name}")

def match_face(target_embedding, db, threshold=0.5):
    """
    Find the best match for the target embedding in the database.
    Returns (name, score).
    """
    best_name = "Unknown" # "غير معروف"
    best_score = 0.0

    if target_embedding is None or len(db) == 0:
        return best_name, best_score

    # Normalize target once
    target_norm = np.linalg.norm(target_embedding)
    if target_norm == 0:
        return best_name, 0.0

    for name, ref_embedding in db.items():
        ref_norm = np.linalg.norm(ref_embedding)
        if ref_norm == 0:
            continue
            
        # Cosine Similarity
        score = np.dot(target_embedding, ref_embedding) / (target_norm * ref_norm)
        
        if score > best_score:
            best_score = score
            best_name = name

    if best_score >= threshold:
        return best_name, best_score
    else:
        return "Unknown", best_score
