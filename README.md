# raco-notifier

## creating app

 * register a new application
 * add redirect url: `http://localhost:12983`
 * Choose application type: Authorization code
 * create a `secrets/raco_app.json` file with the keys `client_id` and `client_secret` and add the corresponding values

## generate token

Run the `api_token.py` script to generate a token. The token will then be refreshed automatically.