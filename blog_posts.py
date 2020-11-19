from feedparser import parse

feed = parse("https://aaronluna.dev/blog/index.xml").entries
post_list = [
    f"""- [{feed[i].title}]({feed[i].link})\n({feed[i].published}) {feed[i].description}\n"""
    for i in range(4)]

readme_lines = []
with open("README.md", "r", encoding='utf8') as rd:
    for line in rd:
        if "<!--blog_posts-->" not in line:
            readme_lines.append(line)
            continue
        break

with open("README.md", "w", encoding='utf8') as rd:
    rd.writelines(readme_lines)
    rd.write("<!--blog_posts-->\n")
    rd.write("#### [Most Recent Blog Posts](https://aaronluna.dev/blog/)\n")
    rd.writelines("\n".join(post_list))