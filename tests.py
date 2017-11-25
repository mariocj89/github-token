import os

try:
    from unittest.mock import ANY
except ImportError:
    from mock import ANY

import requests_mock
import pytest

import github_token
from github_token import TokenFactory, Scopes, DEFAULT_API_URL


def register_uri(mock, method, url, *args, **kwargs):
    """Registers an url on requests_mock ensure the full url was passed"""
    absolute_url = os.path.join(DEFAULT_API_URL, url)
    mock.register_uri(method, absolute_url, *args, **kwargs)


def register_token_creation(mock, token, **kwargs):
    register_uri(mock, "POST", url="authorizations",
                 json=dict(token=token), **kwargs)


@pytest.fixture
def factory():
    return TokenFactory(
        user="mariocj89",
        password="fake_password",
        app_name="testapp",
        scopes=Scopes.all,
    )


def test_create_token_succeeds(factory):
    with requests_mock.mock() as mock:
        register_token_creation(mock, "token")
        assert "token" == factory.create()


def test_create_token_fails_tfa_required(factory):
    with requests_mock.mock() as mock:
        register_uri(mock, "POST", url="authorizations", status_code=401,
                     headers={"X-GitHub-OTP": "required"})
        with pytest.raises(github_token.TFARequired):
            factory.create()


def test_create_call_with_tfa(factory):
    with requests_mock.mock() as mock:
        register_uri(mock, "POST", "authorizations", [
            dict(status_code=401, headers={"X-GitHub-OTP": "required"}),
            dict(json=dict(token="token")),
        ])

        assert "token" == factory(lambda: "tfa-code")
        assert mock.call_count == 2


def test_create_token_arguments(factory):
    def match_scope(request):
        return all(
            s in request.json()["scopes"]
            for s in ["user", "repo", "admin:org"]
        )

    with requests_mock.mock() as mock:
        register_token_creation(
            mock, "token",
            additional_matcher=match_scope
        )
        assert "token" == factory.create()

