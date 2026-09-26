from fastapi import FastAPI
app = FastAPI()
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Customer Account"}

@app.get("/customers/{customer_id}")
async def read_customer(customer_id: int):
    return {"customer_id": customer_id, "status": "Customer details would be here"}

@app.post("/customers/")
async def create_customer(customer_data: dict):
    return {"customer_data": customer_data, "status": "Customer account created successfully"}

@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int, customer_data: dict):
    return {"customer_id": customer_id, "customer_data": customer_data, "status": "Customer account updated successfully"}

@app.delete("/customers/{customer_id}") 
async def delete_customer(customer_id: int):
    return {"customer_id": customer_id, "status": "Customer account deleted successfully"}

@app.get("/billing_info/{customer_id}")
async def read_billing_info(customer_id: int):
    return {"customer_id": customer_id, "status": "Billing info would be here"}

@app.post("/billing_info/")
async def create_billing_info(billing_data: dict):
    return {"billing_data": billing_data, "status": "Billing info created successfully"}

@app.put("/billing_info/{customer_id}")
async def update_billing_info(customer_id: int, billing_data: dict):
    return {"customer_id": customer_id, "billing_data": billing_data, "status": "Billing info updated successfully"}

@app.delete("/billing_info/{customer_id}")
async def delete_billing_info(customer_id: int):
    return {"customer_id": customer_id, "status": "Billing info deleted successfully"}

@app.get("/shipping_info/{customer_id}")
async def read_shipping_info(customer_id: int):
    return {"customer_id": customer_id, "status": "Shipping info would be here"}

@app.post("/shipping_info/")
async def create_shipping_info(shipping_data: dict):
    return {"shipping_data": shipping_data, "status": "Shipping info created successfully"}

@app.put("/shipping_info/{customer_id}")
async def update_shipping_info(customer_id: int, shipping_data: dict):
    return {"customer_id": customer_id, "shipping_data": shipping_data, "status": "Shipping info updated successfully"}

@app.delete("/shipping_info/{customer_id}")
async def delete_shipping_info(customer_id: int):
    return {"customer_id": customer_id, "status": "Shipping info deleted successfully"}
    
@app.get("/payment_info/{customer_id}")
async def read_payment_info(customer_id: int):
    return {"customer_id": customer_id, "status": "Payment info would be here"}

@app.post("/payment_info/")
async def create_payment_info(payment_data: dict):
    return {"payment_data": payment_data, "status": "Payment info created successfully"}

@app.put("/payment_info/{customer_id}")
async def update_payment_info(customer_id: int, payment_data: dict):
    return {"customer_id": customer_id, "payment_data": payment_data, "status": "Payment info updated successfully"}

@app.delete("/payment_info/{customer_id}")
async def delete_payment_info(customer_id: int):
    return {"customer_id": customer_id, "status": "Payment info deleted successfully"}

@app.get("/order_history/{customer_id}")
async def read_order_history(customer_id: int):
    return {"customer_id": customer_id, "status": "Order history would be here"}

@app.post("/order_history/")
async def create_order_history(order_data: dict):
    return {"order_data": order_data, "status": "Order history created successfully"}

@app.put("/order_history/{customer_id}")
async def update_order_history(customer_id: int, order_data: dict):
    return {"customer_id": customer_id, "order_data": order_data, "status": "Order history updated successfully"}

@app.delete("/order_history/{customer_id}")
async def delete_order_history(customer_id: int):
    return {"customer_id": customer_id, "status": "Order history deleted successfully"}

@app.get("/wishlist/{customer_id}")
async def read_wishlist(customer_id: int):
    return {"customer_id": customer_id, "status": "Wishlist would be here"}

@app.post("/wishlist/")
async def create_wishlist(wishlist_data: dict):
    return {"wishlist_data": wishlist_data, "status": "Wishlist created successfully"}

@app.put("/wishlist/{customer_id}")
async def update_wishlist(customer_id: int, wishlist_data: dict):
    return {"customer_id": customer_id, "wishlist_data": wishlist_data, "status": "Wishlist updated successfully"}

@app.delete("/wishlist/{customer_id}")
async def delete_wishlist(customer_id: int):
    return {"customer_id": customer_id, "status": "Wishlist deleted successfully"}

class Customer:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = self.hash_password(password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
    
    def mask_username(self) -> str:
        return self.username[0] + "****" + self.username[-1]

    def update_username(self, new_username: str):
        self.username = new_username

    def verify_username(self, username: str) -> bool:
        return self.username == username

class BillingInfo:
    def __init__(self, billing_address: str, billing_email: str):
        self.billing_address = billing_address
        self.billing_email = billing_email

    def update_billing_info(self, new_billing_address: str, new_billing_email: str):
        self.billing_address = new_billing_address
        self.billing_email = new_billing_email

    def get_billing_info(self):
        return {
            "billing_address": self.billing_address,
            "billing_email": self.billing_email
        }
        
class ShippingInfo:
    def __init__(self, shipping_address: str, shipping_email: str):
        self.shipping_address = shipping_address
        self.shipping_email = shipping_email

    def update_shipping_info(self, new_shipping_address: str, new_shipping_email: str):
        self.shipping_address = new_shipping_address
        self.shipping_email = new_shipping_email

    def get_shipping_info(self):
        return {
            "shipping_address": self.shipping_address,
            "shipping_email": self.shipping_email
        }
        
class PaymentInfo:
    def __init__(self, payment_method: str, card_number: str):
        self.payment_method = payment_method
        self.card_number = card_number

    def update_payment_info(self, new_payment_method: str, new_card_number: str):
        self.payment_method = new_payment_method
        self.card_number = new_card_number

    def get_payment_info(self):
        return {
            "payment_method": self.payment_method,
            "card_number": "****" + self.card_number[-4:]
        }
        
class OrderHistory:
    def __init__(self):
        self.orders = []

    def add_order(self, order: dict):
        self.orders.append(order)

    def get_order_history(self):
        return self.orders
    
class Wishlist:
    def __init__(self):
        self.items = []

    def add_to_wishlist(self, item: dict):
        self.items.append(item)

    def remove_from_wishlist(self, item_id: int):
        self.items = [item for item in self.items if item.get("id") != item_id]

    def get_wishlist(self):
        return self.items
    
                                    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)