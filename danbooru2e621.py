import argparse
import csv
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--csv_file', help='csv file path. default=e621.csv', default='e621.csv')
parser.add_argument('-t', '--text_file_dir', help='caption files(.txt) directory path. default=input', default='input')
# parser.add_argument('-o', '--output_dir', help='output directory path. default=output', default='output')
args = parser.parse_args()

# DICT_FILEは"DominikDoom/a1111-sd-webui-tagcomplete"用CSV tag dataを想定
# 手元の環境だと'stable-diffusion-webui/extensions/a1111-sd-webui-tagcomplete/tags/'に存在
DICT_FILE = Path(args.csv_file)
INPUT_DIR = Path(args.text_file_dir)
# OUTPUT_DIR = Path(args.output_dir)

print('DICT_FILE:', DICT_FILE)
print('INPUT_DIR:', INPUT_DIR)
# print('OUTPUT_DIR:', OUTPUT_DIR)

# DICT_FILEからdict_file(danbooru語->e621語翻訳リスト)を作る
with open(DICT_FILE, 'r') as f:
    dict_file = []
    reader = csv.DictReader(f, fieldnames=['name', 'type', 'postCount', 'aliases'])
    for row in reader:
        # invalid_tag, female, maleの除外
        if row['name'] == 'invalid_tag':
            continue
        if row['name'] == 'female':
            continue
        if row['name'] == 'male':
            continue
        # 'aliases'に値が存在する場合のみ'name'と'aliases'を代入
        # 'aliases'に値が存在する場合のみ'name'と'aliases'を代入
        else:
            if len(row['aliases']) != 0:
                # 'aliases'がstrなのでlistに変換する
                dict_file.append({'name': row['name'].replace('_', ' '), 'aliases': row['aliases'].replace('_', ' ').split(',')})
print('dict_file is ready')

# INPUT_DIR内のテキストファイルを'caption_file'として読み込み、'dict_file'を使って翻訳する
caption_files = INPUT_DIR.glob('**/*.txt')
for caption_file in caption_files:
    # strからlistに変換
    with open(caption_file, 'r') as f:
        caption_list = f.read() \
            .replace('|||', 'sep1,', 1) \
            .replace('|||', 'sep2,', 1) \
            .rstrip() \
            .split(sep=', ')
    # dict_fileの'aliases'に該当するタグがある場合、caption_file内のタグをdict_fileの'name'に置き換え
    for i in range(len(caption_list)):
        for j in dict_file:
            if caption_list[i] in j['aliases']:
                caption_list[i] = j['name']
    # 重複タグの削除。よくわかっていない
    caption_list2 = []
    for k, x in enumerate(caption_list):
        if caption_list.index(x) == k:
            caption_list2.append(x)
    # listからstrに戻す
    caption_str = ', '.join(caption_list2)
    caption_result = caption_str \
        .replace('sep1,', '|||') \
        .replace('sep2,', '|||') \
        .replace('_', ' ')
    # caption_fileを上書き
    with open(caption_file, 'w') as f:
        f.write(caption_result)
print('done')
