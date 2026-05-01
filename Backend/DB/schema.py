from pydantic import BaseModel

class Crypto_Response(BaseModel):
    crypto_pair: str
    Open_time: int
    Close_time: int
    open_: float
    high: float
    low: float
    close: float
    Volume: str
    Volume_Quote: str