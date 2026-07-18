
from app.services.rate_limit import check_rate_limit


if __name__ == "__main__":
    check_rate_limit("192.168.0.1")
