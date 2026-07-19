import redis
from config import MAX_REQUEST_LIMIT,RATE_LIMIT_WINDOW
import time
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def check_rate_limit(ip :str) -> bool:
    now = time.time()
    print(now)
    user = r.hgetall(ip)
    if user:
        if  int(user["NUM_REQUESTS"]) <= 0:
            if 60 > now - float(user["LAST_REQUEST_TIME"]): 
                return False
            else:
                r.hset(ip,mapping={
                "NUM_REQUESTS": MAX_REQUEST_LIMIT,
                "LAST_REQUEST_TIME": now
                }) 
                r.hincrby(ip, "NUM_REQUESTS", -1)
            return True
    else:
        r.hset(ip,mapping={
        "NUM_REQUESTS": MAX_REQUEST_LIMIT,
        "LAST_REQUEST_TIME": now
        }) 
    r.hincrby(ip, "NUM_REQUESTS", -1)
    return True
