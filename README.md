# Slack Inbox Manager Bot

A small Slack app that acts as a posting identity for an AI sales-assistant routine. When a cold-email prospect sends an interested reply, the routine drafts a response and the bot posts it in the Slack thread. Your team then edits it in the thread and approves it with a reaction:

- **Draft to send**: the proposed email, plus a 0–8 lead score
- reply in thread → **Updated draft**
- :white_check_mark: → **Sending…** → **Sent** (via your email platform's API)
- :x: → skipped

Nothing goes to a prospect without an approval.

## What's here

| Path | Purpose |
| --- | --- |
| `manifest.json` | Slack app manifest (bot user + scopes) |
| `scripts/imb_post.py` | Post a message or add a reaction as the bot (token from `SLACK_BOT_TOKEN`) |
| `docs/WORKFLOW.md` | The routine logic that drives the bot (triggers, scoring, draft/approve/send) |
| `app.js`, `app-oauth.js`, `listeners/` | Bolt for JavaScript app skeleton (optional; extend if you want in-app handlers) |
| `tests/` | Listener tests |

## Setup

1. **Create the Slack app**: go to https://api.slack.com/apps → *Create New App* → *From a manifest*, then paste `manifest.json`.
2. **Install** it to your workspace and copy the **Bot User OAuth Token** (`xoxb-…`).
3. **Invite** the bot to your interested-replies channel: `/invite @Inbox Manager Bot`.
4. **Env vars**: `cp .env.sample .env` and fill in the values. At minimum, set `SLACK_BOT_TOKEN`. The workflow also expects `INBOX_API_KEY` for your sending platform.
5. **Run**
   - Posting script (what the routine uses):
     ```bash
     export SLACK_BOT_TOKEN=xoxb-...
     python3 scripts/imb_post.py post payload.json
     python3 scripts/imb_post.py react <CHANNEL_ID> <TS> white_check_mark
     ```
   - Optional Bolt app: `npm install && npm start` (Socket Mode needs `SLACK_APP_TOKEN`; enable it in the manifest first).
   - Tests: `npm test`

## How the routine drives it

An agent routine listens to the channel where your reply notifier posts interested replies, and also listens for :white_check_mark: and :x: reactions. For each new reply, it reads the conversation from your email platform, scores the lead, writes a draft and posts it with `imb_post.py`. Edits and reactions in the thread drive the redraft and send steps. See [docs/WORKFLOW.md](docs/WORKFLOW.md) for the full logic, which you can drop into any agent or automation tool.

## Security

Never commit `.env`, tokens or per-prospect data. `.gitignore` excludes `.env*` (except `.env.sample`).

## License

MIT, see `LICENSE`.
