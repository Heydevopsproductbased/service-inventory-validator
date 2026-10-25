pods = [
    {"name": "api-1", "restarts":0},
    {"name": "api-2", "restarts":8},
    {"name": "worker-1", "restarts":5},
    {"name": "worker-2", "restarts":6},
]

def find_restart_alerts(pods, threshold):
    alerts = []

    for pod in pods:
        restarts = pod.get("restarts",0)

        if restarts >= threshold:
            alerts.append(pod["name"])

    return alerts

alerts = find_restart_alerts(pods,5)

print(alerts)