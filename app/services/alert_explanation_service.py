from app.db.models.alert import Alert
from app.repositories.alert_repository import AlertRepository

class AlertExplanationService:
    def __init__(self, alert_repo: AlertRepository) -> None:
        self.alert_repo = alert_repo

    def explain_alert(self, alert_id: int) -> dict:
        alert = self.alert_repo.get_by_id(alert_id)

        if not alert:
            raise ValueError("Alert not found")

        severity = self._to_str(alert.severity)
        status = self._to_str(alert.status)

        return {
            "alert_id": alert.id,
            "title": alert.title,
            "severity": severity,
            "risk_score": alert.risk_score,
            "status": status,
            "summary": self._build_summary(alert),
            "severity_explanation": self._build_severity_explanation(
                severity=severity,
                risk_score=alert.risk_score,
            ),
            "possible_causes": self._build_possible_causes(alert),
            "recommended_actions": self._build_recommended_actions(
                severity=severity,
                risk_score=alert.risk_score,
            ),
            "source": "rule_based",
        }

    def _build_summary(self, alert: Alert) -> str:
        description = alert.description or "No detailed description available."

        return (
            f"Alert '{alert.title}' was generated with severity "
            f"'{self._to_str(alert.severity)}' and risk score {alert.risk_score}. "
            f"{description}"
        )

    def _build_severity_explanation(
        self,
        severity: str,
        risk_score: int,
    ) -> str:
        if severity == "critical" or risk_score >= 95:
            return (
                "Critical severity indicates a very high-risk security event that may "
                "require immediate investigation, containment, and response."
            )

        if severity == "high" or risk_score >= 70:
            return (
                "High severity indicates suspicious activity with significant risk. "
                "The event should be reviewed as soon as possible and correlated with related logs."
            )

        if severity == "medium" or risk_score >= 40:
            return (
                "Medium severity indicates potentially suspicious behavior. "
                "The event should be investigated and monitored for repeated or related activity."
            )

        return (
            "Low severity indicates limited risk, but the event should still be "
            "monitored for repeated or correlated activity."
        )

    def _build_possible_causes(self, alert: Alert) -> list[str]:
        title = alert.title.lower()
        description = (alert.description or "").lower()

        if "autoencoder" in title or "autoencoder" in description:
            return [
                "Unusual network traffic pattern compared to learned normal behavior.",
                "Abnormal packet or byte ratio in the analyzed network event.",
                "Potential scanning, probing, or suspicious automated traffic.",
            ]

        if "intrusion" in title or "intrusion" in description:
            return [
                "Potential network intrusion attempt.",
                "Suspicious traffic pattern detected by rule engine or ML model.",
                "Possible packet flood, scanning activity, or malicious connection attempt.",
            ]

        if (
            "fraud" in title
            or "fraud" in description
            or "transaction" in title
            or "transaction" in description
        ):
            return [
                "Suspicious transaction behavior.",
                "Transaction pattern differs from expected legitimate activity.",
                "Potential financial fraud or abnormal user behavior.",
            ]

        return [
            "Unusual security event detected.",
            "Potential anomaly requiring investigation.",
            "Event may be related to suspicious system or network behavior.",
        ]

    def _build_recommended_actions(
        self,
        severity: str,
        risk_score: int,
    ) -> list[str]:
        actions = [
            "Review the related security event details.",
            "Check correlated alerts and recent activity from the same source.",
            "Verify whether similar events occurred in a short time window.",
        ]

        if severity in {"critical", "high"} or risk_score >= 70:
            actions.extend(
                [
                    "Investigate the source IP and destination system immediately.",
                    "Review firewall, application, and authentication logs.",
                    "Consider temporarily blocking or isolating suspicious traffic.",
                ]
            )

        elif severity == "medium" or risk_score >= 40:
            actions.extend(
                [
                    "Check source IP reputation.",
                    "Review network traffic patterns for repeated anomalies.",
                ]
            )

        else:
            actions.extend(
                [
                    "Monitor the source for repeated suspicious behavior.",
                    "Keep the alert open if additional context is needed.",
                ]
            )

        return actions

    def _to_str(self, value) -> str:
        if hasattr(value, "value"):
            return value.value

        return str(value)    