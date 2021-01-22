from flask import Flask, abort, request

from oxct.common import exceptions

from . import community

app = Flask("oxct")


@app.route("/community/members")
def community_members():
    """
    Search by tag is possible. For instance:

        ?tag=corecommitter
    """
    # TODO: pagination? sorting?
    tag = request.args.get("tag")
    return {
        "members": [
            member.as_dict()
            for member in community.iter_members()
            if tag is None or tag in member.tags
        ]
    }


@app.route("/community/members/<username>")
def community_member(username):
    try:
        return community.find_member(username).as_dict()
    except exceptions.OxctNotFoundError:
        abort(404)


@app.route("/community/tags")
def community_tags():
    return {"tags": community.list_tags()}
