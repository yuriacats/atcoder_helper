"""Tests for init_task."""


from typing import Type

import mock
import pytest

from atcoder_helper.models.atcoder_helper_config import AtCoderHelperConfig
from atcoder_helper.models.atcoder_helper_config import LanguageConfig
from atcoder_helper.repositories.errors import CopyError
from atcoder_helper.repositories.errors import DirectoryNotEmpty
from atcoder_helper.repositories.errors import ParseError
from atcoder_helper.repositories.errors import ReadError
from atcoder_helper.repositories.errors import WriteError
from atcoder_helper.services.errors import ConfigAccessError
from atcoder_helper.services.init_task import InitTaskDirServiceImpl


def _get_config() -> AtCoderHelperConfig:
    return AtCoderHelperConfig(
        languages={"fooLang": LanguageConfig(name="fooLang", build=[], run=[])},
        default_language="fooLang",
    )


def _get_sut(
    atcoder_helper_repo_mock: mock.MagicMock, task_config_repo_mock: mock.MagicMock
) -> InitTaskDirServiceImpl:
    return InitTaskDirServiceImpl(
        atcoder_helper_config_repo=atcoder_helper_repo_mock,
        task_config_repo=task_config_repo_mock,
    )


test_init_task_parameters = {
    "OK": [
        mock.MagicMock(read=mock.MagicMock(return_value=_get_config())),
        mock.MagicMock(),
        None,
    ],
    "error(language configの取得に失敗)": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ReadError)),
        mock.MagicMock(),
        ConfigAccessError,
    ],
    "error(language configのパースに失敗)": [
        mock.MagicMock(read=mock.MagicMock(side_effect=ParseError)),
        mock.MagicMock(),
        ConfigAccessError,
    ],
    "error(ディレクトリが空でない)": [
        mock.MagicMock(read=mock.MagicMock(return_value=_get_config())),
        mock.MagicMock(write=mock.MagicMock(side_effect=DirectoryNotEmpty())),
        ConfigAccessError,
    ],
    "error(タスク設定ファイルに書き込めない)": [
        mock.MagicMock(read=mock.MagicMock(return_value=_get_config())),
        mock.MagicMock(write=mock.MagicMock(side_effect=WriteError())),
        ConfigAccessError,
    ],
    "error(テンプレートのコピーに失敗)": [
        mock.MagicMock(read=mock.MagicMock(return_value=_get_config())),
        mock.MagicMock(write=mock.MagicMock(side_effect=CopyError())),
        ConfigAccessError,
    ],
}


@pytest.mark.parametrize(
    argnames=("atcoder_helper_config_repo_mock", "task_config_repo_mock", "exception"),
    argvalues=test_init_task_parameters.values(),
    ids=test_init_task_parameters.keys(),
)
def test_init_task(
    atcoder_helper_config_repo_mock: mock.MagicMock,
    task_config_repo_mock: mock.MagicMock,
    exception: Type[Exception],
) -> None:
    """Test for init_task."""
    dir = "fooDir"
    contest = "fooContest"
    task = "fooTask"

    sut = InitTaskDirServiceImpl(atcoder_helper_config_repo_mock, task_config_repo_mock)

    if exception:
        with pytest.raises(exception):
            sut.init_task(dir, contest, task)
    else:
        sut.init_task(dir, contest, task)
