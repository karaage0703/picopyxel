"""
picopyxel - 8bitスタイルの音楽シーケンサー
"""

import pyxel
from sequencer import Sequencer
from input_manager import InputManager


class PicoPixel:
    """
    メインアプリケーションクラス
    """

    def __init__(self):
        """アプリケーションの初期化"""
        # 画面サイズ設定
        self.WIDTH = 160
        self.HEIGHT = 120

        # Pyxel初期化
        pyxel.init(self.WIDTH, self.HEIGHT, title="PicoPixel", fps=30)

        # サウンド設定
        self._setup_sounds()

        # シーケンサーとインプットマネージャーの初期化
        self.sequencer = Sequencer()
        self.input_manager = InputManager(self.sequencer)

        # 色の定義
        self.COLOR_BG = 0  # 背景色（黒）
        self.COLOR_TEXT = 7  # テキスト色（白）
        self.COLOR_GRID = 5  # グリッド色（暗い青）
        self.COLOR_STEP = 8  # ステップ色（灰色）
        self.COLOR_ACTIVE = 11  # アクティブステップ色（水色）
        self.COLOR_NOTE = 10  # 音符色（緑）

        # グリッド設定
        self.GRID_X = 10
        self.GRID_Y = 30
        self.CELL_WIDTH = 8
        self.CELL_HEIGHT = 8
        self.GRID_WIDTH = 16 * self.CELL_WIDTH
        self.GRID_HEIGHT = 8 * self.CELL_HEIGHT

        # 音階表示位置
        self.notes = ["ド+", "シ", "ラ", "ソ", "ファ", "ミ", "レ", "ド"]

        # Pyxelアプリ実行
        pyxel.run(self.update, self.draw)

    def _setup_sounds(self):
        """サウンド設定"""
        # 矩形波（四角波）の音色を設定
        # 音色0: 通常の矩形波
        pyxel.sounds[0].set(
            "c2c2",  # note
            "s",  # tone
            "5",  # volume
            "n",  # effect
            15,  # speed
        )

        # 音色1: ビブラート付き矩形波
        pyxel.sounds[1].set(
            "c2c2",  # note
            "s",  # tone
            "5",  # volume
            "v",  # effect
            15,  # speed
        )

        # 音色2: フェードアウト付き矩形波
        pyxel.sounds[2].set(
            "c2c2",  # note
            "s",  # tone
            "5",  # volume
            "f",  # effect
            15,  # speed
        )

        # 音色3: ノイズ
        pyxel.sounds[3].set(
            "c2c2",  # note
            "n",  # tone
            "5",  # volume
            "n",  # effect
            15,  # speed
        )

    def update(self):
        """状態更新（毎フレーム呼び出し）"""
        # 終了判定（ESCキー）
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # 入力処理
        self.input_manager.update()

        # シーケンサー更新
        self.sequencer.update()

    def draw(self):
        """描画処理（毎フレーム呼び出し）"""
        # 画面クリア
        pyxel.cls(self.COLOR_BG)

        # タイトル描画
        pyxel.text(5, 5, "PicoPixel - 8bit Music Sequencer", self.COLOR_TEXT)
        pyxel.text(5, 15, "SPACE: Play/Stop  ARROWS: Move  Z-B: Input Note", self.COLOR_TEXT)

        # シーケンサーグリッド描画
        self._draw_sequencer_grid()

        # 再生状態表示
        status = "PLAYING" if self.sequencer.playing else "STOPPED"
        pyxel.text(5, self.GRID_Y + self.GRID_HEIGHT + 10, f"Status: {status}", self.COLOR_TEXT)

        # 選択中のステップ表示
        pyxel.text(80, self.GRID_Y + self.GRID_HEIGHT + 10, f"Step: {self.input_manager.selected_step + 1}", self.COLOR_TEXT)

    def _draw_sequencer_grid(self):
        """シーケンサーグリッドの描画"""
        # グリッド背景
        pyxel.rectb(self.GRID_X - 1, self.GRID_Y - 1, self.GRID_WIDTH + 2, self.GRID_HEIGHT + 2, self.COLOR_GRID)

        # 音階ラベル描画
        for i, note in enumerate(self.notes):
            pyxel.text(self.GRID_X - 9, self.GRID_Y + i * self.CELL_HEIGHT + 1, note, self.COLOR_TEXT)

        # ステップ番号描画
        for i in range(16):
            if i % 4 == 0:  # 4拍子の区切りを強調
                pyxel.text(self.GRID_X + i * self.CELL_WIDTH, self.GRID_Y - 8, str(i + 1), self.COLOR_TEXT)

        # 各セル描画
        for x in range(16):
            for y in range(8):
                cell_x = self.GRID_X + x * self.CELL_WIDTH
                cell_y = self.GRID_Y + y * self.CELL_HEIGHT

                # セルの背景色決定
                if x == self.sequencer.current_step and self.sequencer.playing:
                    # 現在再生中のステップ
                    cell_color = self.COLOR_ACTIVE
                elif x == self.input_manager.selected_step:
                    # 選択中のステップ
                    cell_color = self.COLOR_STEP
                else:
                    # 通常のセル
                    cell_color = self.COLOR_BG

                # セル描画
                pyxel.rect(cell_x, cell_y, self.CELL_WIDTH - 1, self.CELL_HEIGHT - 1, cell_color)

                # 音符があれば描画
                note_idx = 7 - y  # 音階は下から上へ
                if self.sequencer.steps[x] == self.notes[y]:
                    pyxel.rect(cell_x + 1, cell_y + 1, self.CELL_WIDTH - 3, self.CELL_HEIGHT - 3, self.COLOR_NOTE)


if __name__ == "__main__":
    PicoPixel()
