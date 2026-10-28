import re
from typing import Dict, List, Optional, Tuple, Set

# Comprehensive canonical skills taxonomy with aliases and categories
SKILL_TAXONOMY: Dict[str, Dict] = {
    # Programming Languages
    "python": {
        "canonical": "Python",
        "category": "Programming Languages",
        "aliases": ["python", "python3", "py", "cpython"],
    },
    "java": {
        "canonical": "Java",
        "category": "Programming Languages",
        "aliases": ["java", "core java", "j2se", "jdk"],
    },
    "javascript": {
        "canonical": "JavaScript",
        "category": "Programming Languages",
        "aliases": ["javascript", "js", "ecmascript", "es6", "es6+"],
    },
    "typescript": {
        "canonical": "TypeScript",
        "category": "Programming Languages",
        "aliases": ["typescript", "ts"],
    },
    "c++": {
        "canonical": "C++",
        "category": "Programming Languages",
        "aliases": ["c++", "cpp", "c plus plus"],
    },
    "c#": {
        "canonical": "C#",
        "category": "Programming Languages",
        "aliases": ["c#", "csharp", "c sharp", ".net c#"],
    },
    "go": {
        "canonical": "Go",
        "category": "Programming Languages",
        "aliases": ["golang", "go language", "go lang"],
    },
    "rust": {
        "canonical": "Rust",
        "category": "Programming Languages",
        "aliases": ["rust", "rustlang"],
    },
    "sql": {
        "canonical": "SQL",
        "category": "Databases & Query Languages",
        "aliases": ["sql", "structured query language", "t-sql", "pl/sql"],
    },
    "r": {
        "canonical": "R",
        "category": "Programming Languages",
        "aliases": ["r language", "r programming"],
    },

    # Machine Learning & AI
    "pytorch": {
        "canonical": "PyTorch",
        "category": "Machine Learning & AI",
        "aliases": ["pytorch", "torch", "libtorch"],
    },
    "tensorflow": {
        "canonical": "TensorFlow",
        "category": "Machine Learning & AI",
        "aliases": ["tensorflow", "tf", "tf2"],
    },
    "keras": {
        "canonical": "Keras",
        "category": "Machine Learning & AI",
        "aliases": ["keras"],
    },
    "scikit-learn": {
        "canonical": "scikit-learn",
        "category": "Machine Learning & AI",
        "aliases": ["scikit-learn", "sklearn", "scikit learn"],
    },
    "nlp": {
        "canonical": "Natural Language Processing",
        "category": "Machine Learning & AI",
        "aliases": ["nlp", "natural language processing", "text mining", "computational linguistics"],
    },
    "computer vision": {
        "canonical": "Computer Vision",
        "category": "Machine Learning & AI",
        "aliases": ["computer vision", "cv", "image processing", "object detection"],
    },
    "transformers": {
        "canonical": "Transformers",
        "category": "Machine Learning & AI",
        "aliases": ["transformers", "huggingface", "hugging face", "bert", "gpt", "roberta", "t5"],
    },
    "llm": {
        "canonical": "Large Language Models",
        "category": "Machine Learning & AI",
        "aliases": ["llm", "large language models", "prompt engineering", "langchain", "llamaindex", "rag"],
    },
    "deep learning": {
        "canonical": "Deep Learning",
        "category": "Machine Learning & AI",
        "aliases": ["deep learning", "neural networks", "dnn", "cnn", "rnn", "lstm"],
    },
    "mlops": {
        "canonical": "MLOps",
        "category": "Machine Learning & AI",
        "aliases": ["mlops", "model deployment", "model monitoring", "mlflow", "kubeflow", "weights & biases", "wandb"],
    },
    "pandas": {
        "canonical": "Pandas",
        "category": "Data Science & Analytics",
        "aliases": ["pandas"],
    },
    "numpy": {
        "canonical": "NumPy",
        "category": "Data Science & Analytics",
        "aliases": ["numpy"],
    },

    # Web & Backend Frameworks
    "fastapi": {
        "canonical": "FastAPI",
        "category": "Backend Engineering",
        "aliases": ["fastapi", "fast api", "fast-api"],
    },
    "flask": {
        "canonical": "Flask",
        "category": "Backend Engineering",
        "aliases": ["flask"],
    },
    "django": {
        "canonical": "Django",
        "category": "Backend Engineering",
        "aliases": ["django", "django rest framework", "drf"],
    },
    "react": {
        "canonical": "React",
        "category": "Frontend Engineering",
        "aliases": ["react", "react.js", "reactjs", "react native"],
    },
    "node.js": {
        "canonical": "Node.js",
        "category": "Backend Engineering",
        "aliases": ["node.js", "nodejs", "node js", "express", "express.js"],
    },
    "next.js": {
        "canonical": "Next.js",
        "category": "Frontend Engineering",
        "aliases": ["next.js", "nextjs"],
    },
    "spring boot": {
        "canonical": "Spring Boot",
        "category": "Backend Engineering",
        "aliases": ["spring boot", "springboot", "spring framework", "spring"],
    },
    "graphql": {
        "canonical": "GraphQL",
        "category": "Backend Engineering",
        "aliases": ["graphql", "apollo graphql"],
    },
    "rest api": {
        "canonical": "REST APIs",
        "category": "Backend Engineering",
        "aliases": ["rest api", "restful api", "restful apis", "rest web services", "rest"],
    },

    # Cloud, DevOps & Infrastructure
    "docker": {
        "canonical": "Docker",
        "category": "Cloud & DevOps",
        "aliases": ["docker", "containerization", "containers", "docker-compose"],
    },
    "kubernetes": {
        "canonical": "Kubernetes",
        "category": "Cloud & DevOps",
        "aliases": ["kubernetes", "k8s"],
    },
    "aws": {
        "canonical": "AWS",
        "category": "Cloud & DevOps",
        "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "fargate", "cloudformation"],
    },
    "azure": {
        "canonical": "Azure",
        "category": "Cloud & DevOps",
        "aliases": ["azure", "microsoft azure", "azure devops"],
    },
    "gcp": {
        "canonical": "Google Cloud",
        "category": "Cloud & DevOps",
        "aliases": ["gcp", "google cloud", "google cloud platform", "bigquery", "vertex ai"],
    },
    "ci/cd": {
        "canonical": "CI/CD",
        "category": "Cloud & DevOps",
        "aliases": ["ci/cd", "continuous integration", "github actions", "gitlab ci", "jenkins"],
    },
    "git": {
        "canonical": "Git",
        "category": "Tools & Version Control",
        "aliases": ["git", "github", "gitlab", "bitbucket", "version control"],
    },
    "linux": {
        "canonical": "Linux",
        "category": "Systems & OS",
        "aliases": ["linux", "unix", "ubuntu", "debian", "redhat", "centos", "bash", "shell scripting"],
    },

    # Databases & Big Data
    "postgresql": {
        "canonical": "PostgreSQL",
        "category": "Databases & Storage",
        "aliases": ["postgresql", "postgres", "psql"],
    },
    "mysql": {
        "canonical": "MySQL",
        "category": "Databases & Storage",
        "aliases": ["mysql", "mariadb"],
    },
    "mongodb": {
        "canonical": "MongoDB",
        "category": "Databases & Storage",
        "aliases": ["mongodb", "mongo", "nosql"],
    },
    "redis": {
        "canonical": "Redis",
        "category": "Databases & Storage",
        "aliases": ["redis", "in-memory cache", "caching"],
    },
    "elasticsearch": {
        "canonical": "Elasticsearch",
        "category": "Databases & Storage",
        "aliases": ["elasticsearch", "elastic search", "opensearch"],
    },
    "apache spark": {
        "canonical": "Apache Spark",
        "category": "Big Data & Distributed Systems",
        "aliases": ["spark", "pyspark", "apache spark"],
    },
    "apache kafka": {
        "canonical": "Apache Kafka",
        "category": "Big Data & Distributed Systems",
        "aliases": ["kafka", "apache kafka", "event streaming"],
    },
}

# Compile alias lookup map sorted by token length descending (so multi-word matches match first)
ALIAS_TO_CANONICAL: List[Tuple[re.Pattern, str, str, str]] = []

for key, entry in SKILL_TAXONOMY.items():
    canonical = entry["canonical"]
    category = entry["category"]
    for alias in entry["aliases"]:
        # Escape special characters (e.g. C++, C#)
        escaped_alias = re.escape(alias)
        # Word boundary handling for symbols like ++ or #
        if alias.endswith("+") or alias.endswith("#"):
            pattern = rf"(?i)(?:\b|(?<=\s)){escaped_alias}(?=\s|[.,;:\)]|$)"
        elif len(alias) <= 2:
            # Short tokens e.g. "r", "go", "js", "ts", "cv" need strict boundary
            pattern = rf"(?i)\b{escaped_alias}\b"
        else:
            pattern = rf"(?i)\b{escaped_alias}\b"
        
        ALIAS_TO_CANONICAL.append((re.compile(pattern), alias, canonical, category))

# Sort so multi-word aliases (e.g. "natural language processing") get checked before "nlp"
ALIAS_TO_CANONICAL.sort(key=lambda x: len(x[1]), reverse=True)


def normalize_skill(skill_query: str) -> Optional[Dict[str, str]]:
    """Normalize any surface skill string to canonical form, or None if unrecognized."""
    clean = skill_query.strip().lower()
    for pattern, alias, canonical, category in ALIAS_TO_CANONICAL:
        if pattern.search(clean) or clean == alias:
            return {"canonical": canonical, "category": category, "raw": skill_query}
    return None


def extract_skills_from_text(text: str) -> List[Dict]:
    """
    Extracts all recognized skills from arbitrary text, returning canonical name,
    category, matched alias, confidence, and contextual snippet.
    """
    found_canonicals: Set[str] = set()
    results = []

    # Split into lines/sentences for snippet tracking
    sentences = re.split(r"(?<=[.!?\n])\s+", text)

    for sentence in sentences:
        if not sentence.strip():
            continue
        for pattern, alias, canonical, category in ALIAS_TO_CANONICAL:
            if canonical in found_canonicals:
                continue
            match = pattern.search(sentence)
            if match:
                found_canonicals.add(canonical)
                # Capture 100-char context window around match for evidence
                start = max(0, match.start() - 30)
                end = min(len(sentence), match.end() + 70)
                snippet = sentence[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(sentence):
                    snippet = snippet + "..."

                results.append({
                    "canonical_name": canonical,
                    "raw_name": match.group(0),
                    "category": category,
                    "confidence": 1.0,
                    "evidence_snippet": snippet
                })

    return results
