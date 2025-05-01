"""
シーケンサーモジュール - 音楽シーケンスの管理と再生を担当
"""

import pyxel


class Sequencer:
    """
    16ステップのシーケンサークラス
    音階データの管理と再生を行う
    """

    # 音階とPyxel音源のマッピング（全音階対応）
    NOTE_MAP = {
        "C": 0,  # ド
        "C#": 1,  # ド#
        "D": 2,  # レ
        "D#": 3,  # レ#
        "E": 4,  # ミ
        "F": 5,  # ファ
        "F#": 6,  # ファ#
        "G": 7,  # ソ
        "G#": 8,  # ソ#
        "A": 9,  # ラ
        "A#": 10,  # ラ#
        "B": 11,  # シ
        None: None,  # 無音
    }

    # オクターブ範囲（Pyxelの制限に合わせる）
    MIN_OCTAVE = 0
    MAX_OCTAVE = 4  # Pyxelでは0-4のみサポート

    # テンポ範囲
    MIN_TEMPO = 60  # 最小BPM
    MAX_TEMPO = 240  # 最大BPM
    TEMPO_STEP = 10  # テンポ変更の刻み幅

    def __init__(self):
        """シーケンサーの初期化"""
        # 16ステップのシーケンスデータ（初期値はすべてNone=無音）
        # 各ステップは (音階, オクターブ, 音色) のタプルで表現
        self.steps = [None for _ in range(16)]
        # 現在再生中のステップ位置
        self.current_step = 0
        # 再生状態フラグ
        self.playing = False
        # テンポ（BPM）
        self.tempo = 120
        # 前回のフレーム時間（テンポ計算用）
        self.last_frame_time = 0
        # 現在選択中のオクターブ
        self.current_octave = 4
        # 現在選択中の音階（デフォルトはC）
        self.current_note = "C"
        # 音色タイプ（0-3）
        # 0: 三角波(Triangle)、1: 矩形波(Square)、2: パルス波(Pulse)、3: ノイズ(Noise)
        self.sound_types = ["t", "s", "p", "n"]
        # 現在選択中の音色インデックス
        self.current_sound_type = 0
        # 全音階のリスト
        self.all_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

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

            # 次のステップへ
            self.current_step = (self.current_step + 1) % 16

            # 現在のステップの音を鳴らす
            self.play_current_step()

    def toggle_play(self):
        """再生/停止を切り替える"""
        self.playing = not self.playing

        if self.playing:
            # 再生開始時は最初のステップから
            self.current_step = 0
            self.last_frame_time = pyxel.frame_count / 30

    def input_note(self, step_idx, note=None):
        """
        指定したステップに音階を入力する

        Args:
            step_idx: ステップ位置（0-15）
            note: 音階名（"C", "C#", etc.）またはNone（無音）。Noneの場合は現在選択中の音階を使用
        """
        if 0 <= step_idx < 16:
            if note is None:
                if self.current_note is None:
                    # 音を消去
                    self.steps[step_idx] = None
                else:
                    # 現在選択中の音階を入力
                    self.steps[step_idx] = (self.current_note, self.current_octave, self.current_sound_type)
            else:
                # 指定された音階を入力
                self.steps[step_idx] = (note, self.current_octave, self.current_sound_type)

    def play_current_step(self):
        """現在のステップの音を再生する"""
        step_data = self.steps[self.current_step]

        if step_data is not None:
            note, octave, sound_type_idx = step_data

            # 音階をPyxel音源の値に変換
            pyxel_note = self.NOTE_MAP[note]

            if pyxel_note is not None:
                # 音階を正しいノート名に変換
                note_names = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
                note_name = f"{note_names[pyxel_note]}{octave}"

                # 音色タイプを取得
                sound_type = self.sound_types[sound_type_idx]

                # サウンド設定
                pyxel.sounds[sound_type_idx].set(
                    note_name,  # note (c0, c#0, d0, etc.)
                    sound_type,  # tone (s: square, v: vibrato, f: fade, n: noise)
                    "5",  # volume
                    "n",  # effect
                    15,  # speed
                )

                # サウンド再生
                pyxel.play(0, sound_type_idx)

    def clear_step(self, step_idx):
        """指定したステップの音を消去する"""
        if 0 <= step_idx < 16:
            self.steps[step_idx] = None

    def clear_all(self):
        """すべてのステップをクリアする"""
        self.steps = [None for _ in range(16)]

    def change_octave(self, delta):
        """
        オクターブを変更する

        Args:
            delta: 変更量（+1または-1）
        """
        self.current_octave = max(self.MIN_OCTAVE, min(self.MAX_OCTAVE, self.current_octave + delta))
        return self.current_octave

    def change_sound_type(self, delta):
        """
        音色タイプを変更する

        Args:
            delta: 変更量（+1または-1）
        """
        self.current_sound_type = (self.current_sound_type + delta) % len(self.sound_types)
        return self.current_sound_type, self.sound_types[self.current_sound_type]

    def change_note(self, delta):
        """
        音階を変更する

        Args:
            delta: 変更量（+1または-1）
        """
        current_idx = self.all_notes.index(self.current_note)
        new_idx = (current_idx + delta) % len(self.all_notes)
        self.current_note = self.all_notes[new_idx]
        return self.current_note

    def change_tempo(self, delta):
        """
        テンポを変更する

        Args:
            delta: 変更量（+1または-1）
        """
        # テンポを変更（TEMPO_STEPの倍数で変更）
        new_tempo = self.tempo + (delta * self.TEMPO_STEP)
        # 範囲内に収める
        self.tempo = max(self.MIN_TEMPO, min(self.MAX_TEMPO, new_tempo))
        return self.tempo
