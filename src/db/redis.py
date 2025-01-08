from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIARY= 3600

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    db=0
)

async def add_jti_to_blacklist(jti:str)->None:
    await token_blocklist.set(
        name= jti,
        value="",
        ex= JTI_EXPIARY
    )

async def token_in_blocklist(jti:str)->bool:
    jti = await token_blocklist.get(jti)
    
    return jti is not None