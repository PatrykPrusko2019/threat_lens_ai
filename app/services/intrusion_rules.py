from app.schemas.network_event import NetworkEventRequest

class IntrusionRuleEngine:
    def evaluate(
            self,
            event: NetworkEventRequest,
    ) -> tuple[bool, str | None]:
        
        # very high network traffic in a short time
        if (
            event.duration <= 2
            and event.packets_sent >=50_000
        ):
            return True, "Possible packet flood attack"
        
        # very high amount of sent data
        if event.bytes_sent >= 5_000_000:
            return True, "Suspiciously high outgoing traffic"
        
        # scanning / abnormal traffic
        if (
            event.packets_sent > 100_000
            and event.bytes_received < 100
        ):
            return True, "Possible scanning activity"
        
        return False, None

