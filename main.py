import logging

from fastapi import FastAPI, Request

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)


@app.event("app_mention")
async def handle_app_mention(body, say, logger):
    logger.info(say)
    await say('What up?')


# @app.event("message")
# async def handle_message_events(body, logger):
#     logger.info(body)


@app.message("ping")
async def handle_pong(message, say):
    user = message['user']
    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Click Me"},
                "action_id": "button_click"
            }
        }
    ]
    await say(blocks=blocks, text=f"Hi there, <@{user}>!")


@app.action("button_click")
async def action_button_click(body, ack, say):
    # Acknowledge the action
    await ack()
    await say(f"<@{body['user']['id']}> clicked the button")


@app.command("/start")
async def command(ack, body, respond):
    await ack()
    await respond(f"Hi <@{body['user_id']}>!")


api = FastAPI()


@api.post("/slack/events")
async def endpoint(request: Request):
    return await app_handler.handle(request)


@api.get("/slack/install")
async def install(request: Request):
    return await app_handler.handle(request)


@api.post('/slack/auth')
async def oauth_redirect(request: Request):
    return await app_handler.handle(request)


@api.post('/slack/start')
async def start(request: Request):
    return await app_handler.handle(request)


@api.post('/slack/message_action')
async def message_action(request: Request):
    return await app_handler.handle(request)
