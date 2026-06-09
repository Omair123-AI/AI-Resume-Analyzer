"""
skill_extractor.py - Match resume text against the full skills dataset
"""
import re
import pandas as pd
import os

# Load original casing from CSV once at startup
_SKILL_DISPLAY = {}

def _load_display_map():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset", "skills.csv")
    df   = pd.read_csv(path)
    return {row["skill"].lower().strip(): row["skill"].strip() for _, row in df.iterrows()}

_SKILL_DISPLAY = _load_display_map()

# Override map for skills that need special casing
SPECIAL_CASES = {
    "nlp":                    "NLP",
    "llm":                    "LLM",
    "sql":                    "SQL",
    "nosql":                  "NoSQL",
    "css":                    "CSS",
    "html":                   "HTML",
    "api":                    "API",
    "rest api":               "REST API",
    "oop":                    "OOP",
    "jwt":                    "JWT",
    "aws":                    "AWS",
    "gcp":                    "GCP",
    "ci/cd":                  "CI/CD",
    "vs code":                "VS Code",
    "github":                 "GitHub",
    "gitlab":                 "GitLab",
    "node.js":                "Node.js",
    "next.js":                "Next.js",
    "vue.js":                 "Vue.js",
    "express.js":             "Express.js",
    "react native":           "React Native",
    "tailwind css":           "Tailwind CSS",
    "material ui":            "Material UI",
    "shadcn ui":              "Shadcn UI",
    "mlops":                  "MLOps",
    "devops":                 "DevOps",
    "pytorch":                "PyTorch",
    "tensorflow":             "TensorFlow",
    "scikit-learn":           "Scikit-learn",
    "opencv":                 "OpenCV",
    "fastapi":                "FastAPI",
    "mongodb":                "MongoDB",
    "postgresql":             "PostgreSQL",
    "graphql":                "GraphQL",
    "grpc":                   "gRPC",
    "rag":                    "RAG",
    "bert":                   "BERT",
    "yolo":                   "YOLO",
    "cuda":                   "CUDA",
    "etl":                    "ETL",
    "openai api":             "OpenAI API",
    "gemini api":             "Gemini API",
    "langchain":              "LangChain",
    "hugging face":           "Hugging Face",
    "vector database":        "Vector Database",
    "google cloud":           "Google Cloud",
    "spring boot":            "Spring Boot",
    "github actions":         "GitHub Actions",
    "power bi":               "Power BI",
    "apache spark":           "Apache Spark",
    "react":                  "React",
    "redux":                  "Redux",
    "numpy":                  "NumPy",
    "pandas":                 "Pandas",
    "matplotlib":             "Matplotlib",
    "scikit":                 "Scikit-learn",
    "jupyter":                "Jupyter",
    "docker":                 "Docker",
    "kubernetes":             "Kubernetes",
    "linux":                  "Linux",
    "nginx":                  "Nginx",
    "firebase":               "Firebase",
    "supabase":               "Supabase",
    "elasticsearch":          "Elasticsearch",
    "dynamodb":               "DynamoDB",
    "redis":                  "Redis",
    "sqlite":                 "SQLite",
    "mysql":                  "MySQL",
    "vercel":                 "Vercel",
    "netlify":                "Netlify",
    "terraform":              "Terraform",
    "figma":                  "Figma",
    "postman":                "Postman",
    "keras":                  "Keras",
    "xgboost":                "XGBoost",
    "web3.js":                "Web3.js",
    "solidity":               "Solidity",
    "ethereum":               "Ethereum",
}


def extract_skills(text: str) -> dict:
    from utils.constants import ALL_SKILLS, HOT_SKILLS, IN_DEMAND_SKILLS

    text_lower = text.lower()
    found      = []
    hot_tech   = []
    in_demand  = []

    for skill in ALL_SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, text_lower):
            display = _to_display_case(skill)
            found.append(display)
            if skill in HOT_SKILLS:
                hot_tech.append(display)
            if skill in IN_DEMAND_SKILLS:
                in_demand.append(display)

    return {
        "found":          sorted(set(found)),
        "hot_technology": sorted(set(hot_tech)),
        "in_demand":      sorted(set(in_demand)),
        "count":          len(set(found)),
    }


def _to_display_case(skill: str) -> str:
    """Return skill in correct display casing."""
    lower = skill.lower().strip()
    # Check special cases first
    if lower in SPECIAL_CASES:
        return SPECIAL_CASES[lower]
    # Check original CSV casing
    if lower in _SKILL_DISPLAY:
        return _SKILL_DISPLAY[lower]
    # Fallback to title case
    return skill.title()
