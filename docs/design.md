
# 要件・設計書

## 1. 要件定義

### 1.1 基本情報
- ソフトウェア名称: picopyxel
- リポジトリ名: picopyxel

### 1.2 プロジェクト概要
本プロジェクトは、Pyxelを用いて8bitスタイルの音楽シーケンサー「picopyxel」を開発し、
最終的にはポータブルゲームデバイス（例：Powkiddy RGB30）上で動作するオリジナル音楽制作アプリケーションを完成させることを目的とする。
開発はミニマム機能から始め、段階的に高機能なツールへと進化させる。

### 1.3 機能要件

#### 1.3.1 ミニマム版機能
- 1トラック構成
- 16ステップシーケンス
- 全音階入力（半音を含む12音階）
- オクターブ変更機能（0-4）
- 音色タイプ切替機能（三角波、矩形波、パルス波、ノイズ）
- キーボード＆ゲームパッド操作対応
- 再生・停止機能
- テンポ変更機能（60-240 BPM）

#### 1.3.2 バージョン2.0機能（今回の実装）
- 4トラック構成（同時に4つの音を鳴らせる）
- トラック切り替え機能
- トラックごとの音量調整
- ソングモード（複数のパターンを組み合わせて曲を作成）
- パターン管理（最大16パターン）
- パターンチェイン（パターンの連続再生）

#### 1.3.3 将来的な拡張予定機能
- 音色パラメータ詳細設定機能
- エフェクト追加（ビブラート、ピッチシフトなど）
- セーブ／ロード機能（ローカルファイル保存）
- 実機最適化（ボタン配置チューニング）
- UI改善（視認性・操作性向上）
- 将来的にはプラグインシステムの追加（外部音源拡張等）

### 1.4 非機能要件
- PCおよびポータブル実機（Powkiddy RGB30など）で動作すること
- Pyxelの制約（64音制限、低リソース環境）に対応すること
- 実機上でも快適なレスポンスを維持すること

### 1.5 制約条件
- Python 3.8以上
- Pyxel 1.9.0以上
- 実機側OS：plumOS-RN対応
- 配布形式：.pyxapp
- 使用ライブラリはPyxelに標準含まれる範囲を基本とする（外部依存を避ける）

### 1.6 開発環境
- 開発言語：Python
- ライブラリ：Pyxel
- 開発ツール：VSCode、Mac/Linuxターミナル
- 実機デバイス：Powkiddy RGB30（予定）

### 1.7 成果物
- ソースコード
- 実行用パッケージファイル（.pyxapp）
- ドキュメント（README、操作説明書）
- 要件・設計書（本ドキュメント）

## 2. システム設計

### 2.1 システム概要設計

#### 2.1.1 システムアーキテクチャ
```
[Input Manager] <-> [Sequencer Core] <-> [Sound Engine (Pyxel)] <-> [Visualizer]
```

#### 2.1.2 主要コンポーネント
- Input Manager：キー・ゲームパッド入力管理
- Sequencer Core：シーケンスデータ管理と再生制御
- Sound Engine：Pyxelの音源を使ったサウンド再生
- Visualizer：再生中のステップ表示

### 2.2 詳細設計

#### 2.2.1 データ設計
- ステップデータ：リスト形式（長さ16）
- 音階マッピング：ノート名とPyxel音源の対応表

#### 2.2.2 クラス設計

##### Sequencerクラス（更新版）
```python
class Sequencer:
    def __init__(self):
        # 4トラック対応
        self.tracks = [
            [None for _ in range(16)] for _ in range(4)  # 各トラック16ステップ
        ]
        self.track_volumes = [5, 5, 5, 5]  # 各トラックの音量（0-7）
        self.current_track = 0  # 現在編集中のトラック

        # パターン管理
        self.patterns = [
            [
                [None for _ in range(16)] for _ in range(4)
            ] for _ in range(16)  # 最大16パターン
        ]
        self.current_pattern = 0  # 現在編集中のパターン

        # ソングモード
        self.song_sequence = []  # パターン番号のリスト
        self.song_position = 0  # 現在再生中のソング位置
        self.song_mode = False  # ソングモード（True）かパターンモード（False）か

        # 基本パラメータ
        self.current_step = 0
        self.playing = False
        self.tempo = 120  # BPM
        self.current_note = "C"  # 現在選択中の音階
        self.current_octave = 4  # 現在選択中のオクターブ
        self.current_sound_type = 0  # 現在選択中の音色タイプ

    def update(self):
        # テンポに基づいてステップを進める
        pass

    def toggle_play(self):
        # 再生/停止を切り替える
        pass

    def input_note(self, step_idx, track_idx=None, note=None):
        # 指定したステップとトラックに音階を入力する
        pass

    def change_track(self, delta):
        # 編集するトラックを変更する
        pass

    def change_track_volume(self, delta):
        # 現在のトラックの音量を変更する
        pass

    def change_pattern(self, delta):
        # 編集するパターンを変更する
        pass

    def copy_pattern(self, source, destination):
        # パターンをコピーする
        pass

    def add_pattern_to_song(self, pattern_idx):
        # ソングにパターンを追加する
        pass

    def remove_pattern_from_song(self, position):
        # ソングからパターンを削除する
        pass

    def toggle_song_mode(self):
        # ソングモードとパターンモードを切り替える
        pass

    def change_octave(self, delta):
        # オクターブを変更する
        pass

    def change_sound_type(self, delta):
        # 音色タイプを変更する
        pass

    def change_note(self, delta):
        # 音階を変更する
        pass

    def change_tempo(self, delta):
        # テンポを変更する
        pass
```

##### InputManagerクラス（更新版）
```python
class InputManager:
    def __init__(self, sequencer):
        self.sequencer = sequencer
        self.selected_step = 0
        self.mode = 0  # 0: パターン編集、1: ソング編集、2: トラック設定
        self.using_gamepad = False  # ゲームパッド使用フラグ
        self.song_edit_position = 0  # ソング編集時の位置

    def update(self):
        # 入力状態を更新する
        pass

    def _handle_pattern_edit_mode(self):
        # パターン編集モードの入力処理
        pass

    def _handle_song_edit_mode(self):
        # ソング編集モードの入力処理
        pass

    def _handle_track_settings_mode(self):
        # トラック設定モードの入力処理
        pass

    def _is_key_pressed(self, key):
        # キーが押されたかどうかを判定
        pass

    def _is_gamepad_button_pressed(self, button):
        # ゲームパッドボタンが押されたかどうかを判定
        pass

    def _is_analog_triggered(self, axis, value, threshold):
        # アナログ入力が閾値を超えて変化したかを判定
        pass
```

#### 2.2.3 データフロー
1. 入力取得
2. モード判定（パターン編集/ソング編集/トラック設定）
3. シーケンスデータ更新
4. 再生時ステップ進行（パターンモード/ソングモード）
5. 画面描画

#### 2.2.4 エラーハンドリング
- 入力ミス
- ステップアクセスエラー

### 2.3 インターフェース設計
- 16ステップ×12音階表示
- 4トラック表示（色分け）
- 現在再生位置ハイライト
- 現在選択中の音階ハイライト
- 現在選択中のトラックハイライト
- パターン番号表示
- ソングシーケンス表示（ソングモード時）
- 再生状態、選択中のステップ、オクターブ、テンポ、音色タイプ表示
- モード表示（パターン編集/ソング編集/トラック設定）

### 2.4 セキュリティ設計
- 異常時でもクラッシュしない作り
- データ保存時はセーブファイル破損防止（将来対応）

### 2.5 テスト設計
- 単体テスト：入力、再生、移動
- 実機テスト：ボタン入力、再生確認
- 負荷テスト（将来）

### 2.6 開発環境・依存関係
- Python 3.8+
- Pyxel 1.9.0+
- plumOS-RN対応

### 2.7 開発工程
1. ミニマム版プロトタイピング
2. 実機動作確認
3. 機能拡張
4. 本格版リリース
