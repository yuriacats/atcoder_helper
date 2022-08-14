"""テストケース実行のためのメソッド."""

import subprocess
from textwrap import indent
from typing import List
from typing import Protocol

from atcoder_helper.models.test_case import AtcoderTestCase
from atcoder_helper.models.test_case import TestResult
from atcoder_helper.models.test_case import TestStatus
from atcoder_helper.repositories import errors as repository_error
from atcoder_helper.repositories.task_config_repo import TaskConfigRepository
from atcoder_helper.repositories.task_config_repo import (
    get_default_task_config_repository,
)
from atcoder_helper.repositories.test_case_repo import TestCaseRepository
from atcoder_helper.repositories.test_case_repo import get_default_test_case_repository
from atcoder_helper.services.errors import ConfigAccessError


class ExecuteTestService(Protocol):
    """テストを実行するサービス."""

    def execute_test(self) -> None:
        """testcaseに基づき、テストを実行する関数.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """


def get_default_execute_test_service() -> ExecuteTestService:
    """ExecuteTestServiceの標準実装を返す.

    Returns:
        ExecuteTestService:
    """
    return ExecuteTestServiceImpl()


class ExecuteTestServiceImpl:
    """テストを実行するサービス."""

    _task_config_repo: TaskConfigRepository
    _test_case_repo: TestCaseRepository

    def __init__(
        self,
        task_config_repo: TaskConfigRepository = get_default_task_config_repository(),
        test_case_repo: TestCaseRepository = get_default_test_case_repository(),
    ):
        """__init__.

        Args:
            task_config_repo (TaskConfigRepository, optional): Defaults to
                get_default_task_config_repository().
            test_case_repo (TestCaseRepository, optional): Defaults to
                get_default_test_case_repository().
        """
        self._task_config_repo = task_config_repo
        self._test_case_repo = test_case_repo

    def execute_test(self) -> None:
        """testcaseに基づき、テストを実行する関数.

        Raises:
            ConfigAccessError: 設定ファイル読み書きのエラー
        """
        try:
            task_config = self._task_config_repo.read()
            test_cases = self._test_case_repo.read()
        except repository_error.ReadError:
            raise ConfigAccessError("設定ファイルの読み込みに失敗しました")

        subprocess.run(task_config.build)  # TODO(ビルド失敗で止まるようにする)

        results = self._execute_and_show(test_cases, task_config.run)
        self._show_summary(results)

    def _execute_and_show(
        self, test_cases: List[AtcoderTestCase], run_command: List[str]
    ) -> List[TestResult]:

        results = []
        for test_case in test_cases:
            print("-----------------------------------")
            result = test_case.execute(run_command)
            print(f"{test_case.name:<15}: {result.status.dyed}")
            results.append(result)

            if result.status == TestStatus.JUSTSHOW:
                print("    output:")
                print(indent(result.actual, "       >"))
            if result.status == TestStatus.ERROR:
                print(result.error)
            if result.status == TestStatus.WA:
                if result.expected is None:
                    raise Exception("internal error")

                print("    expected:")
                print(indent(result.expected, "       >"))
                print("    but got:")
                print(indent(result.actual, "       >"))

        return results

    def _show_summary(self, results: List[TestResult]) -> None:
        print("========================================")
        print("SUMMARY:")
        for result in results:
            print(f"{result.name:<15}: {result.status.dyed}")
