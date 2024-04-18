from typing import Annotated
from fastapi import Header, HTTPException, Request, status
from datetime import datetime
from app.utils.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_token_header(x_token: Annotated[str, Header()]):
    pass
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    
async def validate_token(request: Request):
    token_in_query = request.query_params.get("token")
    token_in_header = request.headers.get("x-token")

    if not token_in_query and not token_in_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token in query parameter or header",
        )

    # Implement your token validation logic here (e.g., verify against a database)
    # Replace with your actual validation logic
    if token_in_query != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token provided",
        )

    # If validation passes, add the token to the request object (optional)
    request.state.token = token_in_query or token_in_header


DBSessionDep = Annotated[AsyncSession, Depends(get_db)]