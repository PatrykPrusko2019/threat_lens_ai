from app.db.models.alert import Alert
from app.db.models.event import SecurityEvent
from app.db.session import SessionLocal


def main() -> None:
    db = SessionLocal()

    try:
        existing_events_count = db.query(SecurityEvent).count()
        existing_alerts_count = db.query(Alert).count()

        if existing_events_count > 0 or existing_alerts_count > 0:
            print("Demo data already exists. Skipping demo seed.")
            return

        events = [
            SecurityEvent(
                event_type="brute_force",
                severity="high",
                source_ip="192.168.1.25",
                description="Multiple failed login attempts detected from the same source IP.",
            ),
            SecurityEvent(
                event_type="port_scan",
                severity="medium",
                source_ip="10.0.0.15",
                description="Unusual port scanning activity detected against internal services.",
            ),
            SecurityEvent(
                event_type="malware_activity",
                severity="critical",
                source_ip="172.16.0.22",
                description="Suspicious executable behavior detected on monitored host.",
            ),
            SecurityEvent(
                event_type="data_exfiltration",
                severity="critical",
                source_ip="192.168.1.80",
                description="Abnormally high outbound traffic volume detected.",
            ),
            SecurityEvent(
                event_type="suspicious_login",
                severity="medium",
                source_ip="185.23.44.10",
                description="Login attempt from unusual geolocation and unknown device.",
            ),
        ]

        db.add_all(events)
        db.flush()

        alerts = [
            Alert(
                event_id=events[0].id,
                title="Possible brute force attack",
                severity="high",
                status="open",
                risk_score=85,
                description="Repeated authentication failures may indicate a brute force attempt.",
            ),
            Alert(
                event_id=events[1].id,
                title="Internal port scan detected",
                severity="medium",
                status="in_progress",
                risk_score=62,
                description="Network scan behavior detected from internal host.",
            ),
            Alert(
                event_id=events[2].id,
                title="Critical malware activity",
                severity="critical",
                status="open",
                risk_score=96,
                description="Host behavior matches malware execution patterns.",
            ),
            Alert(
                event_id=events[3].id,
                title="Possible data exfiltration",
                severity="critical",
                status="open",
                risk_score=93,
                description="Large outbound transfer detected from workstation.",
            ),
            Alert(
                event_id=events[4].id,
                title="Suspicious login attempt",
                severity="medium",
                status="closed",
                risk_score=58,
                description="Login anomaly was reviewed and closed.",
            ),
        ]

        db.add_all(alerts)
        db.commit()

        print("Demo security events and alerts created.")

    finally:
        db.close()


if __name__ == "__main__":
    main()