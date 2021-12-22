import json.decoder
import os

import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dhooks import Webhook
from dotenv import load_dotenv
from nextcord.ext import commands

from utils.games.super_people import SPPL_Updates

load_dotenv()
patches_webhook = os.getenv("webhook_url")


class job_scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 120})
        self.sppl = SPPL_Updates()

    @commands.Cog.listener()
    async def on_ready(self):
        scheduler = self.scheduler

        # add jobs for scheduler
        url = "https://superpeopleapi.herokuapp.com/news"
        response = requests.get(url)
        response_json = response.json()
        status = response_json["status"]

        try:
            if status == 200:
                scheduler.add_job(self.sppl.super_people_updates, "interval", minutes=20, id="sppl", max_instances=1)
                scheduler.start()

        except json.JSONDecodeError as e:
            scheduler.remove_job('sppl')
            hook = Webhook(patches_webhook)
            hook.send(e)
        except TypeError as e:
            scheduler.remove_job('sppl')
            hook = Webhook(patches_webhook)
            hook.send(e)


def setup(bot):
    bot.add_cog(job_scheduler(bot))
