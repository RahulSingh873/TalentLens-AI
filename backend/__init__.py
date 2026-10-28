import os

# Ensure HuggingFace runs strictly in offline mode without network socket timeouts
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
