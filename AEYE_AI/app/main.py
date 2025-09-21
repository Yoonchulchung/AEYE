import argparse
import asyncio

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config

parser = argparse.ArgumentParser(description="SomniAI FastAPI Server")
parser.add_argument('config', type=str, help="FastAPI config path")
args = parser.parse_args()

from contextlib import asynccontextmanager

from AEYE.boot_loader import bootstrap, shutdown
from AEYE.config import load_config
from AEYE import registry as registry


AEYE_cfg = load_config(args.config)
registry.set_cfg(AEYE_cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    gpu = await bootstrap()
    asyncio.create_task(gpu.micro_batch_schdeuler())
    
    yield
    
    shutdown()


app = FastAPI(lifespan=lifespan)

from routers.v1 import health
app.include_router(health.router, prefix=AEYE_cfg.FASTAPI.API_PREFIX, tags=["health"])



async def start():
    config = Config()
    config.bind = [f"{AEYE_cfg.FASTAPI.HOST}:{AEYE_cfg.FASTAPI.PORT}"]
    config.reload = getattr(AEYE_cfg.FASTAPI.RELOAD, "RELOAD", True)
    config.workers = AEYE_cfg.FASTAPI.WORKERS
    config.loglevel = getattr(AEYE_cfg.FASTAPI.LOG_LEVEL, "LOG_LEVEL", "info").lower()

    await serve(app, config)
    
if __name__ == "__main__":
    asyncio.run(start())