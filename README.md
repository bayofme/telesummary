## Installation

Script was tested on Python 3.12.6, so it is the recommended version.

It is also recommended to user virtualenv and/or pyenv.

To install requirements, run the following:

```shell
pip install -r requirements.txt
```

## Usage

## Configuration

Create the following environment variables:

- `TELESUMMARY_APP_ID` - Telegram App api_id
- `TELESUMMARY_APP_API_HASH` - Telegram App api_hash

Those values you can find here: https://my.telegram.org/apps

### List chats

```shell
python telesummary/main.py list
```

Example of output:

```text
-00004568087239		test
```

where the first column is ID of chat, and `test` is the name of chat.

### Get messages from a chat

```shell
python telesummary/main.py summary -00004568087239
```

where `-00004568087239` is chat ID.

Example of output:

```text
# Message from Some User at 2024-10-16 20:28:21
7

# Message from Some User at 2024-10-16 20:28:21
8

# Message from Some User at 2024-10-16 20:28:22
9

# Message from Some User at 2024-10-16 20:28:23
10

# Message from Some User at 2024-10-16 20:28:23
11

# Message from Some User at 2024-10-16 20:28:24
12

# Message from Some User at 2024-10-16 20:28:24
12

# Message from Some User at 2024-10-16 20:28:25
13

# Message from Some User at 2024-10-16 20:28:27
14
```

### Delete messages from a chat

```shell
python telesummary/main.py delete -00004562087131 --limit=1
```

The default limit is 100, and oldest messages are deleted first.

Example of output:

```text
7

Proceed? (answer yes): 
```

You need to answer yes to proceed.

To see command help, use the following:

```shell
python telesummary/main.py delete -- --help
```
