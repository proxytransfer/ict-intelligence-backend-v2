from dataclasses import dataclass
from enum import Enum

class ZoneType(str, Enum):
    SSL = "SSL"
    BSL = "BSL"
    FVG = "FVG"
    OB = "OB"

@dataclass
class LiquidityZone:
    price_level: float
    zone_type: ZoneType
    strength: float      # 0 a 1
    swept: bool = False
