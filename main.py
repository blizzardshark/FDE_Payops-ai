


from fastapi import FastAPI , HTTPException

from pydantic import BaseModel

app = FastAPI()


orders = []

class Order(BaseModel):
    orderID: str
    amount: float
    currency: str


@app.get("/")

def home():
    return{
        "message": "PayOps AI Payment Service is running"
    }



#Create order API


@app.post("/orders")
def create_order(order:Order):
    order_data = order.model_dump()
    orders.append(order)

    return{
        "message": "Order Created Successfully.",
        "order": order_data
    }


# Order retrieve karna


@app.get("/orders")
def get_orders():
    return{
        "orders": orders
    }

# OrderId se order dhundhna

@app.get("/orders/{orderID}")
def get_orders(orderID: str):
    for order in orders:
        if order["orderID"] == orderID:
            return order

    raise HTTPException(
        status_code=404,
        detail=f"Order with ID '{orderID}' not found."
    )