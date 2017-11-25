from __future__ import print_function
import github_token
import getpass


def main():
    user = input("Username: ")
    password = getpass.getpass()
    app_name = input("App Name to create: ")
    token_factory = github_token.TokenFactory(user, password, app_name,
                                              github_token.ALL_SCOPES)

    print(token_factory())


if __name__ == '__main__':  # pragma: no cover
    exit(main())
