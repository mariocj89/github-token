from __future__ import print_function
import github_token
import getpass

try:
    input = raw_input
except NameError:
    pass


def main():
    user = input("Username: ")
    password = getpass.getpass()
    app_name = input("App Name to create: ")
    token_factory = github_token.TokenFactory(user, password, app_name,
                                              github_token.ALL_SCOPES)

    print(token_factory(
        tfa_token_callback=lambda: input("TFA Token: ")
    ))

if __name__ == '__main__':  # pragma: no cover
    exit(main())
