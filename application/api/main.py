from fastapi import FastAPI
from application.api.endpoints.v1 import customer_endpoints, employee_endpoints, game_endpoints, order_endpoints

app = FastAPI(
    title="Game Store API",
    description="API for managing a game store, including customers, employees, games, and orders.",
    version="1.0.0",
    contact={
        "name": "Support Team",
        "email": "support@gamestore.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(customer_endpoints.router, prefix="/customers", tags=["Customers"])
app.include_router(employee_endpoints.router, prefix="/employees", tags=["Employees"])
app.include_router(game_endpoints.router, prefix="/games", tags=["Games"])
app.include_router(order_endpoints.router, prefix="/orders", tags=["Orders"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
