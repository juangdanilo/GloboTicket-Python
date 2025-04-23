import re
from pathlib import Path
from typing import Any, Dict

import yaml

FRONTMATTER_DIRECTORY = Path(__file__).parent.parent / "product_info"


def get_frontmatter(product_code: str) -> Dict[str, Any]:
    """
    Read the frontmatter for event with given product_code,
    and return the properties as a dict.
    """
    frontmatter_path = find_frontmatter_file(product_code, FRONTMATTER_DIRECTORY)
    frontmatter_content = frontmatter_path.read_text(encoding="utf-8")
    return parse_frontmatter(frontmatter_content)


def find_frontmatter_file(product_code: str, frontmatter_dir: Path) -> Path:
    """
    Find a file called 'product_code'.yml in frontmatter_dir
    and return its path.

    Raises FileNotFoundError if not found for this product_code.
    """
    matches = list(frontmatter_dir.glob(f"**/{product_code}.yml"))
    if not matches:
        raise FileNotFoundError(
            f"File not found for product code: {product_code} in {frontmatter_dir}"
        )
    return matches[0]


class InvalidFrontmatterError(Exception):
    """Exception raised when frontmatter is invalid."""

    pass


FRONTMATTER_REGEX = re.compile(
    r"^---\n(?P<yaml>.*?)---\n(?P<content>.*)",  # Regex para capturar YAML y contenido
    re.DOTALL,
)


def parse_frontmatter(frontmatter: str) -> Dict[str, Any]:
    """
    Return the content of the frontmatter as a dict.

    Raises an InvalidFrontmatterError if the structure is invalid.
    """
    match = FRONTMATTER_REGEX.match(frontmatter)
    if not match:
        raise InvalidFrontmatterError("Invalid file structure")

    try:
        data = yaml.load(match.group("yaml"), Loader=yaml.FullLoader)
        if not isinstance(data, dict):
            raise InvalidFrontmatterError("YAML content must be a dictionary")
        data["content"] = match.group("content")
    except (yaml.YAMLError, TypeError) as e:
        raise InvalidFrontmatterError("Invalid YAML (should be a dict)") from e

    return data
