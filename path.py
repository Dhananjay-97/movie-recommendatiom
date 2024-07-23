import logging
from fastapi import FastAPI, APIRouter, HTTPException
from neo4j import GraphDatabase, basic_auth
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default Neo4j database configuration
DEFAULT_NEO4J_URI = "bolt://localhost:7687"
DEFAULT_NEO4J_USER = "neo4j"
DEFAULT_NEO4J_PASSWORD = "password"

# Create FastAPI instance
app = FastAPI()

# Create a router instance
router = APIRouter()

# Pydantic models
class Node(BaseModel):
    id: int
    labels: List[str]
    properties: Dict[str, str]  # Dictionary of property names to their types

class DbCredentials(BaseModel):
    uri: Optional[str] = DEFAULT_NEO4J_URI
    user: Optional[str] = DEFAULT_NEO4J_USER
    password: Optional[str] = DEFAULT_NEO4J_PASSWORD

# Create Neo4j driver
def get_neo4j_driver(credentials: DbCredentials):
    logger.info(f"Initializing Neo4j driver with URI: {credentials.uri}")
    driver = GraphDatabase.driver(credentials.uri, auth=basic_auth(credentials.user, credentials.password))
    return driver

# Determine the property type
def determine_type(value):
    if isinstance(value, datetime):
        return "datetime"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, bool):
        return "boolean"
    else:
        return "string"

# Fetch nodes from Neo4j
def fetch_nodes_from_neo4j(driver):
    query = "MATCH (n) RETURN n LIMIT 10"
    logger.info("Fetching nodes from Neo4j")
    with driver.session() as session:
        result = session.run(query)
        nodes_list = []
        for record in result:
            node = record["n"]
            properties = {key: determine_type(value) for key, value in node.items()}
            nodes_list.append(Node(
                id=node.id,
                labels=node.labels,
                properties=properties
            ))
        logger.info(f"Fetched nodes: {nodes_list}")
        return nodes_list

# Define the endpoint to fetch nodes
@router.post("/nodes", response_model=List[Node])
async def get_nodes(credentials: DbCredentials = DbCredentials()):
    try:
        logger.info("Received request to fetch nodes")
        driver = get_neo4j_driver(credentials)
        nodes = fetch_nodes_from_neo4j(driver)
        return nodes
    except Exception as e:
        logger.error(f"Error fetching nodes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.close()
        logger.info("Closed Neo4j driver")

# Include the router in the FastAPI app
app.include_router(router, prefix="/api")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
