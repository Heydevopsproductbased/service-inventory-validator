
import argparse
import logging
import sys
logging.basicConfig(
level=logging.INFO,
format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

def classify_disk(usage: int) -> str:
       if usage < 75:
           return "OK"
       elif usage < 90:
           return "WARNING"
       else:
           return "CRITICAL"

def main() -> int:
    parser = argparse.ArgumentParser(
         description= "Classify disk usage as OK/WARNING/CRITICAL."
    )

    parser.add_argument(
     "--usage", type=int,
    required=True,
    help="Disk usage percentage (0-100).",
    )

    args = parser.parse_args()

    usage = args.usage

    if usage < 0 or usage > 100:
     logger.error("Invalid usage: %s (must be 0-100)", usage)
     return 2

    status = classify_disk(usage)
    logger.info("Disk usage: %d%%  -> %s", usage ,status)

    if status == "OK":
       return 0
    elif status == "WARNING":
       return 1
    else:
       return 2

if __name__ == "__main__":
 sys.exit(main())
