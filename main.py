import logging
import re

from fastapi import FastAPI, Request
from icecream import ic

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)


@app.event("app_mention")
async def handle_app_mention(body, say, logger):
    logger.info(say)
    await say('What up?')


@app.event("message")
async def handle_message():
    pass


@app.event("reaction_added")
async def reaction(body, say, logger):
    await say("Kuku")


@app.message(re.compile("(hi|hello|hey)"))
async def ping(message, say):
    ic(message)
    user = message['user']
    say(f"Hi there, <@{user}>!")


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
