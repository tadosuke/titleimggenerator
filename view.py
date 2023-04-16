"""TitleImageGenerator を扱う GUI モジュール."""

from __future__ import annotations

import os.path
import traceback

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

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
    'python': 'program.png',
    'voice': 'voice.png',
}


class _MainWidget(QtWidgets.QWidget):
    """メインウィジェット."""

    _TITLE_EDIT_HEIGHT = 60

    def __init__(
            self,
            parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)

        self._image_dir: str = f'{os.path.dirname(__file__)}/{_IMAGE_DIR}'
        self._check_image_folder()
        self._setup_ui()

    def _check_image_folder(self) -> None:
        if not os.path.exists(self._image_dir):
            message = QtWidgets.QMessageBox(self)
            message.setText(f'画像フォルダが見つかりません。{self._image_dir}')
            message.show()
            self.close()

    def _setup_ui(self) -> None:
        """UI を初期化します."""
        self._combobox_category = self._create_category_combobox()
        self._edit_title = self._create_title_textedit()
        button_save = QtWidgets.QPushButton('保存')
        button_save.clicked.connect(self._on_save)

        layout = QtWidgets.QFormLayout()
        layout.addRow('カテゴリ', self._combobox_category)
        layout.addRow('タイトル', self._edit_title)
        layout.addWidget(button_save)
        self.setLayout(layout)

    @staticmethod
    def _create_category_combobox() -> QtWidgets.QComboBox:
        """カテゴリ選択コンボボックスを生成します."""
        combobox = QtWidgets.QComboBox()
        combobox.addItems(_IMAGE_FILENAME_DICT.keys())
        return combobox

    def _create_title_textedit(self) -> QtWidgets.QTextEdit:
        """タイトルテキスト入力ボックスを生成します."""
        edit_title = QtWidgets.QTextEdit()
        edit_title.setPlainText('【Category】本文$強調$文字\n2行目メッセージ')
        edit_title.setMaximumHeight(self._TITLE_EDIT_HEIGHT)
        return edit_title

    def _on_save(self) -> None:
        """セーブボタンが押された時に呼ばれます."""
        if not self._validate():
            return

        out_path = self._show_save_dialog()
        if out_path == '':
            return

        is_success = self._generate(out_path)
        self._show_result(is_success)

    def _validate(self) -> bool:
        """入力値を検証します."""
        if self._combobox_category.currentText() == "":
            return False
        if self._edit_title.toPlainText() == "":
            return False
        return True

    def _show_save_dialog(self) -> str:
        """保存ダイアログを表示します."""
        out_path, _ = QFileDialog.getSaveFileName(
            self,
            '保存先を選択してください。',
            f'{self._combobox_category.currentText()}_.png',
            '画像ファイル (.*png)')
        return out_path

    def _generate(self, out_path: str) -> bool:
        """画像を生成します."""
        category = self._combobox_category.currentText()
        title = self._edit_title.toPlainText()
        try:
            generator = TitleImageGenerator(self._image_dir, _IMAGE_FILENAME_DICT)
            generator.generate(category, title, out_path)
        except Exception:
            traceback.format_exc()
            return False
        return True

    def _show_result(self, is_success: bool) -> None:
        """結果を表示する."""
        message = QtWidgets.QMessageBox(self)
        if is_success:
            message.setText('保存しました。')
        else:
            message.setText('保存に失敗しました。')
        message.show()


class MainWindow(QtWidgets.QMainWindow):
    """メインウィンドウ."""

    def __init__(
            self,
            parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWindowTitle('TitleImageGenerator')
        widget = _MainWidget(self)
        self.setCentralWidget(widget)


def main() -> None:
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
