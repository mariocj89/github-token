# GitHub Token
Creating an app token might not be the simplest task, use this utility and forget
about all the issues.

# Install
```pip install github_token```

# Usage
```
    import github_token
    user = input("Username: ")
    password = getpass.getpass()
    app_name = input("App Name to create: ")
    token_factory = github_token.TokenFactory(user, password, app_name,
                                              github_token.ALL_SCOPES)

    print(token_factory(
        tfa_token_callback=lambda: input("TFA Token: ")
    ))
```
