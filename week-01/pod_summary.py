pods = [
    {"name": "api-1", "status": "Running", "restarts": 6},
    {"name": "api-2", "status": "CrashLoopBackOff", "restarts": 8},
    {"name": "worker-1", "status": "Pending", "restarts": 7},
]


def summarize_pods(pods):
    summary = {
        "total": len(pods),
        "by_status": {},
        "unhealthy": [],
    }

    for pod in pods:
        status = pod.get("status", "Unknown")
        name = pod.get("name", "unknown")
        restarts = pod.get("restarts", 0)

        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1

        if status != "Running" or restarts > 5:
            summary["unhealthy"].append(name)

    return summary


result = summarize_pods(pods)
print(result)