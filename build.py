from pathlib import Path
import argparse
import re
import yaml
from weasyprint import HTML, CSS


def load_card(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    data["phone_tel"] = re.sub(r"[^\d+]", "", data["phone"])
    return data


def render(template, data):
    text = template
    for key, value in data.items():
        text = text.replace("{{ " + key + " }}", str(value))
    return text


def main():
    parser = argparse.ArgumentParser(description="Build electronic business card PDF")
    parser.add_argument("source", help="YAML card content")
    parser.add_argument("-o", "--output", required=True, help="Output PDF")
    args = parser.parse_args()

    root = Path(__file__).parent
    data = load_card(root / args.source)

    html_template = (root / "template/card.html").read_text(encoding="utf-8")
    html = render(html_template, data)

    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)

    HTML(string=html, base_url=str(root / "template")).write_pdf(
        out,
        stylesheets=[CSS(filename=root / "template/card.css")]
    )

    print(out)


if __name__ == "__main__":
    main()
