import requests
from bs4 import BeautifulSoup
import datetime

timeout = 5
blog_url = "https://cherrue.github.io/"
dest_file_url = "README.md"


def getTitleAndLinkFromResponse(res):
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select('article')
    articles_data = [(article.select_one('a').get_text(), article.select_one('a').get("href"))
                     for article in articles]
    return articles_data


def getPostsTop5(_url: str, _timeout):
    MAX_RETRY = 5
    my_headers = {'Content-Type': 'application/json; charset=utf-8'}
    retries = 0
    while True:
        res = requests.get(_url, headers=my_headers, timeout=_timeout)
        retries = retries + 1

        # like do while
        if res is not None and res.status_code == 200:
            break

        # prevent endless loop
        if retries > MAX_RETRY:
            return [("posts parse failed", "about:blank/")]
    return getTitleAndLinkFromResponse(res)


def getMarkdownTextFromPosts(_posts: list):
    result = ""
    for post in _posts:
        result += f"- [{post[0]}]({post[1]}) <br>\n"
    result += "Updated at " + \
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "<br>\n"
    return result


def writeNewPostListToFile(file_url: str, write_text: str):
    with open(file_url, mode="r+", encoding="utf-8") as f:
        data = f.readlines()
        f.seek(0)

        erase_flag = False
        for line in data:
            if "<!-- BLOG-POST-LIST:START -->" in line:
                erase_flag = True
                f.write(line)
                f.write(write_text)
                continue  # don't erase START line
            if "<!-- BLOG-POST-LIST:END -->" in line:
                erase_flag = False
            if not erase_flag:
                f.write(line)
        f.truncate()


posts = getPostsTop5(blog_url, timeout)
markdown_text = getMarkdownTextFromPosts(posts)
writeNewPostListToFile(dest_file_url, markdown_text)
