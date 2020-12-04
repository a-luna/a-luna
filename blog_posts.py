from feedparser import parse

BLOG_URL = "https://aaronluna.dev/blog/"
BLOG_RSS = f"{BLOG_URL}index.xml"
README_COMMENT = "<!--blog_posts-->"


def update_recent_blog_posts(post_count=3):
    readme_content = get_readme_content()
    post_list = get_recent_posts(post_count)
    with open("README.md", "w", encoding='utf8') as readme:
        readme.writelines(readme_content)
        readme.write(f"{README_COMMENT}\n")
        readme.write(f"## [Recent Blog Posts]({BLOG_URL})\n")
        readme.write("\n".join(post_list))

def get_readme_content():
    readme_lines = []
    with open("README.md", "r", encoding='utf8') as readme:
        for line in readme:
            if README_COMMENT not in line:
                readme_lines.append(line)
                continue
            break
    return readme_lines

def get_recent_posts(post_count):
    all_blog_posts = parse(BLOG_RSS).entries
    return [format_blog_post_as_markdown(post) for post in all_blog_posts[:3]]

def format_blog_post_as_markdown(post):
    return (
        f"- [{post.title}]({post.link})  \n"
        f"**{post.published}** &mdash; {post.description}\n"
    )
if __name__ == "__main__":
    update_recent_blog_posts()