import json
import sys
from pathlib import Path

from corebank_api.main import create_app


def main() -> None:
    output_path = Path(sys.argv[1])
    output_path.write_text(
        json.dumps(create_app().openapi(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
