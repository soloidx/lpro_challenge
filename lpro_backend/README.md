# Loan Pro challenge

## Description

This is a Python (Django) project for an API implementation of a calculator with authentication and api rate limit per request

## Requeriments

- Python 3.9+
- Poetry

## Installation in development

- Install and activate the poetry environment in the directory:
  ```shell 
  poetry install
  poetry shell
  ```
  
- Configure the environment variables, you can export or create an environment file named `.env`, you can use the file `env.example` as example.
  
### Testing:

The project currently uses `Pytest` as a tool for testing you can run tests with:

```shell
pytest
```
it also has a coverage near to the 90%


## Live server:
There is a live server configured in a AWS lambda instance, for access to the API service you can go to:

https://zmm1wgh21d.execute-api.us-east-1.amazonaws.com/dev/

### API Documentation:
I am using openapi documentation, you can look at it on: https://zmm1wgh21d.execute-api.us-east-1.amazonaws.com/dev/docs

### Authentication:
For testing purposes, I created a single user:

```
username: guest@mail.com
password: easypass
```

If you want to authenticate to the API service, you need to generate a oauth token using:

```shell
curl -X POST \
    -d "grant_type=password" \
    -d "username=guest@mail.com" \
    -d "password=easypass" \
    -u"bwqrE6J5xPX2IjA1YiawqvkvIGdbSjmq3jAq4heB:FYMsyshE4w8EOdsTZxWyDQ2XUlcBCstEgcjKULuDVEHKrLdomYgWyP81zyVw9dwBSDuLhK3qZJrLl2fjJeNhWH91xd7yUqlhhwbebQ1H1MvF5Q1B0YE9UqP0JIAdcWLb" \
    https://zmm1wgh21d.execute-api.us-east-1.amazonaws.com/dev/o/token/
```

You will receive a json document like this:

```json
{
  "access_token": "apphfkaaLo4kyBIx4harEKCb173uwE",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "read write",
  "refresh_token": "W3kYrcOQU3Mcwu6j0JcpvI3F20yuWJ"
}
```

and you can use the token from the `access_token` field as the `Bearer` token for the `Authentication` header

### Admin access:

for admin access you will go to the link: https://zmm1wgh21d.execute-api.us-east-1.amazonaws.com/dev/admin/ and use:

```text
username: admin@fakemail.com
password: th1$i$af4k3passw0rd
```
