import faiss, os, numpy as np
from pathlib import Path
from .embeddings import embed

AI_ROOT = Path("ai_data")
TXT_DIRS = [AI_ROOT / "textos", AI_ROOT / "web_txt"]
IDX_DIR  = AI_ROOT / "index"
IDX_DIR.mkdir(parents=True, exist_ok=True)

EMB_FILE = IDX_DIR / "embeddings.npy"
MAP_FILE = IDX_DIR / "map.txt"

class SimpleIndex:
    def __init__(self):
        self.index = None
        self.texts = []

    def build(self, texts, embs: np.ndarray | None = None):
        self.texts = texts
        X = embs if embs is not None else embed(texts)
        self.index = faiss.IndexFlatIP(X.shape[1])
        self.index.add(X)

    def search(self, query, k=3):
        q = embed([query])
        D, I = self.index.search(q, k)
        return [(float(D[0][i]), self.texts[I[0][i]]) for i in range(min(k, len(self.texts)))]

def _load_all_texts():
    texts = []
    for d in TXT_DIRS:
        if d.exists():
            for p in d.glob("*.txt"):
                t = p.read_text(encoding="utf-8").strip()
                if t:
                    texts.append(t)
    if not texts:
        texts = [
            "Paracetamol: analgésico/antipirético; possíveis náuseas, rash.",
            "Ibuprofeno: AINE; risco GI; evitar em insuficiência renal.",
            "Amoxicilina: antibiótico; interação com anticoagulantes; alergia à penicilina."
        ]
    return texts

def _load_cached():
    if EMB_FILE.exists() and MAP_FILE.exists():
        embs = np.load(EMB_FILE)
        texts = MAP_FILE.read_text(encoding="utf-8").split("\n")
        texts = [t for t in texts if t.strip()]
        if len(texts) == embs.shape[0]:
            return texts, embs
    return None, None

def _save_cache(texts, embs):
    np.save(EMB_FILE, embs)
    MAP_FILE.write_text("\n".join(texts), encoding="utf-8")

_IDX = None

def ensure_index_loaded(force_rebuild=False):
    global _IDX
    if force_rebuild or _IDX is None:
        texts = _load_all_texts()
        if not force_rebuild:
            cached_texts, cached_embs = _load_cached()
        else:
            cached_texts, cached_embs = (None, None)
        if cached_texts is not None and cached_texts == texts:
            embs = cached_embs
        else:
            embs = embed(texts)
            _save_cache(texts, embs)
        idx = SimpleIndex()
        idx.build(texts, embs)
        _IDX = idx

def answer(query: str):
    ensure_index_loaded()
    top = _IDX.search(query, k=3)
    bullets = "\n- ".join(t for _, t in top)
    return f"Resposta baseada em trechos:\n- {bullets}"

def rebuild_index():
    ensure_index_loaded(force_rebuild=True)
    return len(_IDX.texts)
