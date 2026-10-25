import argparse
import json
import logging
import sys
from pathlib import Path
import yaml


log = logging.getLogger(__name__)

class ConfigError(Exception):
    """Raised when the configuration has a problem."""
def load_config(path: Path) -> dict:
    """Read a config file and check required keys."""
    try:
        extension = path.suffix.lower()

        if extension not in {".json", ".yaml", ".yml"}:
            raise ValueError("Please use a JSON or YAML file")

        log.debug("Opening file: %s", path)

        with path.open(encoding="utf-8") as file:
                if extension == ".json":
                    data = json.load(file)
                else:
                    data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValueError("The config must contain a dictionary")

        required = {"name", "replicas" , "region"}
        missing = required - data.keys()

        if missing:
            raise ValueError(f"Missing settings: {sorted(missing)}")

        log.debug("Name and replicas are present")
        return data

    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise ConfigError(f"Cannot read {path}: {exc}") from exc


def main() -> int:
    """Read and display command-line arguments."""
    parser = argparse.ArgumentParser(description="Check a config file")

    parser.add_argument("path",type=Path, help="Path to the config file")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s : %(message)s",
    )

    try:
        log.info("Starting Config Check")
        load_config(args.path)
        log.info("Config is Valid")
        return 0
    except ConfigError as exec:
        log.error("%s",exec)
        return 1


if __name__ == "__main__":
    sys.exit(main())