from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from Backend.DB.schema import Crypto_Response
from Backend.DB.main import get_session
from Backend.DB.models import CryptoResonse


db_route = APIRouter(prefix="/init db", tags=["Initialize Database"])


@db_route.post("/init_db")
async def init_db(crypto_data: Crypto_Response, session: AsyncSession = Depends(get_session)):
    crypto_pair_data = crypto_data
    crypto_records = CryptoResonse(
    crypto_pair = crypto_pair_data.crypto_pair,
    Open_time = crypto_pair_data.Open_time,
    Close_time = crypto_pair_data.Close_time,
    open_= crypto_pair_data.open_,
    high = crypto_pair_data.high,
    low = crypto_pair_data.low,
    close = crypto_pair_data.close,
    Volume = crypto_pair_data.Volume,
    Volume_Quote = crypto_pair_data.Volume_Quote
    )

    session.add(crypto_records)

    await session.commit()




    