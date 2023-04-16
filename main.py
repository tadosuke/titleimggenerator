from __future__ import annotations

import os

from model import TitleImageGenerator

# 画像ファイルのあるフォルダ
_IMAGE_DIR = 'images'

# カテゴリ名→画像ファイル名の辞書
_IMAGE_FILENAME_DICT = {
    'common': 'common.png',
    'english': 'english.png',
    'health': 'health.png',
    'life': 'life.png',
    'music': 'music.png',
    'program': 'program.png',
    'python': 'python.png',
    'voice': 'voice.png',
}


def main():
    """メイン関数."""

    # カテゴリ名
    category_name = 'english'
    # 表示するテキスト
    text = '【ボイトレ】\n$アンザッツ$4～6 を\n$一ヶ月！$'
    # 出力先
    out_path = 'images/out.png'

    image_dir = f'{os.path.dirname(__file__)}/{_IMAGE_DIR}'
    generator = TitleImageGenerator(image_dir, _IMAGE_FILENAME_DICT)
    generator.generate(category_name, text, out_path)


if __name__ == '__main__':
    main()
