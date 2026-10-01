---
name: support-chat
description: >-
  Drives a company's customer-support live chat for Graham in the browser pane, with
  him in the loop: drafts the opener in his voice and sends it on his go, then
  answers routine back-and-forth on its own, relays every agent message to him, polls
  while waiting, and stops before anything that commits him (a charge, an
  appointment, an account detail, a reset, an offer, a choice between options). Use
  when Graham says "chat with their support", "drive the live chat", "open a ticket
  with X and handle it", "the chat window is open, can you drive it", or hands over a
  complaint, return or outage to raise with a company. Not for email or phone
  support, not for signing in (Graham signs in himself), and never for accepting
  terms, paying or changing an account. Costs a poll every minute or two for the
  length of the chat.
metadata:
  maturity: incubator
---

# Support chat

A live support chat run for Graham, where he sees every message the agent sends and
nothing is agreed to without him. Built from three chats in the week of 2026-09-28
(a misrouted Quince order, an Astound outage, a Spruce cleaning complaint) that each
rebuilt this protocol by hand.

## Before the chat

1. **Check the live state first.** Re-read the order, ticket, bill or device status
   the complaint is about, even if a handoff or an earlier session describes it. One
   chat resumed nine days later and the facts had moved.
2. **Write a context file** in the project folder: what happened, what Graham wants
   (refund, replacement, a technician, an explanation), and every fact tagged
   `sourced` (seen in a receipt, page or photo, with where) or `reported` (Graham
   said so). The opener and every answer come from this file.
3. **Graham signs in, in the browser pane.** Never type a password or a one-time
   code. Use the built-in pane: once he signs in there the sign-in persists, and you
   can then open the chat widget yourself. Claude in Chrome is the wrong tool here:
   in one chat it was unreachable, and in another it opened a tab of its own that
   could not see the chat open in his.

## The opener

Draft it with `voice-and-editing:graham-voice`: the problem, the order or account
reference the company needs, and the outcome he wants, in two to four sentences.
Show it to Graham and send it only on his go ("yes, send it").

## During the chat

- **A bot often answers first.** Answer its routing questions from the context file,
  ask for a person if it loops, and relay the hand-off when a person joins.
- **Answer routine questions yourself** once the opener is out: order numbers,
  dates, what happened, technical readings, photos he has already provided, anything
  in the context file. Graham said so in two of the three chats ("continue chatting
  until they ask for me to commit something"; "You dont need my confirmation on back
  and forth messages and providing context and detail").
- **Relay every agent message to Graham**, in a short quote with the time, as soon as
  you read it. On each poll, read the whole chat since your last message, scrolling
  if needed, not only the newest bubble: in one chat an agent offer and question went
  unrelayed and Graham answered it himself from the pane.
- **Graham may read the pane and answer you directly.** His answer in chat is his go
  for that item: send it, and say what you sent.
- **Stop and ask Graham before any commitment.** A fact he already approved (in the
  opener, or given by him in this session) may be repeated without asking again;
  anything new on this list may not. The stop list:
  - a charge, refund amount, credit or payment method;
  - an appointment, technician visit or delivery window;
  - an account detail (address, phone, card digits, date of birth, security answers);
  - a reset, restart, cancellation or change on his account or device;
  - accepting an offer, upgrade, plan change or survey;
  - a choice between options the agent offers (a replacement color, a resolution):
    relay the options and ask, rather than waiting for him to find them in the pane;
  - ending the chat.
  Tell the agent you are checking ("One moment, checking with Graham") and keep
  polling while you wait for him. A wake-up prompt you wrote for yourself is never
  Graham's go; it covers routine sends only.
- **Quote time words as the agent wrote them.** "Your window" can mean an arrival
  window, not a duration; one chat sent "less than an hour left in our window" from a
  misread. Do not convert the agent's times into durations or deadlines.
- **Poll every one to two minutes** while a reply is due (ScheduleWakeup or Monitor,
  whichever the session has); never leave the chat unread for long, since agents
  close idle chats. After about ten minutes with no agent reply, ask whether they are
  still there, sooner if Graham asks.

## Ending

End the chat only on Graham's word, and then actually end it (the chat's End or
Close control), not just stop polling. Save the chat text and the outcome (case
number, promised dates, amounts, the agent's name) into the context file, and tell
Graham the outcome in two or three lines. If the End Chat control does not respond,
say so rather than clicking it again and again.

## Inputs

The company, the complaint and the outcome Graham wants; whatever evidence he has
(receipts, photos, readings); the chat open and signed in, in the browser pane.

## Verify

Every agent message in the saved chat text has a relay line to Graham after it, and
every stop-list item in it has Graham's answer before Claude's reply. Replayed
against the Quince chat on 2026-10-01 (a slimmed transcript, so agent text was
visible only through Claude's relays): the opener waited for Graham's go and nothing
was sent unapproved, and the rules flag what went wrong, the agent offer that went
unrelayed until Graham answered it from the pane, the color options he picked
before Claude relayed them, relays with no time, and the chat left open at the end.
The replay also produced the bot-first, already-approved-fact, Graham-answers-directly
and wake-prompt rules above.

## Done when

The chat is closed on Graham's word, the outcome and chat text are in the context
file, and Graham has a two-to-three-line summary.

## Stop when

The chat asks for anything on the stop list and Graham has not answered; the chat
needs a sign-in, a one-time code or a payment step (Graham's to do); the browser pane
cannot load the chat; or the company ends the chat. Say which, and what is still open.
