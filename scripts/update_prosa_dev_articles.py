import requests
import feedparser

prosa_dev_feed_url = "https://prosa.dev/feed.xml"
start_mark = "<!-- recent-prosa-dev-articles start -->"
end_mark = "<!-- recent-prosa-dev-articles end -->"

def get_readme_file_content():
    path = "README.md"
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def fetch_prosa_dev_articles():
    feed = feedparser.parse(prosa_dev_feed_url)

    result = []
    for entry in feed.entries[:10]:
        if entry.author != "contato@prosa.dev (Marcos Leandro)":
            continue

        result.append({
            "title": entry.title,
            "link": entry.link,
            "description": entry.description,
            "cover": entry.links[1].href
        })

    return result

def create_articles_markdown(articles):
    html = []
    html.append('<table style="margin-left:auto; margin-right:auto">')

    i = 0
    for article in articles:
        if i % 2 == 0:
            html.append("<tr>")
        html.append(cell(article, articles, i))

        if i % 2 == 1 or i == len(articles) - 1:
            html.append("</tr>")
        i += 1

    html.append("</table>")
    return "\n".join(html)


def cell(article, articles, i):
    img = f'<img src="{article["cover"]}" alt="{article["title"]}" style="width:300px; aspect-ratio:16/9; max-width:100%; border-radius:4px;" />'
    title = f'<h4><a href="{article["link"]}" target="_blank">{article["title"]}</a></h4>'

    result = '<td style="text-align:center; padding:12px'
    if i % 2 == 0 and i == len(articles) - 1:
        result += ' colspan="2";'
    result += '">'
    result += f'<div style="width:100%; margin-top:6px; font-weight:600">{img}</div>'
    result += f'<div>{title}</div>'
    return result


def main():
    readme = get_readme_file_content()
    articles = fetch_prosa_dev_articles()
    articles_markdown = create_articles_markdown(articles)

    start_index = readme.index(start_mark) + len(start_mark)
    end_index = readme.index(end_mark)
    new_readme = readme[:start_index] + "\n" + articles_markdown + "\n" + readme[end_index:]
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_readme)


if __name__ == "__main__":
    main()
