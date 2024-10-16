import os
import argparse

import telethon


client = telethon.TelegramClient(
    "telesummary", os.getenv("TELESUMMARY_APP_ID"), os.getenv("TELESUMMARY_APP_API_HASH"))

ACTION_SUMMARY = "summary"
ACTION_DELETE = "delete"
ACTION_LIST = "list"


async def get_messages(chat_id, limit, messages, **kwargs):
    params = {}
    if kwargs.get('oldest_first', False):
        params["reverse"] = True
    if kwargs.get('from_me'):
        params['from_user'] = 'me'
    async for message in client.iter_messages(chat_id, limit=limit, **params):
        messages.append(message)


def action_summary(action_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_id", nargs=1)
    parser.add_argument('--limit', type=int, default=500)
    args = parser.parse_args(action_args)
    chat_id = int(args.chat_id[0])

    raw_messages = []
    with client:
        client.loop.run_until_complete(get_messages(chat_id, args.limit, raw_messages))
    messages = []
    for msg in raw_messages:
        messages.append({
            "text": msg.message,
            "date": msg.date,
            "author": " ".join(filter(None, [msg.sender.first_name, msg.sender.last_name])) if msg.sender else None,
        })
    body = ""
    for msg in reversed(messages):
        if not msg['text']:
            continue
        if not msg['text'].strip():
            continue
        body += "# Message from {} at {}\n".format(
            msg['author'] or 'Unknown', msg['date'].strftime("%Y-%m-%d %H:%M:%S"))
        body += msg['text']
        body += '\n\n'

    print(body)


async def get_chats(chats):
    async for dialog in client.iter_dialogs():
        chats.append(dialog)


def action_list(action_args):
    chats = []
    with client:
        client.loop.run_until_complete(get_chats(chats))
    chats.sort(key=lambda c: c.name)
    for c in chats:
        if c.archived:
            continue
        if c.entity and getattr(c.entity, 'deleted', False):
            continue
        print("{}\t\t{}".format(str(c.id).zfill(15), c.name or c.title))


async def _delete_messages(messages):
    await client.delete_messages(None, message_ids=messages)


def action_delete(action_args):
    parser = argparse.ArgumentParser()
    parser.add_argument("chat_id", nargs=1)
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--newest', action='store_true')
    args = parser.parse_args(action_args)
    chat_id = int(args.chat_id[0])
    messages = []
    oldest_first = True
    if args.newest:
        oldest_first = False
    with client:
        client.loop.run_until_complete(get_messages(
            chat_id, args.limit, messages, oldest_first=oldest_first, from_me=True
        ))

    for msg in messages:
        print(msg.message)
        print()

    answer = input("Proceed? (answer yes): ")
    if answer.lower() != 'yes':
        return

    with client:
        client.loop.run_until_complete(_delete_messages(messages))


ACTIONS = {
    ACTION_SUMMARY: action_summary,
    ACTION_LIST: action_list,
    ACTION_DELETE: action_delete,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs=1, choices=ACTIONS.keys())
    args, action_args = parser.parse_known_args()
    action = args.action[0]
    ACTIONS[action](action_args)


if __name__ == '__main__':
    main()
