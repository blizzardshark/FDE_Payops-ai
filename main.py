from fastapi import FastAPI , HTTPException

app = FastAPI()

orders = []

@app.get("/")

def home():
    return{
        "message": "PayOps AI Payment Service is running"
    }



#Create order API


@app.post("/orders")
def create_order(order:dict):
    orders.append(order)

    return{
        "message": "Order Created Successfully.",
        "order": order
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
        detail="Order nahi mila."
    )