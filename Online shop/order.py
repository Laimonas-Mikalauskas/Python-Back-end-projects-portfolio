from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Order Catalog!"}

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

@app.review("/orders/{order_id}")
async def review_order(order_id: int, review_data: dict):
    return {"order_id": order_id, "review_data": review_data, "status": "Order reviewed successfully"}

@app.complete("/orders/{order_id}")
async def complete_order(order_id: int, order_data: dict):
    return {"order_id": order_id, "order_data": order_data, "status": "Order completed successfully"}

@app.post("/orders/{order_id}/return")
async def return_order(order_id: int):
    return {"order_id": order_id, "status": "Order returned successfully"}


@app.patch("/orders/{order_id}")
async def patch_order(order_id: int, order_data: dict):
    return {"order_id": order_id, "order_data": order_data, "status": "Order partially updated successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)