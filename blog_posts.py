from feedparser import parse

BLOG_URL = "https://aaronluna.dev/blog/"
BLOG_RSS = f"{BLOG_URL}index.xml"
README_COMMENT = "<!--blog_posts-->"

post_list = [
    f"""- [{f.title}]({f.link})  \n**{f.published}** &mdash; {f.description}\n"""
    for num, f
    in enumerate(parse(BLOG_RSS).entries, start=1)
    if num <= 3
]

readme_lines = []
with open("README.md", "r", encoding='utf8') as rd:
    for line in rd:
        if README_COMMENT not in line:
            readme_lines.append(line)
            continue
        break

with open("README.md", "w", encoding='utf8') as rd:
    rd.writelines(readme_lines)
    rd.write(f"{README_COMMENT}\n")
    rd.write("## [Most Recent Blog Posts](BLOG_URL)\n")
    rd.write("\n".join(post_list))