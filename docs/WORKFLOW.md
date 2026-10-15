# Interested-reply draft workflow

This is the agent routine that drives the Inbox Manager Bot. It runs on an AI agent (any scheduler or event-driven agent works) and uses the bot only as a posting identity, so drafts show up as "Inbox Manager Bot" instead of as a human.

## Trigger

- A new message in `#<INTERESTED_REPLIES_CHANNEL>` (`<CHANNEL_ID>`), posted by your cold-email reply notifier (`<NOTIFIER_USER_ID>`).
- A `:white_check_mark:` or `:x:` reaction in that channel.

## Posting identity

- Post and react as the bot with `scripts/imb_post.py` (`SLACK_BOT_TOKEN` in env). Never post drafts with a personal user token.
- Thread replies: set `channel=<CHANNEL_ID>` and `thread_ts=<PARENT_TS>`.
- Reading the channel can use any Slack reader.

## On a new interested-reply notification

1. Read name, email, company, domain, quoted reply and campaign from the parent message.
2. Skip it if the parent already has `:robot_face:`, `:x:` or `:white_check_mark:`, or the thread already has a current **Draft to send** / **Updated draft**.
3. Skip obvious out-of-office, bounce or "no longer here" replies unless they name a replacement contact.
4. Pull the full conversation from your sending platform's inbox API (`<INBOX_API_BASE>`, workspace `<WORKSPACE_ID>`, key from env `INBOX_API_KEY`).
5. **Score** the lead 0–8 (shown in Slack only, never in the email). Unknown = 0; don't invent headcount.
   - +2 SaaS company (not agency, hardware, real estate, etc.)
   - +2 SaaS with 10–200 employees
   - +2 large TAM (sells into many industries)
   - +2 contact is CEO, founder, CMO or CRO
   - Format: `*Score N/8* · SaaS +2/0 · 10–200 +2/0 · TAM +2/0 · role +2/0`
6. **Lead magnet** (optional): if they asked for a doc/playbook, check `https://<YOUR_DOMAIN>/lead-magnets/<slug>.html`. If it returns 200, link it. If 404, start your build pipeline, draft anyway with **Blocker: page not live**, and don't send until it's live and approved. Never invent a live URL.
7. Write the email in the sender's voice: short, no em dashes, low-effort CTA. On a first reply, hyperlink the call CTA to `<BOOKING_URL>`.
8. Post a thread reply as the bot:

   ```
   **Draft to send** (not in their inbox yet)
   *Score N/8* · SaaS … · 10–200 … · TAM … · role …

   <email copy>

   ---
   React :white_check_mark: to send. Reply here with edits. :x: to skip.
   ```

9. Notify the operator (e.g. a DM) with name / company / score / thread link.

## On an edit reply from an approver

Apply it right away, post **Updated draft** with the full new copy, react `:pencil2:` on the edit message and notify the operator. "send" / "approved" in the reply counts as approval.

## On `:white_check_mark:`

1. Post **Sending…** right away (from mailbox → to address) before calling the API.
2. Send the latest approved copy through the inbox API's send endpoint (`prospect_id`, `subject`, `message`, `to` as an array, `cc`, `bcc`). Keep the booking hyperlink in first replies.
3. Post **Sent** (time + mailbox) or **Send failed** with the error. On success, react `:robot_face:` on the parent. Notify the operator.
4. Never send if a linked lead-magnet URL returns 404.

## On `:x:`

Post "skipped" in the thread and don't send.

## Stay quiet when

The event is the bot's own post, a bot echo, a test message, or there's nothing to draft.

## Rules

- Never email a prospect without a `:white_check_mark:` or an explicit "send".
- Keep secrets in environment variables only.
