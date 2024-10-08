# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime
from typing import Dict, List, NamedTuple, Optional, Sequence, Union, cast
from urllib.parse import quote

import iso8601

from aptly_api.base import AptlyAPIException, BaseAPIClient
from aptly_api.parts.packages import Package, PackageAPISection


class Snapshot(NamedTuple):
    name: str
    description: Optional[str]
    created_at: Optional[datetime]


class SnapshotAPISection(BaseAPIClient):
    @staticmethod
    def snapshot_from_response(api_response: Dict[str, Union[str, None]]) -> Snapshot:
        return Snapshot(
            # use a cast() here as `name` can never be None, but the `api_response` declaration can't handle that
            name=cast(str, api_response["Name"]),
            description=api_response["Description"] if "Description" in api_response else None,
            created_at=iso8601.parse_date(cast(str, api_response["CreatedAt"]))
            if "CreatedAt" in api_response
            else None,
        )

    def list(self, sort: str = "name") -> Sequence[Snapshot]:
        if sort not in ["name", "time"]:
            msg = f"Snapshot LIST only supports two sort modes: 'name' and 'time'. {sort} is not supported."
            raise AptlyAPIException(msg)
        resp = self.do_get("api/snapshots", params={"sort": sort})
        ret = []
        for rsnap in resp.json():
            ret.append(self.snapshot_from_response(rsnap))
        return ret

    def create_from_repo(self, reponame: str, snapshotname: str, description: Optional[str] = None) -> Snapshot:
        body = {
            "Name": snapshotname,
        }
        if description is not None:
            body["Description"] = description

        resp = self.do_post(f"api/repos/{quote(reponame)}/snapshots", json=body)
        return self.snapshot_from_response(resp.json())

    def create_from_mirror(self, mirrorname: str, snapshotname: str, description: Optional[str] = None) -> Snapshot:
        body = {"Name": snapshotname}
        if description is not None:
            body["Description"] = description

        resp = self.do_post(f"api/mirrors/{quote(mirrorname)}/snapshots", json=body)
        return self.snapshot_from_response(resp.json())

    def create_from_packages(
        self,
        snapshotname: str,
        description: Optional[str] = None,
        source_snapshots: Optional[Sequence[str]] = None,
        package_refs: Optional[Sequence[str]] = None,
    ) -> Snapshot:
        body = {
            "Name": snapshotname,
        }  # type: Dict[str, Union[str, Sequence[str]]]
        if description is not None:
            body["Description"] = description

        if source_snapshots is not None:
            body["SourceSnapshots"] = source_snapshots

        if package_refs is not None:
            body["PackageRefs"] = package_refs

        resp = self.do_post("api/snapshots", json=body)
        return self.snapshot_from_response(resp.json())

    def update(
        self, snapshotname: str, newname: Optional[str] = None, newdescription: Optional[str] = None
    ) -> Snapshot:
        if newname is None and newdescription is None:
            msg = "When updating a Snapshot you must at lease provide either a new name or a new description."
            raise AptlyAPIException(msg)
        body = {}  # type: Dict[str, Union[str, Sequence[str]]]
        if newname is not None:
            body["Name"] = newname

        if newdescription is not None:
            body["Description"] = newdescription

        resp = self.do_put(f"api/snapshots/{quote(snapshotname)}", json=body)
        return self.snapshot_from_response(resp.json())

    def show(self, snapshotname: str) -> Snapshot:
        resp = self.do_get(f"api/snapshots/{quote(snapshotname)}")
        return self.snapshot_from_response(resp.json())

    def list_packages(
        self, snapshotname: str, query: Optional[str] = None, with_deps: bool = False, detailed: bool = False
    ) -> Sequence[Package]:
        params = {}
        if query is not None:
            params["q"] = query
        if with_deps:
            params["withDeps"] = "1"
        if detailed:
            params["format"] = "details"

        resp = self.do_get(f"api/snapshots/{quote(snapshotname)}/packages", params=params)
        ret = []
        for rpkg in resp.json():
            ret.append(PackageAPISection.package_from_response(rpkg))
        return ret

    def delete(self, snapshotname: str, force: bool = False) -> None:
        params = None
        if force:
            params = {
                "force": "1",
            }

        self.do_delete(f"api/snapshots/{quote(snapshotname)}", params=params)

    def diff(self, snapshot1: str, snapshot2: str) -> Sequence[Dict[str, str]]:
        resp = self.do_get(f"api/snapshots/{quote(snapshot1)}/diff/{quote(snapshot2)}")
        return cast(List[Dict[str, str]], resp.json())
