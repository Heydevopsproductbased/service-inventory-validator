import logging
from collections import Counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",

)

logger = logging.getLogger(__name__)

def build_cluster_report(pods:list[dict],restart_threshold:int =5) -> dict:
    status_counts = Counter()
    unhealthy_pods = []
    high_restart_pods = []

    for pod in pods:
        name =pod.get("name" , "unnames pods")
        status =pod.get("status" , "Unknown")
        restarts =pod.get("restarts" , 0)

        status_counts[status] += 1

        if status != "Running":
            unhealthy_pods.append(
                {
                    "name" : name,
                    "status" : status,
                    "restarts" : restarts
                }
            )
        if restarts > restart_threshold:
            high_restart_pods.append(
            {
                "name": name,
                "restarts": restarts,
            }
        )

    return {
                "total_pods": len(pods),
                "status_counts": dict(status_counts),
                "unhealthy_pods": unhealthy_pods,
                "high_restart_pods": high_restart_pods,
            }

def print_cluster_report(report: dict) -> None:
            logger.info("Cluster Health Report")
            logger.info("---------------------")
            logger.info("Total pods: %s", report["total_pods"])
            logger.info("Status counts: %s", report["status_counts"])

            logger.info("Unhealthy pods:")
            if report["unhealthy_pods"]:
                for pod in report["unhealthy_pods"]:
                    logger.info(
                                "- %s: %s, restarts=%s",
                                pod["name"],
                                pod["status"],
                                pod["restarts"],
                                )
            else:
                    logger.info("-None")

            logger.info("High restart alerts:")
            if report["high_restart_pods"]:
                for pod in report["high_restart_pods"]:
                    logger.info(
                        "- %s: %s restarts",
                        pod["name"],
                        pod["restarts"],
                        )
            else:
                logger.info("- None")


def main() -> None:

    pods = [
        {"name" : "web-1" , "status" : "Running" , "restarts" : 3},
        {"name" : "web-2" , "status" : "Running" , "restarts" : 1},
        {"name" : "web-3" , "status" : "CrashLoopBackoff" , "restarts" : 8},
        {"name" : "api-1" , "status" : "Pending" , "restarts" : 1},
        {"name" : "api-2" , "status" : "failed" , "restarts" : 3},
        {"name" : "cache-3" , "status" : "Running" ,"restarts" : 0},
        ]
    report = build_cluster_report(pods)
    print_cluster_report(report)

if __name__ == "__main__":
    main()