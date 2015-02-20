import logging

from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

from api import blueprint
from api.oauth import oauth
from api.oauth import clients
from users.auth import session

@blueprint.api_blueprint.route('/oauth/token')
@oauth.token_handler
def access_token():
    pass # We don't need to actually do anything, just attach the handler.


@blueprint.api_blueprint.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    # make sure that we have a user session

    logging.warning("checking user: %s" % session.get_user())

    if not session.get_user():
        next = url_for("api.authorize", **request.args)
        return redirect(url_for("auth.login", next=next))

    if request.method == 'GET':

        client_id = kwargs.get('client_id')
        client = clients.Client.get_by_id(client_id)
        kwargs['client'] = client

        if client.app.trusted == True:
            return True #we don't ask the user for permissions for our own "trusted" app.

        return render_template('oauthorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'
