OXCT: Open edX Community Tools
==============================

WARNING: this is a work-in-progress. If you are an active Open edX community member and you have ideas to improve this repo, please feel free to open a pull request!

This package includes tools to publish information about the Open edX community.

Installation
------------

::

    pip install https+git://github.com/openedx/oxct.git

Usage
-----

List community members::

    oxct community members list

List core committers::

    oxct community members list --tag=corecommitter

Display a particular community member::

    oxct community members show nedbat

Running in production
---------------------

::
    docker-compose build
    docker-compose up -d

Then point a webserver to localhost:5000. Note that the cache will certainly have to be warmed up. To do so, hit the following endpoint: /community/members.

Development
-----------

Run a local Redis instance::

    make dev-redis

Run a development web server::

    make dev-server

Check that the server works by running::

    curl localhost:5000/community/members/nedbat

Point the ``oxct`` client to your local instance::

    oxct --host=http://localhost:5000 community members show nedbat

Run tests (requires a running Redis instance)::

    make test

Server API endpoints
--------------------

The oxct server exposes the following endpoints:

* ``/community/members``: it's possible to search members by tag by passing the ``?tag=...`` query string. For instance: ``?tag=corecommitter``.
* ``/community/members/<username>``
* ``/community/tags``

Architecture
------------

The oxct server relies on a Redis cache to store information collected from the `Open edX forums <https://discuss.openedx.org>`__. Basically, the Discourse API is crawled to extract community information. To make sure that the server cache is always fresh, all cache entries expire with a TTL between 10 seconds and 24 hours. An asynchronous pub/sub worker listens for expire events to recompute data on-the-fly.

TODO
----

- Get rid of all TODO statements
- Better client output
- ... whatever you can think of to improve this!

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://www.gnu.org/licenses/agpl-3.0.en.html>`_.
