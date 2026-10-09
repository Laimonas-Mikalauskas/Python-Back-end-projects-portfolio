try:
    from fastapi import FastAPI
except ImportError:
    raise RuntimeError("FastAPI is not installed. Install it with 'pip install fastapi'.")

app = FastAPI()
@app.get("/")
async def read_root():
    return {"pipes": "Welcome to the Shopping Cart!"}


@app.post("/")
async def create_app(item_data: dict):
    return {"item_data": item_data, "status": "App created successfully"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(name: str):
    return {"name": name}

@app.sort("/pipes/{pipe_id}")
async def sort_pipe(pipe_id: int, name: str):
    return {"pipe_id": pipe_id, "name": name, "status": "Pipe sorted successfully"}

@app.add_to_cart("/pipes/{pipe_id}")
async def add_to_cart(pipe_id: int, name: str):
    return {"pipe_id": pipe_id, "name": name, "status": "Pipe added to cart successfully"}

@app.delete_cart("/pipes/{pipe_id}")
async def delete_pipe(pipe_id: int):
    return {"pipe_id": pipe_id, "status": "Pipe deleted successfully"}

@app.update_cart("/pipes/{pipe_id}")
async def update_pipe(pipe_id: int, name: str):
    return {"pipe_id": pipe_id, "name": name, "status": "Pipe partially updated successfully"}



if __name__ == "__main__":
    app.run(debug=True)

    
    

