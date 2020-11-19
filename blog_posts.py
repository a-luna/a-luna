from feedparser import parse

feed = parse("https://aaronluna.dev/blog/index.xml").entries
post_list = [
    f"""- [{feed[i].title}]({feed[i].link})  \n{feed[i].description} - {feed[i].published}"""
    for i in range(4)]

readme_lines = []
with open("README.md", "r", encoding='utf8') as rd:
    for line in rd:
        if line.strip() == "<!--bp-->":
            break
        readme_lines.append(line)

with open("README.md", "w", encoding='utf8') as rd:
    rd.writelines(readme_lines)
    rd.write("<!--bp-->\n")
    rd.write("### Most Recent Blog Posts\n")
    rd.writelines("\n".join(post_list))