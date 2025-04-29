"""
シーケンサーモジュール - 音楽シーケンスの管理と再生を担当
"""

import pyxel


class Sequencer:
    """
    16ステップのシーケンサークラス
    音階データの管理と再生を行う
    """

    # 音階とPyxel音源のマッピング（ドレミファソラシド）
    NOTE_MAP = {
        "ド": 0,  # C
        "レ": 2,  # D
        "ミ": 4,  # E
        "ファ": 5,  # F
        "ソ": 7,  # G
        "ラ": 9,  # A
        "シ": 11,  # B
        "ド+": 12,  # C+
        None: None,  # 無音
    }

    def __init__(self):
        """シーケンサーの初期化"""
        # 16ステップのシーケンスデータ（初期値はすべてNone=無音）
        self.steps = [None for _ in range(16)]
        # 現在再生中のステップ位置
        self.current_step = 0
        # 再生状態フラグ
        self.playing = False
        # テンポ（BPM）- 固定値
        self.tempo = 120
        # 前回のフレーム時間（テンポ計算用）
        self.last_frame_time = 0
        # 音色（0-2: 矩形波、3: ノイズ）
        self.sound_type = 0

    def update(self):
        """
        シーケンサーの状態を更新する
        毎フレーム呼び出される
        """
        if not self.playing:
            return

        # テンポに基づいてステップを進める
        # 60 BPM = 1秒に1ステップ
        # 120 BPM = 0.5秒に1ステップ
        step_time = 60 / self.tempo  # 秒単位のステップ時間

        # 現在の時間
        current_time = pyxel.frame_count / 30  # 30FPSと仮定

        # ステップを進めるべき時間かチェック
        if current_time - self.last_frame_time >= step_time:
            self.last_frame_time = current_time

            # 現在のステップの音を鳴らす
            self.play_current_step()

            # 次のステップへ
            self.current_step = (self.current_step + 1) % 16

    def toggle_play(self):
        """再生/停止を切り替える"""
        self.playing = not self.playing

        if self.playing:
            # 再生開始時は最初のステップから
            self.current_step = 0
            self.last_frame_time = pyxel.frame_count / 30

    def input_note(self, step_idx, note):
        """
        指定したステップに音階を入力する

        Args:
            step_idx: ステップ位置（0-15）
            note: 音階名（"ド", "レ", etc.）またはNone（無音）
        """
        if 0 <= step_idx < 16:
            self.steps[step_idx] = note

    def play_current_step(self):
        """現在のステップの音を再生する"""
        note = self.steps[self.current_step]

        if note is not None:
            # 音階をPyxel音源の値に変換
            pyxel_note = self.NOTE_MAP[note]

            if pyxel_note is not None:
                # 音を鳴らす（チャンネル0、音色タイプ）
                # 音階に応じてサウンドを設定
                # 音階を正しいノート名に変換
                # C, D, E, F, G, A, B の順序に対応
                note_names = ["c", "d", "e", "f", "g", "a", "b"]
                octave = pyxel_note // 12
                note_idx = pyxel_note % 12

                # 半音の処理（シャープ/フラット）
                if note_idx in [1, 3, 6, 8, 10]:  # 黒鍵（シャープ）
                    # Pyxelでは半音は使えないので、近い音に丸める
                    note_idx = (note_idx + 1) // 2
                else:  # 白鍵
                    note_idx = note_idx // 2 if note_idx > 0 else 0

                note_name = f"{note_names[note_idx]}{octave}"

                pyxel.sounds[self.sound_type].set(
                    note_name,  # note (c0, d0, e0, etc.)
                    "s",  # tone (square wave)
                    "5",  # volume
                    "n",  # effect
                    15,  # speed
                )
                # サウンド再生
                pyxel.play(0, self.sound_type)

    def clear_step(self, step_idx):
        """指定したステップの音を消去する"""
        if 0 <= step_idx < 16:
            self.steps[step_idx] = None

    def clear_all(self):
        """すべてのステップをクリアする"""
        self.steps = [None for _ in range(16)]
