"""
入力管理モジュール - キーボードとゲームパッド入力の処理を担当
"""

import pyxel


class InputManager:
    """
    キーボードとゲームパッド入力を管理するクラス
    """

    # キー入力と音階のマッピング
    KEY_TO_NOTE = {
        pyxel.KEY_Z: "ド",  # Z
        pyxel.KEY_S: "レ",  # S
        pyxel.KEY_X: "ミ",  # X
        pyxel.KEY_D: "ファ",  # D
        pyxel.KEY_C: "ソ",  # C
        pyxel.KEY_V: "ラ",  # V
        pyxel.KEY_G: "シ",  # G
        pyxel.KEY_B: "ド+",  # B
    }

    def __init__(self, sequencer):
        """
        入力マネージャーの初期化

        Args:
            sequencer: 操作対象のSequencerインスタンス
        """
        self.sequencer = sequencer
        # 現在選択中のステップ
        self.selected_step = 0
        # キー入力の前回状態（連続入力防止用）
        self.prev_keys = {}
        # 操作モード（0: 編集モード、1: 再生モード）
        self.mode = 0

    def update(self):
        """
        入力状態を更新する
        毎フレーム呼び出される
        """
        # 再生/停止切り替え
        if self._is_key_pressed(pyxel.KEY_SPACE):
            self.sequencer.toggle_play()

        # 編集モードの操作
        if self.mode == 0:
            self._handle_edit_mode()

        # 前回のキー状態を保存
        self._update_prev_keys()

    def _handle_edit_mode(self):
        """編集モードの入力処理"""
        # ステップ選択（左右移動）
        if self._is_key_pressed(pyxel.KEY_LEFT):
            self.selected_step = (self.selected_step - 1) % 16

        if self._is_key_pressed(pyxel.KEY_RIGHT):
            self.selected_step = (self.selected_step + 1) % 16

        # 音階入力
        for key, note in self.KEY_TO_NOTE.items():
            if self._is_key_pressed(key):
                self.sequencer.input_note(self.selected_step, note)

        # 音消去（DELキー）
        if self._is_key_pressed(pyxel.KEY_DELETE) or self._is_key_pressed(pyxel.KEY_BACKSPACE):
            self.sequencer.clear_step(self.selected_step)

        # 全消去（Ctrl+Dキー）
        if pyxel.btn(pyxel.KEY_CTRL) and self._is_key_pressed(pyxel.KEY_D):
            self.sequencer.clear_all()

    def _is_key_pressed(self, key):
        """
        キーが押されたかどうかを判定（前回の状態と比較して一度だけ反応）

        Args:
            key: チェックするキーコード

        Returns:
            bool: キーが新たに押されたらTrue
        """
        # 現在押されていて、前回は押されていなかった場合にTrue
        return pyxel.btnp(key) or (pyxel.btn(key) and key not in self.prev_keys)

    def _update_prev_keys(self):
        """前回のキー状態を更新"""
        self.prev_keys = {}
        for key in self.KEY_TO_NOTE.keys():
            if pyxel.btn(key):
                self.prev_keys[key] = True

        # 操作キーも記録
        for key in [pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_SPACE, pyxel.KEY_DELETE, pyxel.KEY_BACKSPACE, pyxel.KEY_D]:
            if pyxel.btn(key):
                self.prev_keys[key] = True
