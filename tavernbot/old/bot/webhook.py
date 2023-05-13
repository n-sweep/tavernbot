#!/usr/bin/env python
# Discord Webhook Messenger!

from discord import Webhook, RequestsWebhookAdapter


class DiscordWebhook:
	def __init__(self, wh_id, token):
		self.hook = Webhook.partial(wh_id, token, adapter=RequestsWebhookAdapter())

	def send_message(self, text):
		self.hook.send(text)
