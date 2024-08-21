from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from aptly_api.base import HTTP_CODE_200, AptlyAPIException, BaseAPIClient


class State(Enum):
    IDLE = 0
    RUNNING = 1
    SUCCEEDED = 2
    FAILED = 3

class Task(NamedTuple):
    task_id: int
    name: str
    state: State

class TasksAPISection(BaseAPIClient):

    def list(self) -> list[Task]:
        resp = self.do_get("api/tasks")

        if resp.status_code != HTTP_CODE_200:
            msg = f"Unexpected status_code : {resp.status_code}"
            raise AptlyAPIException(msg)
        # GET tasks -> 200

        data = []
        resp_json = resp.json()
        if resp_json is None:
            return data

        for x in resp_json:
            task = Task(
                task_id = x["ID"],
                name = x["Name"],
                state = State(x["State"])
                )
            data.append(task)

        return data

    # Deletes given completed task from the list. If none specified clears all finished tasks
    def clear(self, task_to_clear:  Task | None) -> None:
        if task_to_clear is not None:
            pass
            # DELETE tasks/# -> 200 400 500
        else:
            # POST tasks-clear -> 200
            pass

        raise NotImplementedError

    # Wait for specified task to finish before returning.
    # If no task is given for task_to_wait_for then wait for all tasks to complete.
    def wait(self, task_to_wait_for: Task | None) -> None:
        if task_to_wait_for is not None:
            # GET tasks/id#/wait -> 200
            raise NotImplementedError
        else:
            raise NotImplementedError
            # GET tasks-wait -> 200 400 500

    def show(self, task_to_show: Task) -> Task:
        # GET tasks/#id -> 200 404 500
        raise NotImplementedError

    def output(self, task_to_get_output_for: Task) -> None:
        # GET tasks/#id/output -> 200 404 500
        raise NotImplementedError

    def detail(self, task_to_get_details_for: Task) -> None:
        # GET tasks/#id/detail -> 200 404 500
        raise NotImplementedError

    def return_value(self, task_to_get_return_value_for: Task) -> None:
        # GET tasks/id#/return_value -> 200 404 500
        raise NotImplementedError

