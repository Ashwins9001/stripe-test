# Motivation #
Doing this project to learn about back-end development and to play around more with a Stripe payments integration.

# Overview #
Project currently shows a placeholder inventories page of three different products with varying inventories, prices. Upon selecting the 'buy' option for any, user gets redirected to sandbox Stripe payment page to complete transaction. When transaction is successful, then a locally running webhook is triggered to update the underlying item inventory and it fails if inventory is at zero. 

Project uses following technologies
- Docker
- Stripe payments API
- Flask
- HTML/Jinja2

# Project Setup #
1. Open cmd line tab to root directory, install Stripe CLI
2. In same cmd line tab run: stripe login
3. In same cmd line tab run: stripe listen --forward-to localhost:5000/webhook
4. Fetch the returned webhook secret and replace the local STRIPE_WEBHOOK_SECRET environment variable with it
5. Open another cmd line tab to root directory, run docker-compose --build
6. Goto localhost:5000
7. Execute payment, to do dummy transaction pass any details and a valid future expiration date

Need to manually provide webhook secret since it's run locally, normally Stripe will provide a webhook secret for a publically available endpoint, but this project is all locally-run. 