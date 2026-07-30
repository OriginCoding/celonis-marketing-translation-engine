from app.models import QualityMetricBreakdown, RoutingDecision

class RouterAgent:
    def route(self, quality_score: QualityMetricBreakdown, auto_pass_threshold: float = 88.0, hitl_threshold: float = 70.0) -> RoutingDecision:
        score = quality_score.overall_confidence
        residue_level = getattr(quality_score, "residue_level", "NONE")

        # Hard Override 1: Any DNT violation forces HITL Review or Re-translation
        if quality_score.dnt_violations:
            if score >= hitl_threshold:
                return RoutingDecision(
                    status="HITL_REVIEW",
                    threshold_auto_pass=auto_pass_threshold,
                    threshold_hitl=hitl_threshold,
                    reasoning=f"Overridden to HITL Review due to {len(quality_score.dnt_violations)} critical Do-Not-Translate (DNT) term violations.",
                    assigned_to="Language Champion (Spanish Team)",
                    recommended_action="Review DNT term alterations manually before approving asset."
                )
            else:
                return RoutingDecision(
                    status="REJECT_RETRANSLATE",
                    threshold_auto_pass=auto_pass_threshold,
                    threshold_hitl=hitl_threshold,
                    reasoning=f"Rejected: Confidence score ({score}%) fell below minimum threshold ({hitl_threshold}%) with DNT violations.",
                    assigned_to="Translation Agent (Critique Loop)",
                    recommended_action="Re-trigger translation agent with critique feedback to restore DNT terms."
                )

        # Hard Override 2: Medium/High English Residue forces HITL Review
        if residue_level in ["MEDIUM", "HIGH"]:
            return RoutingDecision(
                status="HITL_REVIEW",
                threshold_auto_pass=auto_pass_threshold,
                threshold_hitl=hitl_threshold,
                reasoning=f"Overridden to HITL Review due to {residue_level} Risk English Residue detected in translated text.",
                assigned_to="Language Champion (Spanish Team)",
                recommended_action="Review untranslated English residue phrases in review portal before publishing."
            )

        if score >= auto_pass_threshold and residue_level in ["NONE", "LOW"]:
            return RoutingDecision(
                status="AUTO_PASS",
                threshold_auto_pass=auto_pass_threshold,
                threshold_hitl=hitl_threshold,
                reasoning=f"Auto-Pass: Confidence score ({score}%) meets threshold ({auto_pass_threshold}%) with Zero DNT violations and {residue_level} English residue.",
                assigned_to="Automated CMS / Staging Pipeline",
                recommended_action="Approve asset for staging deployment and ingest segments into Translation Memory."
            )
        elif score >= hitl_threshold:
            return RoutingDecision(
                status="HITL_REVIEW",
                threshold_auto_pass=auto_pass_threshold,
                threshold_hitl=hitl_threshold,
                reasoning=f"HITL Review Required: Confidence score ({score}%) falls between {hitl_threshold}% and {auto_pass_threshold}%.",
                assigned_to="Language Champion (Spanish Team)",
                recommended_action="Inspect pre-highlighted glossary/formatting flags in review dashboard before publishing."
            )
        else:
            return RoutingDecision(
                status="REJECT_RETRANSLATE",
                threshold_auto_pass=auto_pass_threshold,
                threshold_hitl=hitl_threshold,
                reasoning=f"Rejected: Confidence score ({score}%) is below minimum acceptance threshold ({hitl_threshold}%).",
                assigned_to="Translation Agent (Critique Loop)",
                recommended_action="Re-translate asset using adjusted prompt and explicit structural guardrails."
            )
