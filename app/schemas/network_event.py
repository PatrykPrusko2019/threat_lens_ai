from pydantic import BaseModel

class NetworkEventRequest(BaseModel):
    source_ip: str
    destination_ip: str
    protocol: str
    duration: float
    bytes_sent: int
    bytes_received: int
    packets_sent: int
    packets_received: int
