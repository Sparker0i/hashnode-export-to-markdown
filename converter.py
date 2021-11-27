import os
import json
import yaml
from markdownify import markdownify
import urllib.request
# import hashnode

export_path = 'devid-stories.json'
media_path = 'posts/media'
posts_path = '../hashnode-articles/'
config = {
    'domain': 'xn--david-9u04d.to',
    'media_url': 'https://david.wolf.gdn/media',
}

export = json.load(open(export_path))
# print(export['posts'])

for post in export['posts']:
    cover_image_basename = f"{post['id']}.png"
    cover_image_path = f"{media_path}/{cover_image_basename}"
    post_path = f"{posts_path}/{post['id']}.md"

    if not os.path.isfile(cover_image_path):
        urllib.request.urlretrieve(
            post['coverImage'], cover_image_path)

    frontmatter = {
        'title': post['title'],
        'slug': post['slug'],
        'cover': f"{config['media_url']}/{cover_image_basename}",
        'domain': config['domain'],
        'tags': ', '.join(post['tags']),
        'date': post['dateAdded'],
    }
    if 'dateUpdated' in post:
        frontmatter['lastmod'] = post['dateUpdated']
    frontmatter_yaml = yaml.dump(frontmatter)

    post = f'''---\n{frontmatter_yaml}---\n\n{markdownify(post['content'])}'''

    with open(post_path, 'w') as f:
        f.write(post)
