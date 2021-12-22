import os

import requests
import ujson as json
from dhooks import Embed, File, Webhook
from dotenv import load_dotenv
from utils.global_utils import crimson, flatten, news_exists

load_dotenv()
webhook = os.getenv("webhook_url")


def getSpplNews():
    URL = "https://superpeopleapi.herokuapp.com/news"
    response = requests.get(URL)
    return response.json()


class SPPL_Updates:
    async def super_people_updates(self):

        # patch-notes channel
        saved_json = "super_people.json"
        response_json = getSpplNews()

        # JSON Results Mapping
        banner = response_json["data"][0]["thumbnail"]
        title = response_json["data"][0]["title"]
        description = response_json["data"][0]["summary"]
        url = response_json["data"][0]["url"]
        status = response_json["status"]

        # check if file exists
        news_exists(saved_json)

        # open saved_json file
        with open(saved_json) as f:
            data = json.load(f)
            res = flatten(data, "", None)
        check_file_json = res["data"][0]["title"]

        # compare title string from file to title string from api then overwrite file
        if data is not None or status == 200:
            if check_file_json == title:
                # print("True")
                return
            elif check_file_json != title:
                # print("False")
                hook = Webhook(webhook)

                embed = Embed(
                    title="Super People",
                    description=f"[{title}]({url})\n\n{description}",
                    color=crimson,
                    timestamp="now",  # sets the timestamp to current time
                )
                embed.set_footer(text="Super People Bot")
                embed.set_image(url=banner)
                file = File(
                    "./assets/images/super_people_logo.png",
                    name="super_people_logo.png",
                )
                embed.set_thumbnail(url="attachment://super_people_logo.png")

                hook.send(embed=embed, file=file)

                with open(saved_json, "w") as updated:
                    json.dump(response_json, updated, ensure_ascii=False)

                updated.close()
