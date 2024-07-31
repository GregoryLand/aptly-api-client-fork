# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from typing import cast

import requests

from aptly_api.base import AptlyAPIException, BaseAPIClient

HTTP_CODE_200: int = 200
HTTP_CODE_404: int = 404
HTTP_CODE_503: int = 503


class MiscAPISection(BaseAPIClient):
    def graph(self, ext: str, layout: str = "horizontal") -> None:  # noqa: ARG002
        msg = "The Graph API is not yet supported"
        raise NotImplementedError(msg)

    def version(self) -> str:
        resp = self.do_get("api/version")
        if "Version" in resp.json():
            return cast(str, resp.json()["Version"])
        msg = f"Aptly server didn't return a valid response object:\n{resp.text}"
        raise AptlyAPIException(msg)

    def _do_get_clear_404(self) -> requests.Response:
        try:
            return self.do_get("api/ready")
        except AptlyAPIException as error:
            # This is needed to hide the exception masking the 404 error
            if error.status_code == HTTP_CODE_404:
                msg = "The Ready API is not yet supported"
                raise NotImplementedError(msg) from error
            # 503 is needed by api/ready for returning its unready condition
            if error.status_code not in {HTTP_CODE_200, HTTP_CODE_503}:
                msg = f"Aptly server returned an unexpected status_code {error.status_code}"
                raise AptlyAPIException(msg) from error
            raise

    def ready(self) -> str:
        resp = self._do_get_clear_404()

        if "Status" not in resp.json():
            msg = f"Aptly server didn't return a valid response object:\n{resp.text}"
            raise AptlyAPIException(msg)

        return cast(str, resp.json()["Status"])

    def healthy(self) -> str:
        try:
            resp = self.do_get("api/healthy")
            if "Status" in resp.json():
                return cast(str, resp.json()["Status"])
            msg = f"Aptly server didn't return a valid response object:\n{resp.text}"
            raise AptlyAPIException(msg)
        except ValueError as error:
            msg = "The Healthy Api is not yet supported"
            raise NotImplementedError(msg) from error

    def metrics(self) -> str:
        try:
            resp = self.do_get("api/metrics")
        except AptlyAPIException as error:
            if error.status_code == HTTP_CODE_404:
                raise NotImplementedError from error
            raise

        if resp.status_code != HTTP_CODE_200:
            raise AptlyAPIException(self._error_from_response(resp), status_code=resp.status_code)

        return resp.text
