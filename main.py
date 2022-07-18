import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import datetime

from sqlalchemy import null
import mail

# 記事クラス
class Article:
    def __init__(self, title, url, date):
        self.title = title
        self.url = url
        self.date = date

    def __eq__(self, __o: object):
        if not isinstance(__o, Article):
            return NotImplemented
        return self.url == __o.url

    def __ne__(self, __o: object):
        return not self.__eq__(__o)


# html取得
def get_content(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup


# メール送信
def make_mail(hiroshima_lists, saitama_lists, nagasaki_lists):
    text = ""
    subject = "[大学監視君]"
    if len(hiroshima_lists) != 0:
        subject += "広島大学:{}".format(len(hiroshima_lists))
    if len(saitama_lists) != 0:
        subject += "/埼玉大学:{}".format(len(saitama_lists))
    if len(nagasaki_lists) != 0:
        subject += "/長崎大学:{}".format(len(nagasaki_lists))

    if len(hiroshima_lists) != 0:
        text += (
            "########################\n"
            + "【広島大学】\n"
            + "########################\n"
            + "----------\n"
        )
        for l in hiroshima_lists:
            text += "{}\n{}\n".format(l.title, l.url)
            text += "----------\n"

    if len(saitama_lists) != 0:
        text += (
            "########################\n"
            + "【埼玉大学】\n"
            + "########################\n"
            + "----------\n"
        )
        for l in saitama_lists:
            text += "{}\n{}\n".format(l.title, l.url)
            text += "----------\n"

    if len(nagasaki_lists) != 0:
        text += (
            "########################\n"
            + "【長崎大学】\n"
            + "########################\n"
            + "----------\n"
        )
        for l in nagasaki_lists:
            text += "{}\n{}\n".format(l.title, l.url)
            text += "----------\n"

    if err_msg != "":
        text += (
            "########################\n"
            + "【データ取得エラー】\n"
            + "########################\n"
            + "----------\n"
            + err_msg
        )

    # 件名調整
    if subject[11:12] == "/":
        subject = subject[:11] + subject[12:]

    if debug_flg is False:
        mail.send_mail(subject, text)


# 広島大学
def search_hiroshima():
    list_article = []
    try:
        soup = get_content("https://www.media.hiroshima-u.ac.jp/news/")
        lists = (
            soup.find_all(class_="su-tabs-pane su-u-clearfix su-u-trim")[0]
            .find_all("dl")[0]
            .contents
        )

        for l in lists:
            if l.name == "dt":
                date = dt.strptime(l.text, r"%Y-%m-%d").replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                continue
            elif l.name == "dd":
                url = l.select_one("a").get("href")
                title = l.text

            if debug_flg is False:
                if yester_day == date:
                    article = Article(title, url, date)
                    list_article.append(article)
            else:
                article = Article(title, url, date)
                list_article.append(article)

    except:
        global err_msg
        err_msg += "・広島大学\n"

    return list_article


# 埼玉大学
def search_saitama():
    list_article = []
    try:
        soup = get_content("https://www.itc.saitama-u.ac.jp/news/")
        lists = soup.find_all(class_="dl-horizontal")[0].contents

        for l in lists:
            if l.name == "dt":
                date = dt.strptime(
                    l.select_one("span").contents[0], r"%Y/%m/%d"
                ).replace(hour=0, minute=0, second=0, microsecond=0)
                continue
            elif l.name == "dd":
                url = "https://www.itc.saitama-u.ac.jp/" + l.select_one("a").get("href")
                title = l.text
            else:
                continue

            if debug_flg is False:
                if yester_day == date:
                    article = Article(title, url, date)
                    list_article.append(article)
            else:
                article = Article(title, url, date)
                list_article.append(article)

    except:
        global err_msg
        err_msg += "・埼玉大学\n"

    return list_article


# 長崎大学
def search_nagasaki():
    list_article = []
    try:
        soup = get_content("http://www.cc.nagasaki-u.ac.jp/news/")
        lists = soup.find_all(id="contents")[0].contents

        for l in lists:

            if l.name == "div":
                if l.attrs["class"][0] == "news_list_box":
                    cols = l.contents[1]
                    date = dt.strptime(cols.contents[1].text, r"%Y年%m月%d日").replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                    url = (
                        "http://www.cc.nagasaki-u.ac.jp"
                        + cols.contents[9].contents[1].attrs["href"]
                    )
                    title = cols.contents[9].text.replace("\n", "").replace("\t", "")
                else:
                    continue
            else:
                continue

            if debug_flg is False:
                if yester_day == date:
                    article = Article(title, url, date)
                    list_article.append(article)
            else:
                article = Article(title, url, date)
                list_article.append(article)

    except:
        global err_msg
        err_msg += "・長崎大学\n"

    return list_article


if __name__ == "__main__":
    debug_flg = True
    err_msg = ""
    yester_day = dt.today().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(days=-1)

    hiroshima_lists = search_hiroshima()
    saitama_lists = search_saitama()
    nagasaki_lists = search_nagasaki()

    if (len(hiroshima_lists) + len(saitama_lists) + len(nagasaki_lists)) != 0:
        make_mail(hiroshima_lists, saitama_lists, nagasaki_lists)
