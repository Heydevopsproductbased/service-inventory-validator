import logging

logging.basicConfig(
    level = logging.INFO,
    format= "%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

def classify_services(services: dict) -> dict:
    healthy = []
    unhealthy = []

    for service_name, status_code in services.items():
        if 200<= status_code < 300:
            healthy.append(service_name)
        else:
            unhealthy.append(service_name)

    return {
            "healthy": healthy,
            "unhealthy":unhealthy,
            }


def main() -> None:
    services = {
        "payment-api" :200,
        "catalogue-api" :503,
        "fraud-api" :201,
        "inventory-api" :404,
        "notification-api":500,
    }

    result = classify_services(services)
    logger.info("Healthy Services: %s",result["healthy"])
    logger.info("Unhealthy Services: %s",result["unhealthy"])

if __name__ == "__main__":
        main()



