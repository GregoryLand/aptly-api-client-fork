# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Dict, NamedTuple, Optional, Union
from urllib.parse import quote

from aptly_api.base import BaseAPIClient


class Package(NamedTuple):
    key: str
    short_key: Optional[str]
    files_hash: Optional[str]
    fields: Optional[Dict[str, str]]


class PackageAPISection(BaseAPIClient):
    @staticmethod
    def package_from_response(api_response: Union[str, Dict[str, str]]) -> Package:
        if isinstance(api_response, str):
            return Package(
                key=api_response,
                short_key=None,
                files_hash=None,
                fields=None,
            )
        return Package(
            key=api_response["Key"],
            short_key=api_response["ShortKey"] if "ShortKey" in api_response else None,
            files_hash=api_response["FilesHash"] if "FilesHash" in api_response else None,
            fields=api_response,
        )

    def show(self, key: str) -> Package:
        resp = self.do_get(f"api/packages/{quote(key)}")
        return self.package_from_response(resp.json())
