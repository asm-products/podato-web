import logging

from flask import render_template
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
@session.require
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':

        client_id = kwargs.get('client_id')
        client = clients.Client.get_by_id(client_id)
        kwargs['client'] = client

        if client.app.trusted == True:
            return True #we don't ask the user for permissions for our own "trusted" app.

        return render_template('oauthorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'
