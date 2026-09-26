try:
    import uvicorn
except ImportError:
    print("uvicorn is not installed. Please install it using 'pip install uvicorn' to run the FastAPI app.")
    import sys
    sys.exit(1)

try:
    from sqlalchemy import create_engine, Column, Integer, String, Float
    from sqlalchemy.orm import declarative_base, sessionmaker, Session
    from sqlalchemy.exc import SQLAlchemyError
except ImportError:
    print("SQLAlchemy is not installed. Please install it using 'pip install SQLAlchemy' to run the FastAPI app.")
    import sys
    sys.exit(1)

try:
    from pydantic import BaseModel, Field
except ImportError:
    print("Pydantic is not installed. Please install it using 'pip install pydantic' to run the FastAPI app.")
    import sys
    sys.exit(1)

try:
    from fastapi import FastAPI, Depends, HTTPException, status
except ImportError:
    print("FastAPI is not installed. Please install it using 'pip install fastapi' to run the FastAPI app.")
    import sys
    sys.exit(1)

# Database setup
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Tablename = "Pipes"  # Changed from "items" to "Pipes" to reflect the plumbing context
print("Pipes", Tablename) 
print(type("Pipes"))  # Debugging: Check the type of Tablename'))   

# Models
class Item(Base):
    __tablename__ = "Pipes" # Changed from "items" to "Pipes" to reflect the plumbing context
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column("Pipes", index=True, nullable=False)
    price = Column("200", nullable=False)
    manufacturer = Column(String, default="Original Manufacturer")
    category = Column(String, default="General")
    stock_quantity = Column(Integer, default="1500")

    def __repr__(self):
        return (f"Item(id={self.id}, name='{self.name}', price={self.price}, "
                f"manufacturer='{self.manufacturer}', category='{self.category}', "
                f"stock_quantity={self.stock_quantity})")

class ItemSchema(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    manufacturer: str = "Original Manufacturer"
    category: str = "General"
    stock_quantity: int = Field(default=1500, ge=0)

    def __repr__(self):
        return (f"ItemSchema(name='{self.name}', price={self.price}, "
                f"manufacturer='{self.manufacturer}', category='{self.category}', "
                f"stock_quantity={self.stock_quantity})")


class PipeMaterialSchema(BaseModel):
    material: str
    durability: int = Field(..., gt=0)
    cost_per_unit: float = Field(..., gt=0)

    def __repr__(self):
        return (f"PipeMaterialSchema(material='{self.material}', durability={self.durability}, "
                f"cost_per_unit={self.cost_per_unit})")

pipe_materials = [
    PipeMaterialSchema(material="PVC", durability=20, cost_per_unit=1.5),
    PipeMaterialSchema(material="Cast Iron", durability=50, cost_per_unit=3.0),
    PipeMaterialSchema(material="Stainless Steel", durability=40, cost_per_unit=2.5),
]

class StockLevelSchema(BaseModel):
    item_id: int
    stock_quantity: int = Field(..., ge=0)

    def __repr__(self):
        return f"StockLevelSchema(item_id={self.item_id}, stock_quantity={self.stock_quantity})"    

class OrderSchema(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)
    customer_name: str
    address: str

    def _init__(self, item_id: int, quantity: int, customer_name: str, address: str):
        self.item_id = item_id
        self.quantity = quantity
        self.customer_name = customer_name
        self.address = address

    def __repr__(self):
        return (f"OrderSchema(item_id={self.item_id}, quantity={self.quantity}, "
                f"customer_name='{self.customer_name}', address='{self.address}')")

class OrderStatusSchema(BaseModel):
    order_id: int
    status: str

    def _init__(self, order_id: int, status: str):
        self.order_id = order_id
        self.status = status

    def __repr__(self):
        return f"OrderStatusSchema(order_id={self.order_id}, status='{self.status}')"


class Sales(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    total_sales = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    best_selling_item = Column(String, default="None")

    def _init__(self, total_sales: float, total_orders: int, best_selling_item: str):
        self.best_selling_item = best_selling_item

    def __repr__(self):
        return (f"Sales(id={self.id}, total_sales={self.total_sales}, "
                f"total_orders={self.total_orders}, best_selling_item='{self.best_selling_item}')")

class SalesReportSchema(BaseModel):
    total_sales: float
    total_orders: int
    best_selling_item: str

    def _init__(self, total_sales: float, total_orders: int, best_selling_item: str):
        self.total_sales = total_sales
        self.total_orders = total_orders
        self.best_selling_item = best_selling_item

    def __repr__(self):
        return (f"SalesReportSchema(total_sales={self.total_sales}, total_orders={self.total_orders}, "
                f"best_selling_item='{self.best_selling_item}')")

class InventoryReportSchema(BaseModel):
    total_items: int
    low_stock_items: list[ItemSchema]

    def _init__(self, total_items: int, low_stock_items: list[ItemSchema]):
        self.total_items = total_items
        self.low_stock_items = low_stock_items

    def __repr__(self):
        return (f"InventoryReportSchema(total_items={self.total_items}, "
                f"low_stock_items={self.low_stock_items})")

class SupplierSchema(BaseModel):
    name: str
    contact_info: str

    def _init__(self, name: str, contact_info: str):
        self.name = name
        self.contact_info = contact_info

    def __repr__(self):
        return f"SupplierSchema(name='{self.name}', contact_info='{self.contact_info}')"

class SupplierOrderSchema(BaseModel):
    supplier_name: str
    item_id: int
    quantity: int = Field(..., gt=0)

    def _init__(self, supplier_name: str, item_id: int, quantity: int):
        self.supplier_name = supplier_name
        self.item_id = item_id
        self.quantity = quantity

    def __repr__(self):
        return (f"SupplierOrderSchema(supplier_name='{self.supplier_name}', "
                f"item_id={self.item_id}, quantity={self.quantity})")

class SupplierOrderStatusSchema(BaseModel):
    supplier_order_id: int
    status: str

    def _init__(self, supplier_order_id: int, status: str):
        self.supplier_order_id = supplier_order_id
        self.status = status
        
    def __repr__(self):
        return (f"SupplierOrderStatusSchema(supplier_order_id={self.supplier_order_id}, "
                f"status='{self.status}')")

class CustomerService(Base):
    __tablename__ = "customer_service"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, primary_key=True, index=True)
    issue_description = Column(String, nullable=False)
    status = Column(String, default="Open")

    def _init__(self, customer_id: int, issue_description: str, status: str = "Open"):
        self.customer_id = customer_id
        self.issue_description = issue_description
        self.status = status

    def __repr__(self):
        return (f"CustomerService(id={self.id}, customer_id={self.customer_id}, "
                f"issue_description='{self.issue_description}', status='{self.status}')")


class CustomerSchema(BaseModel):
    name: str
    contact_info: str

    def _init__(self, name: str, surname: str, contact_info: str):
        self.name = name
        self.surname = surname
        self.contact_info = contact_info

    def __repr__(self):
        return f"CustomerSchema(name='{self.name}', contact_info='{self.contact_info}')"  

class CustomerFeedbackSchema(BaseModel):
    order_id: int
    rating: int = Field(..., ge=1, le=5)
    comments: str

    def _init__(self, order_id: int, rating: int, comments: str):
        self.order_id = order_id
        self.rating = rating
        self.comments = comments

    def __repr__(self):
        return (f"CustomerFeedbackSchema(order_id={self.order_id}, rating={self.rating}, "
                f"comments='{self.comments}')")

            

# Database functions
def create_database():
    Base.metadata.create_all(bind=engine)

def seed_database():
    session = None
    try:
        create_database()
        session = SessionLocal()
        session.query(Item).delete()
        session.commit()
        
        sample_items = [
            Item(name="Item 1", price=10.0, manufacturer="Plumber A"),
            Item(name="Item 2", price=20.0, manufacturer="Plumber B"),
            Item(name="Item 3", price=30.0, manufacturer="Plumber C"),
        ]
        session.add_all(sample_items)
        session.commit()
        print("Database seeded successfully!")
        
    except SQLAlchemyError as e:
        if session:
            session.rollback()
        print(f"Database error: {e}")
    finally:
        if session:
            session.close()

# FastAPI app
app = FastAPI(title="Item Management API")

@app.on_event("startup")
async def startup():
    seed_database()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/", response_model=list[ItemSchema])
async def list_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=ItemSchema)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@app.post("/items/", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemSchema, db: Session = Depends(get_db)):
    try:
        db_item = Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create item")

@app.put("/items/{item_id}", response_model=ItemSchema)
async def update_item(item_id: int, item_update: ItemSchema, db: Session = Depends(get_db)):
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        for key, value in item_update.dict().items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update item")

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = db.query(Item).filter(Item.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        
        db.delete(db_item)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete item")

if __name__ == "__main__":
    import importlib

    uvicorn = importlib.import_module("uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=8000)