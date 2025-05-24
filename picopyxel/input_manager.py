"""
入力管理モジュール - キーボードとゲームパッド入力の処理を担当
"""

import pyxel


class InputManager:
    """
    キーボードとゲームパッド入力を管理するクラス
    バージョン2.0: マルチトラック、パターン、ソングモード対応
    """

    # アナログ入力の閾値
    ANALOG_THRESHOLD = 16000

    # モード定数
    MODE_PATTERN_EDIT = 0  # パターン編集モード
    MODE_SONG_EDIT = 1  # ソング編集モード
    MODE_TRACK_SETTINGS = 2  # トラック設定モード

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
        self.prev_gamepad_buttons = {}
        self.prev_gamepad_axes = {}
        # 操作モード（0: パターン編集、1: ソング編集、2: トラック設定）
        self.mode = self.MODE_PATTERN_EDIT
        # ゲームパッド使用フラグ
        self.using_gamepad = False
        # ソング編集時の位置
        self.song_edit_position = 0

    def update(self):
        """
        入力状態を更新する
        毎フレーム呼び出される
        """
        # モード切替（Tabキーまたはゲームパッドのスタートボタン）
        if self._is_key_pressed(pyxel.KEY_TAB) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_START):
            self.mode = (self.mode + 1) % 3
            print(f"モード変更: {self.mode}")

        # 再生/停止切り替え（スペースキーまたはAボタン）
        if self._is_key_pressed(pyxel.KEY_SPACE) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_A):
            self.sequencer.toggle_play()

        # 共通操作
        # 音階選択（上下キーまたはゲームパッド十字キー上下）- パターン編集モードのみ
        if self.mode == self.MODE_PATTERN_EDIT:
            if self._is_key_pressed(pyxel.KEY_UP) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                new_note = self.sequencer.change_note(1)
                print(f"音階上げ: {new_note}")

            if self._is_key_pressed(pyxel.KEY_DOWN) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                new_note = self.sequencer.change_note(-1)
                print(f"音階下げ: {new_note}")

        # オクターブ変更（PageUp/PageDownキーまたはゲームパッドLRボタン）
        if self._is_key_pressed(pyxel.KEY_PAGEUP) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER):
            new_octave = self.sequencer.change_octave(1)
            print(f"オクターブ上げ: {new_octave}")

        if self._is_key_pressed(pyxel.KEY_PAGEDOWN) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER):
            new_octave = self.sequencer.change_octave(-1)
            print(f"オクターブ下げ: {new_octave}")

        # 音色タイプはトラックごとに固定されるため、この機能は不要になります

        # テンポ変更（hとlキーまたはゲームパッド右スティック左右）
        if self._is_key_pressed(pyxel.KEY_L):
            new_tempo = self.sequencer.change_tempo(1)
            print(f"テンポ上げ: {new_tempo} BPM")

        if self._is_key_pressed(pyxel.KEY_H):
            new_tempo = self.sequencer.change_tempo(-1)
            print(f"テンポ下げ: {new_tempo} BPM")

        # テンポ変更 - ゲームパッド右スティック左右
        right_x = pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTX)
        if self._is_analog_triggered(pyxel.GAMEPAD1_AXIS_RIGHTX, right_x, self.ANALOG_THRESHOLD):
            if right_x > 0:  # 右
                new_tempo = self.sequencer.change_tempo(1)
                print(f"テンポ上げ: {new_tempo} BPM")
            else:  # 左
                new_tempo = self.sequencer.change_tempo(-1)
                print(f"テンポ下げ: {new_tempo} BPM")

        # トラック切り替え（[と]キー、またはゲームパッドのトリガー）
        if self._is_key_pressed(pyxel.KEY_RIGHTBRACKET) or self._is_analog_triggered(
            pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT, pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT), self.ANALOG_THRESHOLD
        ):
            new_track = self.sequencer.change_track(1)
            print(f"トラック変更: {new_track}")

        if self._is_key_pressed(pyxel.KEY_LEFTBRACKET) or self._is_analog_triggered(
            pyxel.GAMEPAD1_AXIS_TRIGGERLEFT, pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERLEFT), self.ANALOG_THRESHOLD
        ):
            new_track = self.sequencer.change_track(-1)
            print(f"トラック変更: {new_track}")

        # パターン切り替え（,と.キー、またはゲームパッド右スティック上下）
        if self._is_key_pressed(pyxel.KEY_PERIOD):
            new_pattern = self.sequencer.change_pattern(1)
            print(f"パターン変更: {new_pattern}")

        if self._is_key_pressed(pyxel.KEY_COMMA):
            new_pattern = self.sequencer.change_pattern(-1)
            print(f"パターン変更: {new_pattern}")

        # パターン切り替え - ゲームパッド右スティック上下
        right_y = pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTY)
        if self._is_analog_triggered(pyxel.GAMEPAD1_AXIS_RIGHTY, right_y, self.ANALOG_THRESHOLD):
            if right_y > 0:  # 下
                new_pattern = self.sequencer.change_pattern(-1)
                print(f"パターン変更: {new_pattern}")
            else:  # 上
                new_pattern = self.sequencer.change_pattern(1)
                print(f"パターン変更: {new_pattern}")

        # ソングモード切り替え（SキーまたはゲームパッドのYボタン）
        if self._is_key_pressed(pyxel.KEY_S) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_Y):
            song_mode = self.sequencer.toggle_song_mode()
            print(f"ソングモード: {'ON' if song_mode else 'OFF'}")

        # 各モードの操作
        if self.mode == self.MODE_PATTERN_EDIT:
            self._handle_pattern_edit_mode()
        elif self.mode == self.MODE_SONG_EDIT:
            self._handle_song_edit_mode()
        elif self.mode == self.MODE_TRACK_SETTINGS:
            self._handle_track_settings_mode()

        # 前回の入力状態を保存
        self._update_prev_inputs()

    def _handle_pattern_edit_mode(self):
        """パターン編集モードの入力処理"""
        # ステップ選択（左右移動）- キーボード
        if self._is_key_pressed(pyxel.KEY_LEFT):
            self.selected_step = (self.selected_step - 1) % 16

        if self._is_key_pressed(pyxel.KEY_RIGHT):
            self.selected_step = (self.selected_step + 1) % 16

        # ステップ選択（左右移動）- ゲームパッド左スティックまたは十字キー左右
        left_x = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX)
        if self._is_analog_triggered(pyxel.GAMEPAD1_AXIS_LEFTX, left_x, self.ANALOG_THRESHOLD):
            if left_x > 0:  # 右
                self.selected_step = (self.selected_step + 1) % 16
            else:  # 左
                self.selected_step = (self.selected_step - 1) % 16

        # ステップ選択（左右移動）- ゲームパッド十字キー左右
        if self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.selected_step = (self.selected_step - 1) % 16

        if self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.selected_step = (self.selected_step + 1) % 16

        # 音階入力 - キーボード（Enterキー）
        if self._is_key_pressed(pyxel.KEY_RETURN):
            self.sequencer.input_note(self.selected_step)
            print(f"音階入力: {self.sequencer.current_note} (オクターブ: {self.sequencer.current_octave})")

        # 音階入力 - ゲームパッド（Bボタン）
        if self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_B):
            self.sequencer.input_note(self.selected_step)
            print(f"音階入力: {self.sequencer.current_note} (オクターブ: {self.sequencer.current_octave})")

        # 音消去（DELキー または ゲームパッドのBACKボタン）
        if (
            self._is_key_pressed(pyxel.KEY_DELETE)
            or self._is_key_pressed(pyxel.KEY_BACKSPACE)
            or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_BACK)
        ):
            self.sequencer.clear_step(self.selected_step)

        # 全消去（Ctrl+Dキー または ゲームパッドのGUIDEボタン長押し）
        if (pyxel.btn(pyxel.KEY_CTRL) and self._is_key_pressed(pyxel.KEY_D)) or (
            pyxel.btn(pyxel.GAMEPAD1_BUTTON_GUIDE) and pyxel.btn(pyxel.GAMEPAD1_BUTTON_BACK)
        ):
            self.sequencer.clear_all()

        # パターンコピー（Ctrl+Cキー）
        if pyxel.btn(pyxel.KEY_CTRL) and self._is_key_pressed(pyxel.KEY_C):
            # 次のパターンにコピー
            next_pattern = (self.sequencer.current_pattern + 1) % self.sequencer.PATTERN_COUNT
            self.sequencer.copy_pattern(self.sequencer.current_pattern, next_pattern)
            print(f"パターンコピー: {self.sequencer.current_pattern} -> {next_pattern}")

    def _handle_song_edit_mode(self):
        """ソング編集モードの入力処理"""
        # ソング位置選択（左右移動）
        if self._is_key_pressed(pyxel.KEY_LEFT):
            if len(self.sequencer.song_sequence) > 0:
                self.song_edit_position = (self.song_edit_position - 1) % len(self.sequencer.song_sequence)

        if self._is_key_pressed(pyxel.KEY_RIGHT):
            if len(self.sequencer.song_sequence) > 0:
                self.song_edit_position = (self.song_edit_position + 1) % len(self.sequencer.song_sequence)

        # パターン追加（EnterキーまたはゲームパッドのBボタン）
        if self._is_key_pressed(pyxel.KEY_RETURN) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_B):
            self.sequencer.add_pattern_to_song(self.sequencer.current_pattern)
            print(f"パターン追加: {self.sequencer.current_pattern}")

        # パターン削除（DELキーまたはゲームパッドのXボタン）
        if (
            self._is_key_pressed(pyxel.KEY_DELETE)
            or self._is_key_pressed(pyxel.KEY_BACKSPACE)
            or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_X)
        ):
            if len(self.sequencer.song_sequence) > 0:
                self.sequencer.remove_pattern_from_song(self.song_edit_position)
                print(f"パターン削除: 位置 {self.song_edit_position}")
                # 位置調整
                if len(self.sequencer.song_sequence) > 0:
                    self.song_edit_position = min(self.song_edit_position, len(self.sequencer.song_sequence) - 1)
                else:
                    self.song_edit_position = 0

        # ソングクリア（Ctrl+Dキー）
        if pyxel.btn(pyxel.KEY_CTRL) and self._is_key_pressed(pyxel.KEY_D):
            self.sequencer.song_sequence = []
            self.song_edit_position = 0
            print("ソングクリア")

    def _handle_track_settings_mode(self):
        """トラック設定モードの入力処理"""
        # 音量調整（上下キー）
        if self._is_key_pressed(pyxel.KEY_UP) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            new_volume = self.sequencer.change_track_volume(1)
            print(f"トラック{self.sequencer.current_track}の音量上げ: {new_volume}")

        if self._is_key_pressed(pyxel.KEY_DOWN) or self._is_gamepad_button_pressed(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            new_volume = self.sequencer.change_track_volume(-1)
            print(f"トラック{self.sequencer.current_track}の音量下げ: {new_volume}")

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

    def _is_gamepad_button_pressed(self, button):
        """
        ゲームパッドボタンが押されたかどうかを判定

        Args:
            button: チェックするボタンコード

        Returns:
            bool: ボタンが新たに押されたらTrue
        """
        return pyxel.btnp(button) or (pyxel.btn(button) and button not in self.prev_gamepad_buttons)

    def _is_analog_triggered(self, axis, value, threshold):
        """
        アナログ入力が閾値を超えて変化したかを判定

        Args:
            axis: チェックする軸
            value: 現在の値
            threshold: 閾値

        Returns:
            bool: 閾値を超えて変化した場合True
        """
        # 閾値を超えていない場合はFalse
        if abs(value) < threshold:
            return False

        # 前回の値を取得
        prev_value = self.prev_gamepad_axes.get(axis, 0)

        # 前回も閾値を超えていた場合はFalse（連続入力防止）
        if abs(prev_value) >= threshold and (value > 0) == (prev_value > 0):
            return False

        return True

    def _update_prev_inputs(self):
        """前回の入力状態を更新"""
        # キーボード
        self.prev_keys = {}

        # 操作キーも記録
        for key in [
            pyxel.KEY_LEFT,
            pyxel.KEY_RIGHT,
            pyxel.KEY_UP,
            pyxel.KEY_DOWN,
            pyxel.KEY_SPACE,
            pyxel.KEY_DELETE,
            pyxel.KEY_BACKSPACE,
            pyxel.KEY_D,
            pyxel.KEY_PAGEUP,
            pyxel.KEY_PAGEDOWN,
            pyxel.KEY_RETURN,
            pyxel.KEY_J,
            pyxel.KEY_K,
            pyxel.KEY_H,
            pyxel.KEY_L,
            pyxel.KEY_TAB,
            pyxel.KEY_S,
            pyxel.KEY_C,
            pyxel.KEY_LEFTBRACKET,
            pyxel.KEY_RIGHTBRACKET,
            pyxel.KEY_COMMA,
            pyxel.KEY_PERIOD,
        ]:
            if pyxel.btn(key):
                self.prev_keys[key] = True

        # ゲームパッドボタン
        self.prev_gamepad_buttons = {}

        # 操作ボタンも記録
        for button in [
            pyxel.GAMEPAD1_BUTTON_START,
            pyxel.GAMEPAD1_BUTTON_BACK,
            pyxel.GAMEPAD1_BUTTON_GUIDE,
            pyxel.GAMEPAD1_BUTTON_DPAD_UP,
            pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,
            pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,
            pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,
            pyxel.GAMEPAD1_BUTTON_A,
            pyxel.GAMEPAD1_BUTTON_B,
            pyxel.GAMEPAD1_BUTTON_X,
            pyxel.GAMEPAD1_BUTTON_Y,
            pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER,
            pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER,
        ]:
            if pyxel.btn(button):
                self.prev_gamepad_buttons[button] = True

        # アナログ入力
        self.prev_gamepad_axes = {
            pyxel.GAMEPAD1_AXIS_LEFTX: pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX),
            pyxel.GAMEPAD1_AXIS_LEFTY: pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY),
            pyxel.GAMEPAD1_AXIS_RIGHTX: pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTX),
            pyxel.GAMEPAD1_AXIS_RIGHTY: pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTY),
            pyxel.GAMEPAD1_AXIS_TRIGGERLEFT: pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERLEFT),
            pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT: pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT),
        }
