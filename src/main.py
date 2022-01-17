import logging
import secrets
from typing import Dict

import aioredis
from dynaconf import settings
from fastapi import FastAPI, Request

from src.templates import ui_scrum_pocker, ui_elections, ui_elections_result

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

app = AsyncApp()
app_handler = AsyncSlackRequestHandler(app)

redis = aioredis.from_url(settings.REDIS.HOST, decode_responses=True)


async def add_user(context_id: str, username: str, value: str) -> None:
    async with redis.client() as conn:
        await conn.hset(context_id, mapping={f"{username}": f"{value}"})
        await conn.expire(context_id, settings.redis.ttl)


async def get_all_users(context_id: str) -> Dict:
    async with redis.client() as conn:
        items = await conn.hgetall(context_id)
        return items


def extract_channel_and_message(body: Dict) -> Dict:
    channel = body["channel"]["id"]
    message_ts = body["container"]["message_ts"]
    return channel, message_ts


async def make_ui(title, is_hidden=True):
    users = await get_all_users(title)
    users = {user: ':see_no_evil:' for user in users.keys()} if is_hidden else users
    ui = ui_scrum_pocker(title, users)
    return ui


@app.event("message")
async def handle_message_events(body, logger):
    logger.info(body)


@app.action("static_select-action")
async def handle_select_action(ack, body, client, logger):
    await ack()
    username = body["user"]["name"]
    value = [action['selected_option']['value'] for action in body['actions'] if 'selected_option' in action][0]
    title = [item['text']['text'] for item in body['message']['blocks'] if 'header' in item['type']][0]
    await add_user(title, username, value)
    ui = await make_ui(title)
    channel, message_ts = extract_channel_and_message(body)
    await client.chat_update(ts=message_ts,
                             channel=channel,
                             blocks=ui["blocks"])
    logger.info(body)


@app.action("action_click")
async def handle_some_action(ack, body, client, logger):
    await ack()
    title = [item['text']['text'] for item in body['message']['blocks'] if 'header' in item['type']][0]
    users = await get_all_users(title)
    is_hidden = True
    if body['user']['name'] in users.keys():
        is_hidden = False
    ui = await make_ui(title, is_hidden=is_hidden)
    channel, message_ts = extract_channel_and_message(body)
    await client.chat_update(ts=message_ts,
                             channel=channel,
                             blocks=ui["blocks"])


@app.command("/start")
async def handler_start_command(ack, body, respond, logger):
    await ack()
    logger.info(body)
    ui = ui_elections()
    await respond(blocks=ui['blocks'])


@app.action("multi_users_select-action")
async def handle_some_action(ack, body, logger):
    await ack()
    logger.info(body)


@app.action("checkboxes-action")
async def handle_some_action(ack, body, logger):
    await ack()
    logger.info(body)


@app.action("election_button-action")
async def handle_some_action(ack, body, say, logger):
    await ack()
    users = list()
    actions = list()
    for item in body['state']['values'].values():
        if 'multi_users_select-action' in item:
            users = item['multi_users_select-action']['selected_users']
        if 'checkboxes-action' in item:
            actions = item['checkboxes-action']['selected_options']

    result = list()
    for action in actions:
        if action['value'] == 'mentor':
            icon = ':microphone:'
        elif action['value'] == 'caden':
            icon = ':writing_hand:'
        elif action['value'] == 'screen':
            icon = ':tv:'
        user = secrets.choice(users)
        result.append(f'{icon} <@{user}>  {action["text"]["text"]}')
        users.remove(user)

    ui = ui_elections_result('\n'.join(result))
    await say(blocks=ui['blocks'])
    logger.info(body)


@app.command("/poker")
async def command_poker(ack, body, say, command):
    ui = await make_ui(title=command["text"])
    await ack()
    await say(blocks=ui["blocks"])


api = FastAPI()


@api.post("/slack/events")
async def endpoint(request: Request):
    return await app_handler.handle(request)


@api.get("/slack/install")
async def install(request: Request):
    return await app_handler.handle(request)


@api.post("/slack/auth")
async def oauth_redirect(request: Request):
    return await app_handler.handle(request)


@api.post("/slack/start")
async def start(request: Request):
    return await app_handler.handle(request)


@api.post("/slack/poker")
async def poker(request: Request):
    return await app_handler.handle(request)


@api.post("/slack/message_action")
async def message_action(request: Request):
    return await app_handler.handle(request)
