from bs4 import BeautifulSoup
import requests
import telegram
from hotdeal.models import Deal
from datetime import datetime, timedelta

response = requests.get(
    "https://www.clien.net/service/board/jirum")

soup = BeautifulSoup(response.text, "html.parser")
BOT_TOKEN = "2024375443:AAG3Fj7gNYQK2l5-5IX5eMg-jr0ZCjUI_VI"

bot = telegram.Bot(token=BOT_TOKEN)


def run():
    # delete deals older than 3days
    row, _ = Deal.objects.filter(created_at__lte=datetime.now() -
                                 timedelta(days=3)).delete()
    print(row, "deals deleted")

    for item in soup.find_all("div", class_="list_title"):
        try:
            title = item.find("span", class_="list_subject").text
            title = title.strip()
            link = item.find("span", class_="list_subject").find("a").get("href")
            link = "https://www.clien.net/" + link
            reply_count = item.find("span", class_="rSymph05").text
            reply_count = int(reply_count)
            up_count = item.find("span", class_="list_votes").text
            up_count = int(up_count)
            if up_count >= 5:
                if (Deal.objects.filter(link__iexact=link).count() == 0):
                    Deal( title=title, link=link,
                         reply_count=reply_count, up_count=up_count).save()
                    bot.sendMessage(-1001305118155,
                                    '{} {}'.format(title, link))

        except Exception as e:
            # print(e):
            continue
