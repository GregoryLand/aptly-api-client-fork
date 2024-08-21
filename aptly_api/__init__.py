# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# explicit exports for mypy
from aptly_api.base import AptlyAPIException
from aptly_api.client import Client
from aptly_api.parts.packages import Package
from aptly_api.parts.publish import PublishEndpoint
from aptly_api.parts.repos import FileReport, Repo
from aptly_api.parts.snapshots import Snapshot
from aptly_api.parts.tasks import State, Task

version = "0.2.5"


__all__ = ["Client", "AptlyAPIException", "version", "Package", "PublishEndpoint", "Repo", "FileReport", "Snapshot", "State", "Task"]
