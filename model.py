"""カテゴリ名とタイトルテキストから、タイトルテキスト入り画像を生成するツール."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

# フォント名
_FONT_NAME = 'HGRPP1'
# フォントサイズ
_FONT_SIZE = 50
# 背景とテキストの間隔
_PADDING_Y = 25


class _BackGround:
    """背景画像."""

    def __init__(self, image_path: str) -> None:
        self.image = Image.open(image_path)

    def paste(self, text_bg: _TextBackGround) -> None:
        """テキスト入りの背景を貼り付ける"""
        bg_pos = (0, int(self.image.height / 2 - text_bg.image.height / 2))
        self.image.paste(text_bg.image, bg_pos, mask=text_bg.image)


class _TextInfo:
    """テキスト情報."""

    # 改行時の間隔
    LINE_SPACE = 20

    def __init__(self, text, font):
        self.line_list = self._split_lines(text, font)
        self.text = text

    @staticmethod
    def _split_lines(text: str, font: ImageFont.FreeTypeFont) -> list[_Line]:
        return [_Line(line_str, font) for line_str in text.splitlines()]

    def calc_size(self) -> tuple[int, int]:
        width = 0
        height = 0
        for i, line in enumerate(self.line_list):
            if 1 <= i:
                height += self.LINE_SPACE
            line_width, line_height = line.calc_size()
            width += max(width, line_width)
            height += line_height
        return width, height


class _Line:
    """行."""

    # 強調区切り文字
    _STRONG_DELIMITER = '$'
    # テキスト色：通常
    _NORMAL_RGBA = (255, 255, 255, 255)
    # テキスト色：強調
    _STRONG_RGBA = (0, 255, 255, 255)

    def __init__(self, line_str: str, font):
        self.phrase_list = self._split_phrases(line_str, font)

    @classmethod
    def _split_phrases(
            cls, line_str: str,
            font: ImageFont.FreeTypeFont) -> list[_Phrase]:
        phrase_list = []
        phrase_strs = line_str.split(cls._STRONG_DELIMITER)
        for i, phrase_str in enumerate(phrase_strs):
            rgba = cls._NORMAL_RGBA if i % 2 == 0 else cls._STRONG_RGBA
            phrase = _Phrase(phrase_str, font, rgba)
            phrase_list.append(phrase)

        return phrase_list

    def calc_size(self):
        width = sum(phrase.width for phrase in self.phrase_list)
        height = max(phrase.height for phrase in self.phrase_list)
        return width, height


class _Phrase:
    """文節."""

    def __init__(
            self,
            phrase_str: str,
            font: ImageFont.FreeTypeFont,
            color: tuple[int, int, int, int]):
        self.text = phrase_str
        self.color = color
        self.font = font
        _, _, self.width, self.height = self.font.getbbox(self.text)


class _TextBackGround:
    """テキスト背景."""

    def __init__(self, width: int, text_info: _TextInfo, padding_y: int) -> None:
        self.image = self._create_image(width, text_info, padding_y)
        self._add_text(text_info)

    @staticmethod
    def _create_image(width: int, text_info: _TextInfo, padding_y: int):
        """背景画像を生成します."""
        text_width, text_height = text_info.calc_size()
        bg_size = (width, text_height + padding_y * 2)
        bg_rgba = (0, 0, 0, 128)
        return Image.new("RGBA", bg_size, bg_rgba)

    def _add_text(self, text_info: _TextInfo) -> None:
        """テキストを追加します."""
        text_draw = ImageDraw.Draw(self.image)

        text_width, text_height = text_info.calc_size()
        cur_height = self.image.height / 2 - text_height / 2
        for line in text_info.line_list:
            line_width, line_height = line.calc_size()
            cur_width = self.image.width / 2 - line_width / 2
            for phrase in line.phrase_list:
                phrase_pos = (cur_width, cur_height)
                text_draw.text(phrase_pos, phrase.text, font=phrase.font, fill=phrase.color)
                cur_width += phrase.width
            # 改行
            cur_height += line_height + text_info.LINE_SPACE


class TitleImageGenerator:
    """カテゴリとテキストから、テキスト入りタイトル画像を生成するクラス.

    :param directory: 画像ファイルのあるディレクトリ
    :param category_dict: カテゴリ→画像ファイル名の辞書
    """

    def __init__(
            self,
            directory: str,
            category_dict: dict[str, str]) -> None:
        self._directory = directory
        self._category_dict = category_dict
        self._font = ImageFont.truetype(_FONT_NAME, _FONT_SIZE)

    def generate(
            self,
            category: str,
            text: str,
            out_path: str) -> None:
        """画像を生成します.

        :param category: カテゴリ名
        :param text: タイトルテキスト
        :param out_path: 出力先のパス
        """
        image_path = self._get_image_path(category)
        bg_image = _BackGround(image_path)
        text_info = _TextInfo(text, self._font)
        text_bg = _TextBackGround(bg_image.image.width, text_info, _PADDING_Y)

        bg_image.paste(text_bg)
        bg_image.image.save(out_path)

    def _get_image_path(self, category: str) -> str:
        image_file_name = self._category_dict[category]
        return f'{self._directory}/{image_file_name}'
