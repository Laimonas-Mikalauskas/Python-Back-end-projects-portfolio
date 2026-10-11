import importlib
import subprocess
import sys

try:
    from fastapi import FastAPI
    uvicorn = importlib.import_module("uvicorn")
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
    from fastapi import FastAPI
    uvicorn = importlib.import_module("uvicorn")

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Online Plumbing Store!"}

@app.get("/categories/{category_id}")
async def read_category(category_id: int):
    return {"category_id": category_id, "status": "Category details would be here"}

@app.post("/categories/")
async def create_category(category_data: dict):
    return {"category_data": category_data, "status": "Category created successfully"}

@app.put("/categories/{category_id}")
async def update_category(category_id: int, category_data: dict):
    return {"category_id": category_id, "category_data": category_data, "status": "Category updated successfully"}

@app.get("/prices/{price_id}")
async def read_price(price_id: int):
    return {"price_id": price_id, "status": "Price details would be here"}  

@app.post("/prices/")
async def create_price(price_data: dict):
    return {"price_data": price_data, "status": "Price created successfully"}

@app.put("/prices/{price_id}")
async def update_price(price_id: int, price_data: dict):
    return {"price_id": price_id, "price_data": price_data, "status": "Price updated successfully"}

@app.get("/prices/{price_id}")
async def delete_price(price_id: int):
    return {"price_id": price_id, "status": "Price deleted successfully"}

@app.get("/discounts/{discount_id}")
async def read_discount(discount_id: int):
    return {"discount_id": discount_id, "status": "Discount details would be here"}

@app.post("/discounts/")
async def create_discount(discount_data: dict):
    return {"discount_data": discount_data, "status": "Discount created successfully"}

@app.put("/discounts/{discount_id}")
async def update_discount(discount_id: int, discount_data: dict):
    return {"discount_id": discount_id, "discount_data": discount_data, "status": "Discount updated successfully"}

@app.delete("/discounts/{discount_id}")
async def delete_discount(discount_id: int):
    return {"discount_id": discount_id, "status": "Discount deleted successfully"}

@app.get("/orders/{order_id}")
async def read_order(order_id: int):
    return {"order_id": order_id, "status": "Order details would be here"}

@app.post("/orders/")
async def create_order(order_data: dict):
    return {"order_data": order_data, "status": "Order created successfully"}

@app.put("/orders/{order_id}")
async def update_order(order_id: int, order_data: dict):
    return {"order_id": order_id, "order_data": order_data, "status": "Order updated successfully"}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    return {"order_id": order_id, "status": "Order deleted successfully"}

@app.get("/orders/{order_id}/review")
async def review_order(order_id: int):
    return {"order_id": order_id, "status": "Order reviewed successfully"}

@app.put("/orders/{order_id}")
async def complete_order(order_id: int, order_data: dict):
    return {"order_id": order_id, "order_data": order_data, "status": "Order completed successfully"}


@app.post("/orders/{order_id}/return")
async def return_order(order_id: int):
    return {"order_id": order_id, "status": "Order returned successfully"}

@app.patch("/orders/{order_id}")
async def patch_order(order_id: int, order_data: dict):
    return {"order_id": order_id, "order_data": order_data, "status": "Order partially updated successfully"}

@app.get("/about_us")
async def read_about_us():
    return {"message": "About us page would be here"}

@app.get("/contact_us")
async def read_contact_us():
    return {"message": "Contact us page would be here"}

@app.post("/contact_us")
async def create_contact_us(contact_data: dict):
    return {"contact_data": contact_data, "status": "Contact information submitted successfully"}

@app.put("/contact_us")
async def update_contact_us(contact_data: dict):
    return {"contact_data": contact_data, "status": "Contact information updated successfully"}

@app.delete("/contact_us")
async def delete_contact_us():
    return {"message": "Contact information deleted successfully"}


   
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host= "0.0.0.0", port=8000)
                

