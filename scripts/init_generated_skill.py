from __future__ import annotations

import argparse
from pathlib import Path

from skillify_runtime import BookBrief, init_generated_skill, read_data_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a standard generated skill directory for a book.")
    parser.add_argument("--skills-root", default="skills", help="Directory that contains generated skills.")
    parser.add_argument("--book-brief", help="Path to a JSON/YAML-like book brief file.")
    parser.add_argument("--title")
    parser.add_argument("--author")
    parser.add_argument("--domain")
    parser.add_argument("--audience")
    parser.add_argument("--goal")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--force", action="store_true", help="Overwrite placeholder files when the directory already exists.")
    return parser


def resolve_book_brief(args: argparse.Namespace) -> BookBrief:
    if args.book_brief:
        payload = read_data_file(Path(args.book_brief))
    else:
        payload = {
            "title": args.title,
            "author": args.author,
            "domain": args.domain,
            "audience": args.audience,
            "goal": args.goal,
            "language": args.language,
        }
    book = BookBrief.from_mapping(payload)
    missing = [field for field, value in vars(book).items() if not value]
    if missing:
        raise SystemExit(f"Missing required book brief fields: {', '.join(missing)}")
    return book


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    book = resolve_book_brief(args)
    target = init_generated_skill(book, Path(args.skills_root), force=args.force)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
