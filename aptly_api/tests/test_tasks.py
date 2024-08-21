from typing import Any
from unittest.case import TestCase

import requests_mock

from aptly_api.parts.tasks import State, Task, TasksAPISection


@requests_mock.Mocker(kw="rmock")
class TasksAPISectionTests(TestCase):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.tapi = TasksAPISection("http://test/")

    def test_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/tasks",
                  text='[{"ID":4,"Name":"1234","State":0},{"ID":1,"Name":"1","State":1},{"ID":3,"Name":"df","State":2},{"ID":2,"Name":"asdf","State":3}]')
        data = [
                   Task(4, "1234", State.IDLE),
                   Task(1, "1", State.RUNNING),
                   Task(3, "df", State.SUCCEEDED),
                   Task(2, "asdf", State.FAILED),
               ]
        returned_list = self.tapi.list()
        assert data == returned_list

    def test_empty_list(self, *, rmock: requests_mock.Mocker) -> None:
        rmock.get("http://test/api/tasks", text='[]')
        data = []
        returned_list = self.tapi.list()
        assert data == returned_list

    def test_clear(self, *, rmock: requests_mock.Mocker) -> None:
        raise NotImplementedError

    def test_wait(self, *, rmock: requests_mock.Mocker) -> None:
        raise NotImplementedError

    def test_show(self, *, rmock: requests_mock.Mocker) -> None:
        raise NotImplementedError

    def test_output(self, *, rmock: requests_mock.Mocker) -> None:
        raise NotImplementedError

    def test_detail(self, *, rmock: requests_mock.Mocker) -> None:
        raise NotImplementedError

    def test_return_vaule(self, *, rmock: requests_mock.Mocker) -> None:
        raise NotImplementedError

