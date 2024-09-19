import time

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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define request model
class Item(BaseModel):
    name: str
    description: str = None


def some_function():
    time.sleep(5)
    return "some_function"



@app.post("/items/")
async def create_item(item: Item, request: Request):
    logger.info(f"Received request to create item: {item.name}")

    # Process the item (in this example, we're just returning it)
    result = {"item": item.dict(), "client_host": request.client.host}

    st = time.time()
    some_function()
    duration = time.time() - st
    logger.info(f"some function took: {duration}")

    logger.info(f"Item created successfully: {item.name}")
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")