Python 3 Aptly API client
=========================

This is a fork of the the original aptly-api-client library. It has interfaces
to some of the newer aptly interfaces as well as some interfaces that are
unsupported by `upstream <https://github.com/gopythongo/aptly-api-client/?`__.

It is a dropin replacement for aptly-api-client.

.. code-block:: shell

    pip install aptly-api-client-fork


Usage
-----
The library provides a direct abstraction of the published Aptly API, mostly
using the same naming, only replacing it with pythonic naming where necessary.
All code has full `PEP 484 <https://www.python.org/dev/peps/pep-0484/>`__
annotations, so if you're using a modern IDE, using this library should be
especially straight-forward.

Where appropriate, the library exposes the interface of the underlying
``requests`` library. This allows you to configure CA pinning, SSL client
certificates, HTTP Basic authentication etc.

.. code-block:: python

    # initialize a client
    from aptly_api import Client
    aptly = Client("http://aptly-endpoint.test/")

    # create a repository
    aptly.repos.create("myrepo", comment="a test repo",
                       default_distribution="mydist",
                       default_component="main")

    # upload a package
    aptly.files.upload("test_folder", "/tmp/mypkg_1.0_amd64.deb")

    # add the package to the repo
    aptly.repos.add_uploaded_file("myrepo", "test_folder")

License
=======

Copyright (c) 2016-2019, Jonas Maurus and Contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
