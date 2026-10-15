#!/usr/bin/env python3
"""Post or react as the Inbox Manager Bot.

Usage:
  SLACK_BOT_TOKEN=xoxb-... python3 scripts/imb_post.py post <payload.json>
  SLACK_BOT_TOKEN=xoxb-... python3 scripts/imb_post.py react <channel_id> <ts> <emoji>

payload.json is a chat.postMessage body, e.g.
  {"channel": "<CHANNEL_ID>", "thread_ts": "<PARENT_TS>", "text": "**Draft to send** ..."}

The token is read only from the SLACK_BOT_TOKEN environment variable.
"""
import json
import os
import sys
import urllib.request


def api(method, token, payload):
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise SystemExit("SLACK_BOT_TOKEN is not set")
    if len(sys.argv) < 2:
        raise SystemExit("usage: imb_post.py post <json> | react <channel> <ts> <emoji>")
    cmd = sys.argv[1]
    if cmd == "post" and len(sys.argv) == 3:
        with open(sys.argv[2]) as f:
            out = api("chat.postMessage", token, json.load(f))
    elif cmd == "react" and len(sys.argv) == 5:
        out = api("reactions.add", token, {
            "channel": sys.argv[2], "timestamp": sys.argv[3], "name": sys.argv[4],
        })
    else:
        raise SystemExit("usage: imb_post.py post <json> | react <channel> <ts> <emoji>")
    print(json.dumps({k: out.get(k) for k in ("ok", "ts", "error", "channel")}))
    if not out.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
