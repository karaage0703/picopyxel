"""
picopyxel - 8bitスタイルの音楽シーケンサー
バージョン2.0: 4トラック、パターン管理、ソングモード対応
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
        pyxel.init(self.WIDTH, self.HEIGHT, title="PicoPixel v2.0", fps=30)

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

        # トラック色
        self.TRACK_COLORS = [10, 9, 8, 12]  # 緑、オレンジ、灰色、青

        # グリッド設定
        self.GRID_X = 10
        self.GRID_Y = 30
        self.CELL_WIDTH = 8
        self.CELL_HEIGHT = 8
        self.GRID_WIDTH = 16 * self.CELL_WIDTH
        self.GRID_HEIGHT = 8 * self.CELL_HEIGHT

        # Pyxelアプリ実行
        pyxel.run(self.update, self.draw)

    def update(self):
        """状態更新（毎フレーム呼び出し）"""
        # 終了判定（ESCキーまたはSTARTボタン長押し）
        if pyxel.btnp(pyxel.KEY_ESCAPE) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_START) and pyxel.btn(pyxel.GAMEPAD1_BUTTON_BACK)):
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
        pyxel.text(5, 5, "PicoPixel v2.0 - 8bit Music Sequencer", self.COLOR_TEXT)

        # 現在のモードを表示
        mode_names = ["Pattern Edit", "Song Edit", "Track Settings"]
        mode_name = mode_names[self.input_manager.mode]
        pyxel.text(5, 15, f"Mode: {mode_name}", self.COLOR_TEXT)

        # 現在のパターン番号を表示
        pyxel.text(80, 15, f"Pattern: {self.sequencer.current_pattern + 1}", self.COLOR_TEXT)

        # 現在のトラック番号を表示
        track_color = self.TRACK_COLORS[self.sequencer.current_track]
        pyxel.text(125, 15, f"Track: {self.sequencer.current_track + 1}", track_color)

        # モードに応じた描画
        if self.input_manager.mode == self.input_manager.MODE_PATTERN_EDIT:
            # シーケンサーグリッド描画
            self._draw_sequencer_grid()
        elif self.input_manager.mode == self.input_manager.MODE_SONG_EDIT:
            # ソングシーケンス描画
            self._draw_song_sequence()
        elif self.input_manager.mode == self.input_manager.MODE_TRACK_SETTINGS:
            # トラック設定描画
            self._draw_track_settings()

        # 共通情報表示
        # 再生状態表示
        status = "PLAYING" if self.sequencer.playing else "STOPPED"
        song_mode = " (SONG)" if self.sequencer.song_mode else " (PATTERN)"
        pyxel.text(5, self.GRID_Y + self.GRID_HEIGHT + 5, f"Status: {status}{song_mode}", self.COLOR_TEXT)

        # 選択中のステップ表示（パターン編集モードのみ）
        if self.input_manager.mode == self.input_manager.MODE_PATTERN_EDIT:
            pyxel.text(
                5, self.GRID_Y + self.GRID_HEIGHT + 12, f"Step: {self.input_manager.selected_step + 1}", self.COLOR_TEXT
            )
            # 現在選択中の音階表示
            pyxel.text(45, self.GRID_Y + self.GRID_HEIGHT + 12, f"Note: {self.sequencer.current_note}", self.COLOR_TEXT)
            # オクターブ表示
            pyxel.text(5, self.GRID_Y + self.GRID_HEIGHT + 20, f"Oct: {self.sequencer.current_octave}", self.COLOR_TEXT)

        # テンポ表示
        pyxel.text(45, self.GRID_Y + self.GRID_HEIGHT + 20, f"Tempo: {self.sequencer.tempo}", self.COLOR_TEXT)

        # 音色タイプ表示（パターン編集モードのみ）
        if self.input_manager.mode == self.input_manager.MODE_PATTERN_EDIT:
            sound_types = ["Triangle", "Square", "Pulse", "Noise"]
            sound_type = sound_types[self.sequencer.current_sound_type]
            pyxel.text(90, self.GRID_Y + self.GRID_HEIGHT + 20, f"Sound: {sound_type}", self.COLOR_TEXT)

    def _draw_sequencer_grid(self):
        """シーケンサーグリッドの描画"""
        # グリッド背景
        pyxel.rectb(self.GRID_X - 1, self.GRID_Y - 1, self.GRID_WIDTH + 2, self.GRID_HEIGHT + 2, self.COLOR_GRID)

        # 音階ラベル描画（全12音階）
        note_names = ["B", "A#", "A", "G#", "G", "F#", "F", "E", "D#", "D", "C#", "C"]
        for i, note in enumerate(note_names):
            # 現在選択中の音階は強調表示
            color = self.COLOR_ACTIVE if note == self.sequencer.current_note else self.COLOR_TEXT
            pyxel.text(self.GRID_X - 9, self.GRID_Y + i * (self.CELL_HEIGHT * 8 / 12) + 1, note, color)

        # ステップ番号描画
        for i in range(16):
            if i % 4 == 0:  # 4拍子の区切りを強調
                pyxel.text(self.GRID_X + i * self.CELL_WIDTH, self.GRID_Y - 8, str(i + 1), self.COLOR_TEXT)

        # 各セル描画
        for x in range(16):
            for y in range(12):  # 12音階に対応
                cell_x = self.GRID_X + x * self.CELL_WIDTH
                cell_y = self.GRID_Y + y * (self.CELL_HEIGHT * 8 / 12)  # 高さを調整

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

                # 音符があれば描画（全トラック）
                for track_idx in range(self.sequencer.TRACK_COUNT):
                    step_data = self.sequencer.patterns[self.sequencer.current_pattern][track_idx][x]
                    if step_data is not None:
                        note, octave, sound_type = step_data
                        note_names = ["B", "A#", "A", "G#", "G", "F#", "F", "E", "D#", "D", "C#", "C"]

                        # 音階が一致するか確認（オクターブは考慮しない）
                        if note == note_names[y]:
                            # トラックに応じた色を使用
                            note_color = self.TRACK_COLORS[track_idx]

                            # 現在のトラックの音符は少し大きく表示
                            if track_idx == self.sequencer.current_track:
                                pyxel.rect(
                                    cell_x + 1, cell_y + 1, self.CELL_WIDTH - 3, self.CELL_HEIGHT * 8 / 12 - 3, note_color
                                )
                                # オクターブ表示（小さい数字）
                                pyxel.text(cell_x + 2, cell_y + 2, str(octave), self.COLOR_TEXT)
                            else:
                                # 他のトラックの音符は小さく表示
                                pyxel.rect(
                                    cell_x + 2, cell_y + 2, self.CELL_WIDTH - 5, self.CELL_HEIGHT * 8 / 12 - 5, note_color
                                )

    def _draw_song_sequence(self):
        """ソングシーケンスの描画"""
        # ソングシーケンスの背景
        pyxel.rectb(self.GRID_X - 1, self.GRID_Y - 1, self.GRID_WIDTH + 2, 20, self.COLOR_GRID)

        # ソングシーケンスのタイトル
        pyxel.text(self.GRID_X, self.GRID_Y - 8, "Song Sequence", self.COLOR_TEXT)

        # ソングシーケンスの内容
        if not self.sequencer.song_sequence:
            pyxel.text(self.GRID_X + 5, self.GRID_Y + 5, "No patterns in song", self.COLOR_TEXT)
        else:
            # 最大16パターンまで表示
            display_count = min(16, len(self.sequencer.song_sequence))
            for i in range(display_count):
                pattern_idx = self.sequencer.song_sequence[i]

                # 位置計算
                pos_x = self.GRID_X + (i % 8) * 18
                pos_y = self.GRID_Y + (i // 8) * 10

                # 背景色（選択中の位置は強調）
                bg_color = self.COLOR_ACTIVE if i == self.input_manager.song_edit_position else self.COLOR_BG
                pyxel.rect(pos_x, pos_y, 16, 8, bg_color)

                # パターン番号表示
                pyxel.text(pos_x + 2, pos_y + 1, f"P{pattern_idx + 1}", self.COLOR_TEXT)

                # 現在再生中のパターンをマーク
                if self.sequencer.playing and self.sequencer.song_mode and i == self.sequencer.song_position:
                    pyxel.rectb(pos_x - 1, pos_y - 1, 18, 10, self.COLOR_NOTE)

        # 操作ガイド
        pyxel.text(self.GRID_X, self.GRID_Y + 25, "Enter: Add pattern", self.COLOR_TEXT)
        pyxel.text(self.GRID_X, self.GRID_Y + 35, "Del: Remove pattern", self.COLOR_TEXT)
        pyxel.text(self.GRID_X, self.GRID_Y + 45, "Ctrl+D: Clear all", self.COLOR_TEXT)

    def _draw_track_settings(self):
        """トラック設定の描画"""
        # トラック設定の背景
        pyxel.rectb(self.GRID_X - 1, self.GRID_Y - 1, self.GRID_WIDTH + 2, 50, self.COLOR_GRID)

        # トラック設定のタイトル
        pyxel.text(self.GRID_X, self.GRID_Y - 8, "Track Settings", self.COLOR_TEXT)

        # 各トラックの設定を表示
        for i in range(self.sequencer.TRACK_COUNT):
            # 位置計算
            pos_x = self.GRID_X + 5
            pos_y = self.GRID_Y + i * 10 + 5

            # トラック番号と色
            track_color = self.TRACK_COLORS[i]

            # 背景色（現在選択中のトラックは強調）
            bg_color = self.COLOR_ACTIVE if i == self.sequencer.current_track else self.COLOR_BG
            pyxel.rect(pos_x - 2, pos_y - 2, self.GRID_WIDTH - 6, 10, bg_color)

            # トラック情報表示
            pyxel.text(pos_x, pos_y, f"Track {i + 1}", track_color)

            # 音量バー
            volume = self.sequencer.track_volumes[i]
            pyxel.text(pos_x + 50, pos_y, f"Volume: {volume}", self.COLOR_TEXT)

            # 音量バーの描画
            bar_x = pos_x + 100
            bar_width = volume * 5  # 0-7の音量を視覚化
            pyxel.rect(bar_x, pos_y, bar_width, 5, track_color)
            pyxel.rectb(bar_x - 1, pos_y - 1, 36, 7, self.COLOR_GRID)

        # 操作ガイド
        pyxel.text(self.GRID_X, self.GRID_Y + 45, "Up/Down: Adjust volume", self.COLOR_TEXT)


if __name__ == "__main__":
    PicoPixel()
