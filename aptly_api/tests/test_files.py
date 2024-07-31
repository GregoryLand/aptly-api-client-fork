# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from typing import Any
from unittest.case import TestCase

import pytest
import requests_mock

from aptly_api.base import AptlyAPIException
from aptly_api.parts.files import FilesAPISection


@requests_mock.Mocker(kw="rmock")
class FilesAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.fapi = FilesAPISection("http://test/")

    def test_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/files", text='["aptly-0.9"]')
        assert self.fapi.list() == ["aptly-0.9"]

    def test_list_dir(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/files/dir", text='["dir/aptly_0.9~dev+217+ge5d646c_i386.deb"]')
        assert self.fapi.list("dir") == ["dir/aptly_0.9~dev+217+ge5d646c_i386.deb"]

    def test_upload_file(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/files/test", text='["test/testpkg.deb"]')
        assert self.fapi.upload("test", os.path.join(os.path.dirname(__file__), "testpkg.deb")) == ["test/testpkg.deb"]

    def test_upload_invalid(self, *, rmock: requests_mock.Mocker) -> None:  # noqa: ARG002
        with pytest.raises(AptlyAPIException):
            self.fapi.upload("test", "noexistant")

    def test_upload_failed(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.post("http://test/api/files/test", text='["test/testpkg.deb"]', status_code=500)
        with pytest.raises(AptlyAPIException):
            self.fapi.upload("test", os.path.join(os.path.dirname(__file__), "testpkg.deb"))

    def test_delete(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.delete("http://test/api/files/test", text="{}")
        self.fapi.delete("test")
