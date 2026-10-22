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

Tablename = "Inventory"  # Changed from "items" to "Pipes" to reflect the plumbing context
print("Inventory", Tablename) 

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

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
        

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

def add_item():
    name = input("Plumbing_supplies").strip()
    price = input("Item_price").strip()
    manufacturer = input("Manufacturer").strip()
    category = input("Category").strip()
    stock_quantity = input("Stock_quantity").strip()
    return Item(
        name=name,
        price=float(price),
        manufacturer=manufacturer,
        category=category,
        stock_quantity=int(stock_quantity),
    )

def add_items():
    session = SessionLocal()
    try:
        item = add_item()
        session.add(item)
        session.commit()
        print("Item added.")
    except (ValueError, SQLAlchemyError) as e:
        session.rollback()
        print("Failed to add item:", e)
    finally:
        session.close()

def update_items():
    session = Session()
    try:
        item_id = int(input("Item ID to update: "))
        item = session.query(Item).get(item_id)
        if not item:
            print("Item not found.")
            return

        print(f"Current name: {item.name}")
        new_name = input("New name (leave blank to keep): ").strip()
        if new_name:
            item.name = new_name

        session.commit()
        print("Item updated.")
    except Exception as e:
        session.rollback()
        print("Update failed:", e)
    finally:
        session.close()

def list_items():
    session = Session()
    items = session.query(Item).all()
    for p in items:
        print(f"{p.id}: {p}")
    session.close() 

def add_sales():
    session = SessionLocal()
    try:
        total_sales = float(input("Total_sales").strip())
        total_orders = int(input("Total_orders").strip())
        best_selling_item = input("Best_selling_item").strip()
        sales = Sales(
            total_sales=total_sales,
            total_orders=total_orders,
            best_selling_item=best_selling_item,
        )
        session.add(sales)
        session.commit()
        print("Sales_added")
    except (ValueError, SQLAlchemyError) as e:
        session.rollback()
        print("Failed to add the sales:", e)
    finally:
        session.close()

def update_sales():
    session = Session()
    try:
            sales_id = int(input("Sales ID to update: "))
            book = session.query(Sales).get(sales_id)
            if not book:
                print("Sales updated succesfully.")
                return
    
            print(f"Current status: {sales.status}")
            new_sales = input("New sales(leave blank to keep): ").strip()
            if new_sales:
                sales = new_sales
    
               
            session.commit()
            print("Sales updated.")
    except Exception as e:
            session.rollback()
            print("Update failed:", e)
    finally:
            session.close()

def delete_sales():
    session = Session()
    try:
        sales_id = int(input("Sales ID to delete: "))
        sales = session.query(Sales).get(sales_id)
        if not sales:
            print("Sales not found.")
            return
        session.delete(sales)
        session.commit()
        print("Sales deleted.")
    except Exception as e:
        session.rollback()
        print("Failed to delete:", e)
    finally:
        session.close()            

def list_sales():
    session = Session()
    try:
        sales = session.query(Sales).all()
        for b in sales:
            print(f"{b.id}: {b}")
    finally:
        session.close()


def delete_items():
    session = SessionLocal()
    try:
        item_id = int(input("Item ID to delete: ").strip())
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            print("Item not found.")
            return
        session.delete(item)
        session.commit()
        print("Item deleted.")
    except (ValueError, SQLAlchemyError) as e:
        session.rollback()
        print("Failed to delete item:", e)
    finally:
        session.close()


def add_customer():
    session = SessionLocal()
    try:
        name = input("Customer name: ").strip()
        surname = input("Customer surname: ").strip()
        if not name or not surname:
            raise ValueError("Customer name and surname are required.")

        session.add(Customer(name=name, surname=surname))
        session.commit()
        print("Customer added.")
    except (ValueError, SQLAlchemyError) as e:
        session.rollback()
        print("Failed to add customer:", e)
    finally:
        session.close()


def update_customer():
    session = SessionLocal()
    try:
        customer_id = int(input("Customer ID to update: ").strip())
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if customer is None:
            print("Customer not found.")
            return

        new_name = input("New name (leave blank to keep): ").strip()
        new_surname = input("New surname (leave blank to keep): ").strip()
        if new_name:
            customer.name = new_name
        if new_surname:
            customer.surname = new_surname

        session.commit()
        print("Customer updated.")
    except (ValueError, SQLAlchemyError) as e:
        session.rollback()
        print("Failed to update customer:", e)
    finally:
        session.close()


def delete_customer():
    session = SessionLocal()
    try:
        customer_id = int(input("Customer ID to delete: ").strip())
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if customer is None:
            print("Customer not found.")
            return
        session.delete(customer)
        session.commit()
        print("Customer deleted.")
    except (ValueError, SQLAlchemyError) as e:
        session.rollback()
        print("Failed to delete customer:", e)
    finally:
        session.close()


def list_customers():
    session = SessionLocal()
    try:
        customers = session.query(Customer).all()
        for customer in customers:
            print(f"{customer.id}: {customer.name} {customer.surname}")
    finally:
        session.close()


def main():
    actions = {
        '1': add_items,
        '2': update_items,
        '3': delete_items,
        '4': add_customer,
        '5': update_customer,
        '6': delete_customer,
        '7': list_items,
        '8': list_customers,
        '9': list_sales,
        '0': lambda: sys.exit("👋 Exiting..."),
    }
        
   
    while True:
        print("\n Inventory and customres Menu:")
        print("1. Add Item")
        print("2. Add Customer")
        print("4. Update Item")
        print("5. Update Customer")
        print("5. Delete Item")
        print("6. Delete Customer")
        print("7. List All Items")
        print("8. List Customers")
        print("0. Exit")

        choice = input("Choose action: ").strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")



if  __name__ == "__main__":
    import importlib

    uvicorn = importlib.import_module("uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=8000)