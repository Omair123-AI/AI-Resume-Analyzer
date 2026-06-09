"""
keyword_extractor.py - Extract ONLY real technical keywords using whitelist approach.
Instead of blacklisting bad words, we ONLY keep words that are actual tech terms.
"""
import re
from collections import Counter
from utils.constants import ALL_SKILLS

# Supplementary tech terms not in skills.csv but valid keywords
EXTRA_TECH_TERMS = {
    "opencv", "matplotlib", "seaborn", "beautifulsoup", "selenium",
    "scrapy", "celery", "redis", "nginx", "gunicorn", "uvicorn",
    "pydantic", "sqlalchemy", "alembic", "pytest", "jest", "webpack",
    "babel", "eslint", "prettier", "vite", "parcel", "rollup",
    "storybook", "cypress", "playwright", "puppeteer", "axios",
    "zustand", "mobx", "recoil", "swr", "tanstack", "prisma",
    "drizzle", "typeorm", "sequelize", "mongoose", "motor",
    "asyncio", "multiprocessing", "threading", "subprocess",
    "requests", "httpx", "aiohttp", "websocket", "grpc", "protobuf",
    "graphql", "apollo", "relay", "urql", "trpc",
    "opencv", "pillow", "imageio", "torchvision", "albumentations",
    "xgboost", "lightgbm", "catboost", "optuna", "mlflow", "dvc",
    "airflow", "prefect", "dagster", "dbt", "great", "expectations",
    "spark", "kafka", "flink", "hadoop", "hive", "presto", "trino",
    "elasticsearch", "opensearch", "solr", "lucene", "pinecone",
    "weaviate", "chroma", "qdrant", "milvus", "faiss",
    "streamlit", "gradio", "dash", "plotly", "bokeh", "altair",
    "networkx", "igraph", "gephi", "d3js", "chartjs", "recharts",
    "threejs", "webgl", "babylon", "unity", "unreal", "godot",
    "ffmpeg", "gstreamer", "mediapipe", "dlib", "face", "recognition",
    "tesseract", "paddleocr", "easyocr", "layoutlm", "donut",
    "fasttext", "word2vec", "glove", "spacy", "nltk", "gensim",
    "transformers", "tokenizers", "datasets", "evaluate", "peft",
    "deepspeed", "accelerate", "bitsandbytes", "vllm", "ollama",
    "llamaindex", "langchain", "langgraph", "crewai", "autogen",
    "microservice", "monolith", "serverless", "lambda", "functions",
    "webhook", "oauth", "openid", "saml", "ldap", "keycloak",
    "nginx", "caddy", "traefik", "istio", "envoy", "consul",
    "prometheus", "grafana", "datadog", "newrelic", "sentry",
    "cloudwatch", "logstash", "kibana", "fluentd", "jaeger",
    "ansible", "puppet", "chef", "saltstack", "vagrant",
    "virtualbox", "vmware", "hyper", "proxmox", "esxi",
    "raspberrypi", "arduino", "embedded", "firmware", "rtos",
    "mqtt", "coap", "zigbee", "bluetooth", "lorawan",
}


def extract_keywords(text: str, top_n: int = 25) -> list:
    """
    Whitelist approach: only return words that are actual tech terms.
    Uses skills dataset + extra tech terms as the allowed vocabulary.
    """
    # Clean text — remove URLs, emails, phone numbers, names
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    text = re.sub(r"\b\d[\d\s\-().]{5,}\d\b", " ", text)
    text = re.sub(r"github\.com/\S*", " ", text, flags=re.I)
    text = re.sub(r"linkedin\.com/\S*", " ", text, flags=re.I)

    text_lower = text.lower()

    # Build allowed vocab = ALL_SKILLS + EXTRA_TECH_TERMS
    allowed_vocab = set(s.lower() for s in ALL_SKILLS) | EXTRA_TECH_TERMS

    found_terms = []

    # Match multi-word tech terms first (e.g. "machine learning", "deep learning")
    for term in sorted(allowed_vocab, key=len, reverse=True):
        if len(term) < 3:
            continue
        pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
        matches = re.findall(pattern, text_lower)
        if matches:
            found_terms.extend([term] * len(matches))

    # Count occurrences
    counts = Counter(found_terms)

    # Score by frequency × specificity (longer terms = more specific)
    scored = {
        term: count * (1 + len(term) * 0.06)
        for term, count in counts.items()
    }

    # Sort and deduplicate
    sorted_terms = sorted(scored.items(), key=lambda x: x[1], reverse=True)

    # Format nicely using display case from skill_extractor
    from nlp.skill_extractor import _to_display_case
    result = []
    seen = set()
    for term, _ in sorted_terms:
        display = _to_display_case(term)
        if display.lower() not in seen:
            seen.add(display.lower())
            result.append(display)
        if len(result) >= top_n:
            break

    return result
