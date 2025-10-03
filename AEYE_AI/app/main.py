import argparse
import asyncio

from fastapi import FastAPI
from hypercorn.asyncio import serve
from hypercorn.config import Config

parser = argparse.ArgumentParser(description="AEYE Flask Server")
parser.add_argument('config', type=str, help="Flask config path")
args = parser.parse_args()

from contextlib import asynccontextmanager

from AEYE import registry as registry
from AEYE.boot_loader import bootstrap, shutdown
from AEYE.config import load_config

AEYE_cfg = load_config(args.config)
registry.set_cfg(AEYE_cfg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    gpu = await bootstrap()
    asyncio.create_task(gpu.micro_batch_schdeuler())

    yield
    
    await shutdown()

app = FastAPI(lifespan=lifespan)

from routers.v1 import check_result, health, http_1_1, main

app.include_router(health.router, prefix=AEYE_cfg.FASTAPI.API_PREFIX, tags=["health"])
app.include_router(http_1_1.router, prefix=AEYE_cfg.FASTAPI.API_PREFIX, tags=["upload"])
app.include_router(check_result.router, prefix=AEYE_cfg.FASTAPI.API_PREFIX, tags=["result"])
app.include_router(main.router, tags=["main"])

async def start():
    config = Config()
    config.bind = [AEYE_cfg.FASTAPI.HOST + ":" + str(AEYE_cfg.FASTAPI.PORT)]
    config.reload = getattr(AEYE_cfg.FASTAPI.RELOAD, "RELOAD", True)
    config.workers = AEYE_cfg.FASTAPI.WORKERS
    config.loglevel = getattr(AEYE_cfg.FASTAPI.LOG_LEVEL, "LOG_LEVEL", "info").lower()

    await serve(app, config)
    
if __name__ == "__main__":
    asyncio.run(start())