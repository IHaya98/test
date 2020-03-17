import os
import slack
import urllib.request as req
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, FirefoxOptions

@slack.RTMClient.run_on(event='message')

def qiitabot(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']

    url = 'https://qiita.com/qiita'
    res = req.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser')
    list = soup.select('.media.ItemLink')

    if 'qiita リスト' in data['text']:
        channel_id = data['channel']
        for li in list:
            t = li.select_one(".ItemLink__title")
            title = t.string
            a = t.a
            href = a.attrs["href"]
            likelist = li.select(".ItemLink__status li")
            info = li.select_one(".ItemLink__info").text
            for i in likelist:
                i = 1
                likenum = likelist[0].text 

            web_client.chat_postMessage(
                channel=channel_id,
                text=f"""
:+1:*{likenum}* いいね！ {info}
> {title}
> https://qiita.com{href}
                """
            )

    elif 'qiita キャプチャ' in data['text']:
        channel_id = data['channel']
        options = FirefoxOptions()
        options.add_argument('-headless')
        browser = Firefox(options=options)
        browser.get(url)
        browser.save_screenshot("qiita-mypage.png")
        web_client.files_upload(
            channels=channel_id,
            file="qiita-mypage.png"
        )

slack_token = os.environ['SLACK_TOKEN']
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()