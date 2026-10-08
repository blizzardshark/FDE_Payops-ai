
from uuid import uuid4

from fastapi import FastAPI , HTTPException

from pydantic import BaseModel, Field

from typing import Literal

app = FastAPI()

# Orders store karne ke liye
orders = []

# Payments store karne ke liye
payments = []

class Order(BaseModel):
    orderID: str
    amount: float = Field(gt=0)
    currency: Literal["INR","USD","EUR"]

class OrderUpdate(BaseModel):
    amount:float|None = Field(default=None,gt=0)
    currency: Literal["INR","USD","EUR"]|None=None


# Payment request model
class PaymentRequest(BaseModel):
    orderID: str

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

    order_data["status"] = "CREATED"      

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



# Acctual Post/Payment endpoint create karna
@app.post("/payments",status_code=201)
def initiate_payment(request: PaymentRequest):

    for order in orders:

        if order["orderID"] == request.orderID:

            if order["status"] != "CREATED":

                raise HTTPException(
                    status_code=409,
                    detail="Payment cannot be initiated for this order."
                )

            payment = {
                "paymentID":f"PAY-{uuid4()}",
                "orderID":order["orderID"],
                "amount":order["amount"],
                "currency":order["currency"],
                "status":"PENDING"

            }

            payments.append(payment)

            order["status"]="PENDING"

            return{
                "message":"Payment initiated successfully.",
                "payment":payment
            }
    
    raise HTTPException(
        status_code=404,
        detail="Order not found."
    )


# Payment list inspect karne ke liye endpoint crete karna.
@app.get("/payments")
def get_payments():
    return{
        "payments":payments
    }


# Specific payment fetch karne ke liye endpoints.
@app.get("/payments/{paymentID}")
def get_payments(paymentID:str):
    for payment in payments:
        if payment["paymentID"]==paymentID:
            return payment

    raise HTTPException(
        status_code=404,
        detail="Payment not found."
    )