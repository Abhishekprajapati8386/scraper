from fastapi import FastAPI, Query, HTTPException
from app.scraper import scrape_reels
from app.cache import cache

app = FastAPI()

@app.get("/scrape")
def get_reels(username: str, limit: int = Query(20, le=50)):
    print("Script Initiated")
    key = f"{username}_{limit}"
    if key in cache:
        return {"source": "cache", "data": cache[key]}

    try:
        reels = scrape_reels(username, limit)
        cache[key] = reels
        return {"source": "live", "data": reels}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
