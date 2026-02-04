"""MkDocs hook to inject recent blog posts into the homepage."""

import re
from pathlib import Path


def on_page_markdown(markdown, page, config, files):
    """Replace {{ recent_posts }} with recent blog post cards."""
    if page.file.src_path != "index.md":
        return markdown

    if "{{ recent_posts }}" not in markdown:
        return markdown

    posts = []
    blog_posts_dir = Path(config["docs_dir"]) / "blog" / "posts"
    images_dir = Path(config["docs_dir"]) / "images"

    if not blog_posts_dir.exists():
        return markdown.replace("{{ recent_posts }}", "*No posts yet*")

    for post_file in blog_posts_dir.glob("*.md"):
        content = post_file.read_text(encoding="utf-8")

        # Parse YAML front matter
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            continue

        front_matter = match.group(1)

        # Extract title
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', front_matter, re.MULTILINE)
        title = title_match.group(1) if title_match else post_file.stem

        # Extract date
        date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', front_matter, re.MULTILINE)
        date = date_match.group(1) if date_match else "1970-01-01"

        # Extract slug
        slug_match = re.search(r'^slug:\s*(.+?)\s*$', front_matter, re.MULTILINE)
        if slug_match:
            slug = slug_match.group(1)
        else:
            slug = re.sub(r'[^a-z0-9-]', '', title.lower().replace(' ', '-'))

        # Extract image path
        image_match = re.search(r'^image:\s*["\']?(.+?)["\']?\s*$', front_matter, re.MULTILINE)
        image = None
        if image_match:
            image_path = image_match.group(1).lstrip("/")
            # Check for _small variant
            if image_path.startswith("images/"):
                img_name = image_path[7:]  # Remove "images/" prefix
                base, ext = img_name.rsplit(".", 1) if "." in img_name else (img_name, "jpg")
                small_path = images_dir / f"{base}_small.{ext}"
                if small_path.exists():
                    image = f"images/{base}_small.{ext}"
                elif (images_dir / img_name).exists():
                    image = image_path

        # Build URL from date and slug: blog/{year}/{month}/{slug}/
        year, month, _ = date.split("-")
        url = f"blog/{year}/{month}/{slug}/"

        posts.append({"title": title, "date": date, "url": url, "image": image})

    # Sort by date descending, take latest 10
    posts.sort(key=lambda x: x["date"], reverse=True)
    posts = posts[:10]

    if not posts:
        return markdown.replace("{{ recent_posts }}", "*No posts yet*")

    # Generate responsive card grid HTML
    cards_html = """<style>
.post-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin: 1rem 0; }
.post-card { border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s, box-shadow 0.2s; background: var(--md-default-bg-color); }
.post-card:hover { transform: translateY(-4px); box-shadow: 0 4px 16px rgba(0,0,0,0.15); }
.post-card a { text-decoration: none; color: inherit; display: block; }
.post-card-img { width: 100%; height: 180px; object-fit: cover; background: var(--md-default-fg-color--lightest); }
.post-card-body { padding: 1rem; }
.post-card-title { margin: 0 0 0.5rem 0; font-size: 1.1rem; font-weight: 600; color: var(--md-default-fg-color); }
.post-card-date { font-size: 0.85rem; color: var(--md-default-fg-color--light); }
</style>
<div class="post-cards">
"""
    for post in posts:
        img_html = ""
        if post["image"]:
            img_html = f'<img class="post-card-img" src="{post["image"]}" alt="{post["title"]}">'
        else:
            img_html = '<div class="post-card-img"></div>'

        cards_html += f"""<div class="post-card">
<a href="{post['url']}">
{img_html}
<div class="post-card-body">
<h3 class="post-card-title">{post['title']}</h3>
<span class="post-card-date">{post['date']}</span>
</div>
</a>
</div>
"""
    cards_html += "</div>"

    return markdown.replace("{{ recent_posts }}", cards_html)
