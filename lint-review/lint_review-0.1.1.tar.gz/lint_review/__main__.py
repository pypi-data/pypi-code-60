"""Main entry point for lint review cli."""
import argparse
import re
import sys
import typing

from .gitlab import GitlabReviewer, add_gitlab_args
from .reviewer import Comment, DryReviewer, Reviewer

premade_patterns = {
    "flake8": r"(?P<path>[^:]+):(?P<line>\d+):(?P<col>\d+): (?P<message>.+)",
    "mypy": r"(?P<path>[^:]+):(?P<line>\d+): error: (?P<message>.+)",
}

reviewers: typing.Dict[str, typing.Callable[[argparse.Namespace], Reviewer]] = {
    "dry": lambda _args: DryReviewer(),
    "gitlab": GitlabReviewer.from_args,
}

required_groups = {"line", "path", "message"}


def _parse_args(argv: typing.Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--linter", choices=premade_patterns, help="Name of the linter to use",
    )
    parser.add_argument(
        "--reviewer",
        help="The service used to review the code",
        choices=reviewers,
        required=True,
    )
    parser.add_argument(
        "--custom_pattern",
        help=f"""A custom regex pattern to capture comments.
         The pattern must have the named capture groups:
         {required_groups} and optionally col""",
    )

    add_gitlab_args(parser)

    return parser.parse_args(argv)


def _get_comments(
    source: typing.Iterable[str], pattern: re.Pattern
) -> typing.Iterator[Comment]:
    for line in source:
        match = pattern.match(line)
        if match:
            groups = match.groupdict()
            groups["line"] = int(groups["line"])
            groups["col"] = int(groups["col"])
            yield Comment(**groups)


def _get_pattern(args: argparse.Namespace) -> re.Pattern:
    """Extract the comment pattern from user arguments."""
    if args.linter:
        if args.linter not in premade_patterns:
            raise KeyError(
                f"{args.linter} is not yet supported, please use --custom_pattern"
            )
        return re.compile(premade_patterns[args.linter])
    if not args.custom_pattern:
        raise ValueError(
            "No linter pattern given, pass either --linter or --custom_pattern"
        )
    return _create_custom_pattern(args.custom_pattern)


def _create_custom_pattern(pattern: str) -> re.Pattern:
    custom_pattern = re.compile(pattern)
    if not required_groups.issubset(custom_pattern.groupindex.keys()):
        raise ValueError(
            f"Custom pattern must include the capture groups {required_groups}"
        )
    return custom_pattern


def _review(args: argparse.Namespace) -> int:
    """Posts a review. Returns the amount of unresolved comments."""
    reviewer = reviewers[args.reviewer](args)
    fresh_comments = _get_comments(source=sys.stdin, pattern=_get_pattern(args))
    relevant_comments = {
        comment
        for comment in fresh_comments
        if comment.line in reviewer.get_changed_lines()[comment.path]
    }
    posted_comments = set(reviewer.get_existing_comments())
    for comment in relevant_comments - posted_comments:
        reviewer.post_comment(comment)
        print(comment, file=sys.stderr)
    for comment in posted_comments - relevant_comments:
        reviewer.resolve_comment(comment)
    return len(relevant_comments - posted_comments)


def main():
    """Main entry point for cli script."""
    args = _parse_args(sys.argv[1:])
    sys.exit(_review(args))


if __name__ == "__main__":
    main()
