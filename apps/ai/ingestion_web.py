import re, math
from pathlib import Path
import httpx
from trafilatura import extract
from urllib.parse import urlparse
from django.utils.text import slugify

AI_ROOT = Path("ai_data")
TXT_DIR  = AI_ROOT / "web_txt"
TXT_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = "PI4-HospitalBot/1.0 (+for academic demo)"
MAX_BYTES = 2_000_000   # ~2MB por página (limite de segurança)
CHUNK_CHARS = 1200      # ~800-1000 tokens em PT (ajuste se quiser)

def _respect_domain(url: str):
    # exemplo simples: bloqueia schemas não http(s)
    p = urlparse(url)
    if p.scheme not in {"http", "https"}:
        raise ValueError("URL não suportada (apenas http/https).")

def fetch_html(url: str) -> str:
    _respect_domain(url)
    with httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=30.0, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        if len(r.content) > MAX_BYTES:
            raise ValueError("Página muito grande (limite 2MB).")
        return r.text

def extract_main_text(html: str) -> str:
    # trafilatura extrai conteúdo "principal" do artigo
    text = extract(html, include_links=False, include_formatting=False, favor_recall=True)
    if not text:
        # fallback ingênuo: remove tags grosseiramente
        text = re.sub(r"<[^>]+>", " ", html)
    # limpeza básica
    text = re.sub(r"\s+\n", "\n", text).strip()
    return text

def chunk_text(text: str, chunk_chars: int = CHUNK_CHARS):
    # corta em blocos com sobreposição suave
    overlap = int(chunk_chars * 0.15)
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+chunk_chars]
        chunks.append(chunk.strip())
        i += (chunk_chars - overlap)
    return [c for c in chunks if c]

def save_txt_chunks(url: str, title: str | None, chunks: list[str]) -> list[Path]:
    domain = urlparse(url).netloc
    base = slugify((title or "")[:60]) or slugify(domain)
    paths = []
    for idx, c in enumerate(chunks, start=1):
        p = TXT_DIR / f"{base}-{idx:03d}.txt"
        p.write_text(c, encoding="utf-8")
        paths.append(p)
    return paths

def ingest_url_to_txt(url: str) -> list[Path]:
    html = fetch_html(url)
    text = extract_main_text(html)
    if not text or len(text) < 300:
        raise ValueError("Conteúdo muito curto para indexar.")
    # título simples: pega 1ª linha não vazia
    title = next((ln.strip() for ln in text.splitlines() if ln.strip()), None)
    chunks = chunk_text(text)
    return save_txt_chunks(url, title, chunks)
