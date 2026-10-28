import os
import sys
import json
from datetime import datetime, timezone

# Ensure root workspace is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.api.evaluation import get_evaluation_report


def generate_reports():
    os.makedirs("./reports", exist_ok=True)
    report_data = get_evaluation_report().model_dump()

    json_path = "./reports/evaluation_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    md_path = "./reports/EVALUATION_REPORT.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# TalentLens AI — Model Evaluation & Academic Benchmark Report\n\n")
        f.write(f"**Generated At:** {report_data['generated_at']}\n")
        f.write(f"**Dataset:** {report_data['dataset_name']} (Total Samples: {report_data['total_samples']})\n\n")

        f.write("## 1. Algorithmic Benchmark Comparison Matrix\n\n")
        f.write("| Model Architecture | Precision | Recall | F1-Score | PR-AUC | NDCG@5 | MRR | Latency |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for b in report_data["benchmarks"]:
            f.write(f"| **{b['model_name']}** | {b['precision']:.3f} | {b['recall']:.3f} | {b['f1_score']:.3f} | {b['pr_auc']:.3f} | {b['ndcg_at_5']:.3f} | {b['mrr']:.3f} | {b['latency_ms']} ms |\n")

        f.write("\n## 2. Demographic Fairness & Proxy Feature Audit\n\n")
        audit = report_data["proxy_bias_audit"]
        f.write(f"**Audit Status:** {audit['status']}\n\n")
        f.write(f"**Excluded Attributes:** {', '.join(audit['protected_attributes_excluded'])}\n\n")
        f.write(f"**Audit Analysis:** {audit['feature_audit_notes']}\n\n")

        f.write("## 3. Calibration & Uncertainty Statement\n\n")
        f.write(f"{report_data['calibration_summary']}\n")

    print(f"Evaluation report generated successfully:\n - {json_path}\n - {md_path}")


if __name__ == "__main__":
    generate_reports()
