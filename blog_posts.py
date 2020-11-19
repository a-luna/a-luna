from feedparser import parse

BLOG_URL = "https://aaronluna.dev/blog/"
BLOG_RSS = f"{BLOG_URL}index.xml"
README_COMMENT = "<!--blog_posts-->"


def get_recent_posts(post_count):
    return [
        f"- [{f.title}]({f.link})  \n**{f.published}** &mdash; {f.description}\n"
        for num, f
        in enumerate(parse(BLOG_RSS).entries, start=1)
        if num <= post_count
    ]

def preserve_readme():
    readme_lines = []
    with open("README.md", "r", encoding='utf8') as rd:
        for line in rd:
            if README_COMMENT not in line:
                readme_lines.append(line)
                continue
            break
    return readme_lines

def update_blog_posts_on_readme(self, post_count=3):
    readme_lines = preserve_readme()
    post_list = get_recent_posts(post_count)
    with open("README.md", "w", encoding='utf8') as rd:
        rd.writelines(readme_lines)
        rd.write(f"{README_COMMENT}\n")
        rd.write(f"## [Recent Blog Posts]({BLOG_URL})\n")
        rd.write("\n".join(post_list))
        
if __name__ == "__main__":
    update_blog_posts_on_readme()