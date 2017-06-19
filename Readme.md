# Messenger bot in Python with AWS lambda and zappa

## Overview

Create a messenger chatbot powered by an AWS lambda in python 3.6 and zappa

This tutorial has been made on :
- Windows 10
- Amazon Web Services (AWS) account 5use the free tier)
- install virtualenv (can work with anaconda/miniconda) and python 3.6

## Process
**Facebook application setup**
- Setup a [Facebook application](https://developers.facebook.com) in the developer
- Add a messenger product in the application
![Image](pictures\setup_app.png)
- Create a Facebook page
![Image](pictures\create_facebook_page.png)
- Add a "send message" button to the page
![Image](pictures\add send message button.png)
- Select the page that you have created (and accept the your profile have access blah blah)
![Image](pictures\settings_messenger_product.png)
- Keep the access token that has been assigned

**Flask application Setup**
- Create a virtual environment with the command virtualenv in my case **zappa_env**
- Activate the environment `activate zappa_env`
- Install with pip `pip install zappa flask awscli`
- Clone the content of this git in a separate folder of your environment
![Image](pictures\environnment.png)
- Replace the `access_token` in the application.py file by the access token of your application

**Deploy the application on AWS**
- You need to create a user on your AWS account that will have the administrator access
- Use the command `zappa init` in your project folder

In this tutorial you can accept the default parameter that zappa offer you to complete the process:
![Image](pictures\zappa_init.png)
  1. environment name : dev
  2. S3 bucket name : random name
  3. available for all region : n

- Check if in your project folder there is a zappa_settings.json file
- Your application is now initialize so we can deploy the app with the command `zappa deploy dev`
![Image](pictures\zappa_deploy_dev.png)
Let's the magic begin (take a break , have a kitkat)

**Finish to complete the Facebook application setup**

On the messenger settings page you have to setup the webhooks
- Copy paste the url of your app on the callback url field
- Create a verify token (be imaginative or not)
- Verify and save
- Subscribe the webhook to your facebook page events
![Image](pictures\subscribe_webhook.png)

**Update you application**

- To finish you need to update the `verify_token` variable on the application.py files by the token that you create previously
- Update the app with the command
`zappa update dev`

**Test it**

![Image](pictures\test_bot.png)


## Ressources
- [Facebook Messenger Bot Tutorial: Step-by-Step Instructions for Building a Basic Facebook Chat Bot](https://blog.hartleybrody.com/fb-messenger-bot/) by Hartley Brody
- [First step with zappa flask and Python 3](https://andrich.blog/2017/02/12/first-steps-with-aws-lambda-zappa-flask-and-python/) by Oliver Andrich
- [Zappa](https://www.zappa.io/)
