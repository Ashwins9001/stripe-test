# Motivation #
Doing this project to learn about back-end development and to play around more with a Stripe payments integration.

# Overview #
Project currently shows a placeholder inventories page of three different products with varying inventories, prices. Upon selecting the 'buy' option for any, user gets redirected to sandbox Stripe payment page to complete transaction. When transaction is successful, then a locally running webhook is triggered to update the underlying item inventory and it fails if inventory is at zero. 

Project uses following technologies
- Docker
- Stripe payments API
- Flask
- HTML/Jinja2