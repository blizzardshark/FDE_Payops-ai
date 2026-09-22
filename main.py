


from fastapi import FastAPI , HTTPException

from pydantic import BaseModel, Field

from typing import Literal

app = FastAPI()


orders = []

class Order(BaseModel):
    orderID: str
    amount: float = Field(gt=0)
    currency: Literal["INR","USD","EUR"]

class OrderUpdate(BaseModel):
    amount:float|None = Field(default=None,gt=0)
    currency: Literal["INR","USD","EUR"]|None=None

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


# Partially Update karne ke liye
@app.patch("/orders/{orderID}")
def update_order(orderID:str , updated_order: OrderUpdate):

   for order in orders:

       if order["orderID"] == orderID:
          update_data = updated_order.model_dump(exclude_none=True)
          order.update(update_data)

          return{
            "message":"Order updated successfully.",
            "order": order
          }

   raise HTTPException(
        status_code = 404,
        detail= f"Order with ID '{orderID}' not found."
    )

# Existing order delete karna
@app.delete("/orders/{orderID}")
def delete_order(orderID: str):

    for order in orders:
        if order["orderID"] == orderID:
            orders.remove(order)

            return{
                "message":f"Order '{orderID}' deleted successfully."
            }

    raise HTTPException(
        status_code=404,
        detail=f"Order with ID '{orderID}' not found."
    )