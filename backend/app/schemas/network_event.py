from ipaddress import ip_address

from pydantic import BaseModel, Field, field_validator

class NetworkEventRequest(BaseModel):
    source_ip: str = Field(min_length=3, max_length=45)
    destination_ip: str = Field(min_length=3, max_length=45)
    protocol: str = Field(min_length=2, max_length=10)
    duration: float = Field(ge=0)
    bytes_sent: int = Field(ge=0)
    bytes_received: int = Field(ge=0)
    packets_sent: int = Field(ge=0)
    packets_received: int = Field(ge=0)

@field_validator("source_ip", "destination_ip")
@classmethod
def validate_ip_address(cls, value: str) -> str:
    try:
        ip_address(value)
    except ValueError as exc:
        raise ValueError("must be a valid IP address") from exc

    return value

@field_validator("protocol")
@classmethod
def normalize_protocol(cls, value: str) -> str:
    normalize_protocol = value.strip().lower()
    allowed_protocols = {"tcp", "udp", "icmp"}

    if normalize_protocol not in allowed_protocols:
        raise ValueError("protocol must be one of: tcp, udp, icmp")

    return normalize_protocol    