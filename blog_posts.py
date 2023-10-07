import requests
from datetime import date
from dateutil import parser
from lxml import etree

DATE_MONTH_NAME = "%b %d %Y"
BLOG_URL = "https://portfolio.aaronluna.dev/blog"
BLOG_RSS = "https://portfolio.aaronluna.dev/rss.xml"
RECENT_POSTS_BOUNDARY = "<!--blog_posts-->"


def update_recent_blog_posts(post_count=3):
    readme_content = get_readme_content()
    recent_posts = get_recent_posts(post_count)
    update_readme_file(readme_content, recent_posts)


def get_readme_content():
    readme_lines = []
    with open("README.md", "r", encoding="utf8") as readme:
        for line in readme:
            if RECENT_POSTS_BOUNDARY not in line:
                readme_lines.append(line)
                continue
            break
    return readme_lines


def get_recent_posts(post_count):
    all_posts = get_all_posts()
    for post in all_posts:
        post.pop("pub_date")
    post_count = post_count if len(all_posts) >= post_count else len(all_posts)
    return [format_blog_post_as_markdown(post) for post in all_posts[:post_count]]


def get_all_posts():
    rss_xml = get_rss_xml()
    all_posts = [parse_post_details(post) for post in rss_xml.iterfind(".//item")]
    return sorted(all_posts, key=lambda x: x["pub_date"], reverse=True)


def get_rss_xml():
    response = requests.get(BLOG_RSS)
    response.raise_for_status()
    return etree.XML(response.text, parser=None)


def parse_post_details(item):
    pub_date = item.findtext("pubDate")
    pub_date = parser.parse(pub_date).date() if pub_date else date.min
    return {
        "title": item.findtext("title"),
        "description": item.findtext("description"),
        "link": item.findtext("link"),
        "pub_date": pub_date,
        "published": pub_date.strftime(DATE_MONTH_NAME),
    }


def format_blog_post_as_markdown(post):
    return (
        f'- [{post["title"]}]({post["link"]})  \n'
        f'**{post["published"]}** &mdash; {post["description"]}\n'
    )


def update_readme_file(readme_content, recent_posts):
    with open("README.md", "w", encoding="utf8") as readme:
        readme.writelines(readme_content)
        readme.write(f"{RECENT_POSTS_BOUNDARY}\n")
        readme.write(f"## [Recent Blog Posts]({BLOG_URL})\n")
        readme.write("\n".join(recent_posts))


if __name__ == "__main__":
    update_recent_blog_posts()