"""Github Token

This is an utility to ease the process of accessing the GitHub API
by allowing a painless creation of application tokens.

Those tokens can be used as just passwords when interating with the API.
A much more secure way than storing an user password.
"""
import enum
import functools
import operator
import platform

import requests
import six.moves

DEFAULT_API_URL = "https://api.github.com/"


class Scopes(enum.Enum):
    repo = ["repo", "admin:repo_hook"]
    org = ["admin:org", "admin:org_hook"]
    user = ["user"]
    gist = ["gist"]
    keys = ["admin:public_key", "admin:gpg_key"]


Scopes.all = functools.reduce(operator.concat, [s.value for s in Scopes], [])
ALL_SCOPES = Scopes.all


def _default_tfa_callback():
    return six.moves.input("TFA Token Required: ")


class AlreadyExistsError(Exception):
    """Indicates the app already exists. Delete it first if you want a new token"""


class TFARequired(Exception):
    """Indicates the client needs to provide a TFA token

    This will be sent to the user if this exception was raised"""


class BadPassword(Exception):
    """Indicates the client needs to provide a TFA token

    This will be sent to the user if this exception was raised"""


class TokenFactory(object):
    """Factory class to create a token"""

    def __init__(self, user, password, app_name, scopes, api_url=DEFAULT_API_URL):
        """Creates the factory to send the request and create the token

        :param user: username to auth in github
        :param password: user password for github
        :param app_name: name of the app to create
        :param scopes: scopes required by the app
        :param api_url: base API url for the github API, override for enterprise github
        """
        self.user = user
        self.password = password
        self.api_url = api_url
        self.app_name = app_name
        self.scopes = scopes
        self.tfa_token = None

    def tfa(self, tfa_token):
        """Method to call if a TFA is requested

        This is the usual case after calling create and it
        raising a TFARequired exception. Once this is done next call
        to create will use it
        """
        self.tfa_token = tfa_token

    def create(self):
        """Creates a token

        It uses the app_name as the notes and the scopes are
        the permissions required by the application. See those
        in github when configuring an app token

        Raises a TFARequired if a two factor is required after
        the atempt to create it without having call tfa before
        """
        headers = dict()
        if self.tfa_token:
            headers["X-GitHub-OTP"] = self.tfa_token
        token_name = self.app_name + platform.node()  # node specific in case the user has multiple hosts
        payload = dict(note=token_name, scopes=self.scopes)
        response = requests.post(
                self.api_url + "authorizations", auth=(self.user, self.password),
                headers=headers, json=payload
        )

        if response.status_code == 401 and "required" in response.headers.get("X-GitHub-OTP", ""):
            raise TFARequired("TFA required for the user")
        if response.status_code == 422:
            raise AlreadyExistsError("APP already exists. Please delete {} token".format(token_name))
        if response.status_code == 401:
            raise BadPassword("Bad User/Password")
        response.raise_for_status()
        return response.json()["token"]

    def __call__(self, tfa_token_callback=_default_tfa_callback):
        """Given a callback does all the work for you :)

        This function will attempt to create a the new authorization and
        if the user has Two Factor Authorization configured it will call
        the tfa_token_callback to get it.

        :param tfa_token_callback: Callback that returns the user TFA token
        should be deleted
        :returns: The app token that can be used to authenticate as the user
        """
        try:
            return self.create()
        except TFARequired:
            tfa_token = tfa_token_callback()
            self.tfa(tfa_token)
            return self.create()

