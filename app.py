from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
from azure.monitor.opentelemetry import configure_azure_monitor
import os

# Initialize FastAPI app
app = FastAPI()
APPLICATIONINSIGHTS_CONNECTION_STRING = ""



# Configure Azure Monitor OpenTelemetry
connection_string = APPLICATIONINSIGHTS_CONNECTION_STRING
if connection_string:
    configure_azure_monitor(connection_string=connection_string)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add console handler for local debugging
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


# Define request model
class Item(BaseModel):
    name: str
    description: str = None


@app.post("/items/")
async def create_item(item: Item, request: Request):
    logger.info(f"Received request to create item: {item.name}")

    # Process the item (in this example, we're just returning it)
    result = {"item": item.dict(), "client_host": request.client.host}

    logger.info(f"Item created successfully: {item.name}")
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)