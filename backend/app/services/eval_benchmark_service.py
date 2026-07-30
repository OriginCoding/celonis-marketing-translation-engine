import math
from typing import List, Dict, Any

class EvalBenchmarkService:
    """
    100% Free & Open-Source Evaluator Alignment & Drift Service.
    Calculates Cohen's Kappa (kappa) coefficient measuring human-AI decision agreement
    and tracks AI Judge evaluation score drift over time.
    """

    @staticmethod
    def calculate_cohen_kappa(human_approvals: List[bool], ai_approvals: List[bool]) -> float:
        """
        Calculates Cohen's Kappa (kappa) agreement coefficient.
        Returns value between -1.0 (total disagreement) and +1.0 (perfect agreement).
        """
        if not human_approvals or len(human_approvals) != len(ai_approvals):
            return 1.0

        total = len(human_approvals)
        both_yes = sum(1 for h, a in zip(human_approvals, ai_approvals) if h and a)
        both_no = sum(1 for h, a in zip(human_approvals, ai_approvals) if not h and not a)
        
        observed_agreement = (both_yes + both_no) / total
        
        human_yes_prob = sum(1 for h in human_approvals if h) / total
        ai_yes_prob = sum(1 for a in ai_approvals if a) / total
        
        expected_yes = human_yes_prob * ai_yes_prob
        expected_no = (1 - human_yes_prob) * (1 - ai_yes_prob)
        expected_agreement = expected_yes + expected_no
        
        if expected_agreement == 1.0:
            return 1.0
            
        kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)
        return round(kappa, 4)

    @staticmethod
    def detect_evaluator_drift(baseline_scores: List[float], recent_scores: List[float]) -> Dict[str, Any]:
        """Detects AI Judge score distribution drift over time."""
        if not baseline_scores or not recent_scores:
            return {"drift_detected": False, "score_delta": 0.0}

        avg_baseline = sum(baseline_scores) / len(baseline_scores)
        avg_recent = sum(recent_scores) / len(recent_scores)
        delta = round(abs(avg_recent - avg_baseline), 2)
        
        return {
            "baseline_mean": round(avg_baseline, 2),
            "recent_mean": round(avg_recent, 2),
            "score_delta": delta,
            "drift_detected": delta > 5.0  # Alert if drift exceeds 5 points
        }
