from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MetricDetail(BaseModel):
    name: str
    value: float
    description: str


class ModelBenchmark(BaseModel):
    model_name: str
    task: str
    precision: float
    recall: float
    f1_score: float
    pr_auc: float
    ndcg_at_5: float
    mrr: float
    latency_ms: float
    sample_size: int
    notes: str


class EvaluationReportSchema(BaseModel):
    dataset_name: str
    is_synthetic: bool = True
    total_samples: int
    train_samples: int
    val_samples: int
    test_samples: int
    baseline_metrics: Dict[str, float]
    benchmarks: List[ModelBenchmark]
    calibration_summary: str
    proxy_bias_audit: Dict[str, Any]
    generated_at: str
