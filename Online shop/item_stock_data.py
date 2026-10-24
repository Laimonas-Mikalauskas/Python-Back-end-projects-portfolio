import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base

# 1. Database Configuration
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# 2. Database Models
class Item(Base):
    __tablename__ = "Pipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String, nullable=False, default="Pipes")
    price = Column(String, nullable=False, default="13 $ per unit")
    material = Column(String, nullable=False, default="Stainless_Steel")
    category = Column(String, nullable=False, default="Plumbing_Supplies")
    manufacturer = Column(String, nullable=False, default="Plumbers.Ltd")

    def __init__(
        self,
        item="Pipes",
        price="13 $ per unit",
        material="Stainless_Steel",
        category="Plumbing_Supplies",
        manufacturer="Plumbers.Ltd",
    ):
        self.item = item
        self.price = price
        self.material = material
        self.category = category
        self.manufacturer = manufacturer

    def __repr__(self):
        return (
            f"Item(id={self.id}, item='{self.item}', material='{self.material}', "
            f"category='{self.category}', manufacturer='{self.manufacturer}')"
        )


class Stock(Base):
    __tablename__ = "Stock"
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(String, nullable=False, default="1000 pairs")
    units = Column(String, nullable=False, default="2000")
    status = Column(String, nullable=False, default="Full")

    def __init__(self, total="1000 pairs", units="2000", status="Full"):
        self.total = total
        self.units = units
        self.status = status

    def __repr__(self):
        return f"Stock(id={self.id}, total={self.total}, units={self.units}, status={self.status})"


# 3. Lifespan event to create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This replaces the dangling session.commit() and correctly creates tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up engine connections on shutdown
    await engine.dispose()


# 4. FastAPI App Initialization
app = FastAPI(
    title='Online Plumbing Store',
    version='1.0.0',
    lifespan=lifespan
)


# 5. Dependency injection for route endpoints
async def get_async_db():
    async with async_session() as session:
        yield session


# 6. Sample Endpoint demonstrating proper Async querying
@app.get("/items")
async def read_items(db: AsyncSession = Depends(get_async_db)):
    # Async queries require 'await db.execute()' paired with a select statement
    result = await db.execute(select(Item))
    items = result.scalars().all()
    return items
