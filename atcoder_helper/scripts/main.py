"""atcoder_helperコマンドのエントリポイント."""
import argparse
import os

from atcoder_helper.services.confg_use import config_use
from atcoder_helper.services.config_default_language import config_default_language
from atcoder_helper.services.config_languages import config_languages
from atcoder_helper.services.execute_test import execute_test
from atcoder_helper.services.fetch_task import fetch_task
from atcoder_helper.services.init_config import init_config
from atcoder_helper.services.init_task import init_task


def main() -> None:
    """main."""
    root_parser = argparse.ArgumentParser(description="atcoder の手助けをするコマンド")
    root_parser.set_defaults(parser=root_parser)
    root_subparsers = root_parser.add_subparsers()

    parser_exec = root_subparsers.add_parser("exec")
    parser_exec.set_defaults(handler=_execute_test_handler, parser=parser_exec)

    parser_fetch = root_subparsers.add_parser("fetch")
    parser_fetch.set_defaults(handler=_fetch_task_handler, parser=parser_fetch)
    parser_fetch.add_argument("--contest")
    parser_fetch.add_argument("--task")

    parser_task = root_subparsers.add_parser("task")
    parser_task.set_defaults(parser=parser_task)

    parser_task_subparsers = parser_task.add_subparsers()

    parser_task_init = parser_task_subparsers.add_parser("init")
    parser_task_init.set_defaults(handler=_task_init_handler, parser=parser_task_init)

    parser_task_create = parser_task_subparsers.add_parser("create")
    parser_task_create.set_defaults(
        handler=_task_create_handler, parser=parser_task_create
    )
    parser_task_create.add_argument("contest")
    parser_task_create.add_argument("task")

    parser_config = root_subparsers.add_parser("config")
    parser_config.set_defaults(parser=parser_config)

    parser_config_subparsers = parser_config.add_subparsers()

    parser_config_init = parser_config_subparsers.add_parser("init")
    parser_config_init.set_defaults(
        handler=_config_init_handler, parser=parser_config_init
    )

    parser_config_languages = parser_config_subparsers.add_parser("languages")
    parser_config_languages.set_defaults(
        handler=_config_languages_handler, parser=parser_config_languages
    )

    parser_config_default_language = parser_config_subparsers.add_parser("default")
    parser_config_default_language.set_defaults(
        handler=_config_default_language_handler, parser=parser_config_default_language
    )

    parser_config_use = parser_config_subparsers.add_parser("use")
    parser_config_use.set_defaults(
        handler=_config_use_handler, parser=parser_config_use
    )
    parser_config_use.add_argument("language")

    args = root_parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        args.parser.print_help()


def _task_init_handler(_: argparse.Namespace) -> None:
    init_task(None, None, None)


def _task_create_handler(args: argparse.Namespace) -> None:
    init_task(os.path.join(args.contest, args.task), args.contest, args.task)


def _execute_test_handler(_: argparse.Namespace) -> None:
    execute_test()


def _fetch_task_handler(args: argparse.Namespace) -> None:
    fetch_task(args.contest, args.task)


def _config_init_handler(_: argparse.Namespace) -> None:
    init_config()


def _config_languages_handler(_: argparse.Namespace) -> None:
    languages = config_languages()
    for language_name in languages:
        print(language_name)


def _config_default_language_handler(_: argparse.Namespace) -> None:
    default_language = config_default_language()
    print(default_language.name)


def _config_use_handler(args: argparse.Namespace) -> None:
    config_use(args.language)
