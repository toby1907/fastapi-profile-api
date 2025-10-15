import httpx
from datetime import datetime, timezone
from fastapi import HTTPException
from .config import settings
async def get_cat_fact():
    """
    Fetch a random cat fact from the Cat Facts API
    Returns a tuple: (fact, status, error_message)
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://catfact.ninja/fact")
            
            if response.status_code == 200:
                data = response.json()
                fact = data.get("fact", "No fact available")
                return fact, "success", None
            else:
                error_msg = f"API returned status {response.status_code}"
                return "Unable to fetch cat fact at this time", "api_error", error_msg
                
    except httpx.TimeoutException:
        return "Cat facts service is taking too long to respond", "timeout", "Request timeout"
    except httpx.RequestError as e:
        return "Unable to connect to cat facts service", "connection_error", str(e)
    except Exception as e:
        return "An unexpected error occurred while fetching cat fact", "unknown_error", str(e)
    
# async def get_cat_fact() -> str:
#     """
#     Fetch a random cat fact from the Cat Facts API
#     Returns a fallback message if the API fails
#     """
#     try:
#         async with httpx.AsyncClient(timeout=settings.CAT_FACTS_TIMEOUT) as client:
#             response = await client.get(settings.CAT_FACTS_API_URL)
            
#             if response.status_code == 200:
#                 data = response.json()
#                 return data.get("fact", "No fact available")
#             else:
#                 return "Unable to fetch cat fact at this time"
                
#     except httpx.TimeoutException:
#         return "Cat facts service is taking too long to respond"
#     except httpx.RequestError:
#         return "Unable to connect to cat facts service"
#     except Exception:
#         return "An unexpected error occurred while fetching cat fact"

def get_current_timestamp() -> str:
    """Get current UTC time in ISO 8601 format"""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')