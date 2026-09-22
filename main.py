


from fastapi import FastAPI , HTTPException

from pydantic import BaseModel, Field

from typing import Literal

app = FastAPI()


orders = []

class Order(BaseModel):
    orderID: str
    amount: float = Field(gt=0)
    currency: Literal["INR","USD","EUR"]


@app.get("/")

def home():
    return{
        "message": "PayOps AI Payment Service is running"
    }



#Create order API


@app.post("/orders")
def create_order(order: Order):
    order_data = order.model_dump()

    for existing_order in orders :
        if existing_order["orderID"] == order_data["orderID"]:

           raise HTTPException(
               status_code = 409,
               detail=f"Order with ID'{order_data['orderID']}'already exists."
           )

    orders.append(order_data)

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