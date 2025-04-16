from sentence_transformers import SentenceTransformer
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_topic(question: str) -> str:
    # Define top human rights themes
    themes = [
        "child rights", "refugee protection", "gender equality", "freedom of speech",
        "torture", "right to education", "discrimination", "civil liberties",
        "labor rights", "access to justice", "human trafficking"
    ]
    q_emb = model.encode(question, convert_to_tensor=True)
    t_emb = model.encode(themes, convert_to_tensor=True)
    sims = torch.nn.functional.cosine_similarity(q_emb, t_emb)
    max_score = torch.max(sims)
    best_idx = torch.argmax(sims)
    
    if max_score.item() > 0.4:
        return themes[best_idx]
    return "General Rights"
