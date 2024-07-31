# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
from typing import BinaryIO, List, Optional, Sequence, Tuple, cast  # noqa: F401

from aptly_api.base import AptlyAPIException, BaseAPIClient


class FilesAPISection(BaseAPIClient):
    def list(self, directory: Optional[str] = None) -> Sequence[str]:
        resp = self.do_get("api/files") if directory is None else self.do_get(f"api/files/{directory}")
        return cast(List[str], resp.json())

    def upload(self, destination: str, *files: str) -> Sequence[str]:
        to_upload = []  # type: List[Tuple[str, BinaryIO]]
        for f in files:
            if not os.path.exists(f) or not os.access(f, os.R_OK):
                msg = f"File to upload {f} can't be opened or read"
                raise AptlyAPIException(msg)
            fh = open(f, mode="rb")  # noqa: SIM115
            to_upload.append(
                (f, fh),
            )

        try:
            resp = self.do_post(f"api/files/{destination}", files=to_upload)
        finally:
            for _fn, to_close in to_upload:
                if not to_close.closed:
                    to_close.close()

        return cast(List[str], resp.json())

    def delete(self, path: Optional[str] = None) -> None:
        self.do_delete(f"api/files/{path}")
