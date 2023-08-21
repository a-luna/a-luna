from feedparser import parse

BLOG_URL = "https://portfolio.aaronluna.dev/"
BLOG_RSS = f"{BLOG_URL}rss.xml"
RECENT_POSTS_BOUNDARY = "<!--blog_posts-->"


def update_recent_blog_posts(post_count=3):
    readme_content = get_readme_content()
    recent_posts = get_recent_posts(post_count)
    with open("README.md", "w", encoding="utf8") as readme:
        readme.writelines(readme_content)
        readme.write(f"{RECENT_POSTS_BOUNDARY}\n")
        readme.write(f"## [Recent Blog Posts]({BLOG_URL})\n")
        readme.write("\n".join(recent_posts))


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
    all_posts = parse(BLOG_RSS).entries
    all_posts.sort(key=lambda x: x.published, reverse=True)
    post_count = post_count if len(all_posts) >= post_count else len(all_posts)
    return [format_blog_post_as_markdown(post) for post in all_posts[:post_count]]


def format_blog_post_as_markdown(post):
    return (
        f"- [{post.title}]({post.link})  \n"
        f"**{post.published}** &mdash; {post.description}\n"
    )


if __name__ == "__main__":
    update_recent_blog_posts()