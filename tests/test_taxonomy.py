from backend.nlp.taxonomy import normalize_skill, extract_skills_from_text


def test_canonical_normalization():
    norm_py = normalize_skill("python3")
    assert norm_py is not None
    assert norm_py["canonical"] == "Python"
    assert norm_py["category"] == "Programming Languages"

    norm_nlp = normalize_skill("natural language processing")
    assert norm_nlp is not None
    assert norm_nlp["canonical"] == "Natural Language Processing"

    norm_k8s = normalize_skill("k8s")
    assert norm_k8s is not None
    assert norm_k8s["canonical"] == "Kubernetes"

    norm_cpp = normalize_skill("c++")
    assert norm_cpp is not None
    assert norm_cpp["canonical"] == "C++"


def test_extract_skills_from_sentence():
    text = "Engineered deep learning models with PyTorch, trained Transformers, and deployed via Docker on AWS."
    extracted = extract_skills_from_text(text)
    canonicals = [e["canonical_name"] for e in extracted]

    assert "PyTorch" in canonicals
    assert "Transformers" in canonicals
    assert "Docker" in canonicals
    assert "AWS" in canonicals
    assert "Deep Learning" in canonicals

    # Verify snippet citation is populated
    pytorch_item = next(e for e in extracted if e["canonical_name"] == "PyTorch")
    assert pytorch_item["evidence_snippet"] is not None
    assert "PyTorch" in pytorch_item["evidence_snippet"]
