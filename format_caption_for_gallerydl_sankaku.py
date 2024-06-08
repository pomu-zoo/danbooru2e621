import itertools
import json
from pathlib import Path


CAPTION_DIR = Path.cwd()
caption_files = CAPTION_DIR.glob('**/*.json')

for caption_file in caption_files:
    with open(caption_file, 'r') as f:
        json_file = json.load(f)

    nested_caption_list = [
        json_file.get('tags_character', ['']), \
        json_file.get('tags_copyright', ['']), \
        json_file.get('tags_artist', ['']), \
        ['|||'], \
        json_file.get('tags_general', ['']), \
        ['|||'], \
        json_file.get('tags_medium', ['']), \
        json_file.get('tags_meta', ['']), \
        ['rating:'], \
        json_file.get('rating', [''])
    ]

    flattened_caption_list = list(itertools.chain(*nested_caption_list))

    caption = ", ".join(flattened_caption_list)
    caption = caption.replace('|||,', '|||' ).replace('rating:,', 'rating:')
    caption = caption.lower()
    print(caption)

    with open(caption_file.with_suffix('.txt'), 'w') as f:
        f.write(caption)

print('\n' 'Done!')
