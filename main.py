from fastapi import FastAPI

from Db.database import Base,engine
from Router.CoursSets import router as CoursSets_router
from Router.Requirements import router as Requirements_router

app = FastAPI()

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(CoursSets_router, prefix='/CoursSets',tags=['CoursSets'])
app.include_router(Requirements_router, prefix='/Requirements',tags=['Requirements'])

