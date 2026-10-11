from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Shipment Tracking Web App!"}

@app.get("/shipments/{shipment_id}")
async def read_shipment(shipment_id: int):
    return {"shipment_id": shipment_id, "status": "Shipment details would be here"}

@app.post("/shipments/")
async def create_shipment(shipment_data: dict):
    return {"shipment_data": shipment_data, "status": "Shipment created successfully"}


@app.post("/shipments/{shipment_id}")
async def update_shipment(shipment_id: int, shipment_data: dict):
    return {"shipment_id": shipment_id, "shipment_data": shipment_data, "status": "Shipment updated successfully"}

@app.patch("/shipments/{shipment_id}")
async def patch_shipment(shipment_id: int, shipment_data: dict):
    return {"shipment_id": shipment_id, "shipment_data": shipment_data, "status": "Shipment partially updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
