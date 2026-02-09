# AbletonOSC: OSCでAbleton Liveをコントロール

[![stability-beta](https://img.shields.io/badge/stability-beta-33bbff.svg)](https://github.com/mkenney/software-guides/blob/master/STABILITY-BADGES.md#beta)

AbletonOSCは、[Open Sound Control (OSC)](https://ccrma.stanford.edu/groups/osc/) インターフェースを提供し、[Ableton Live](https://www.ableton.com/en/live/) をコントロールするためのMIDIリモートスクリプトです。このプロジェクトの目的は、[Live Object Model (LOM)](https://docs.cycling74.com/max8/vignettes/live_object_model) API全体（[完全なAPIドキュメント](https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml)）を公開し、LOMと同じ命名構造とオブジェクト階層を使用して、Liveのコントロールインターフェースに対する包括的な制御を提供することです。

# インストール

AbletonOSCにはAbleton Live 11以上が必要です。

スクリプトをインストールするには:

- [このリポジトリのzipをダウンロード](https://github.com/ideoforms/AbletonOSC/archive/refs/heads/master.zip)し、解凍して、`AbletonOSC-master` を `AbletonOSC` にリネームします。
- Abletonの[サードパーティ製リモートスクリプトのインストール](https://help.ableton.com/hc/en-us/articles/209072009-Installing-third-party-remote-scripts)ドキュメントの手順に従い、`AbletonOSC` フォルダを以下にコピーしてインストールします:
    - **Windows**: `\Users\[username]\Documents\Ableton\User Library\Remote Scripts`
    - **macOS**: `Macintosh HD/Users/[username]/Music/Ableton/User Library/Remote Scripts`
- Liveを再起動します。
- `Preferences > Link / Tempo / MIDI` の `Control Surface` ドロップダウンで、新しい "AbletonOSC" オプションを選択します。Liveは "AbletonOSC: Listening for OSC on port 11000" というメッセージを表示するはずです。

アクティビティログは `logs` サブディレクトリに出力されます。ログの粒度は `/live/api/set/log_level` で制御できます（以下の [Application API](#application-api) を参照）。

# 使い方

AbletonOSCはポート **11000** でOSCメッセージをリッスンし、ポート **11001** で応答を送信します。応答は、元のメッセージと同じIPに送信されます。プロパティを照会する場合、OSCワイルドカードパターンを使用できます。たとえば、`/live/clip/get/* 0 0` は、トラック0、クリップ0のすべてのプロパティを照会します。

## Application API

<details>
<summary><b>ドキュメント</b>: Application API</summary>

| Address                       | Query params | Response params              | Description                                                                              |
|:------------------------------|:-------------|:-----------------------------|:-----------------------------------------------------------------------------------------|
| /live/test                    |              | 'ok'                         | Liveで確認メッセージを表示し、/live/test にOSC応答を送信します             |
| /live/application/get/version |              | major_version, minor_version | Liveのバージョンを照会します                                                                     |
| /live/api/reload              |              |                              | AbletonOSCサーバーコードのライブリロードを開始します。開発時のみ使用されます。         |
| /live/api/get/log_level       |              | log_level                    | 現在のログレベルを返します。デフォルトは `info` です。                                        |
| /live/api/set/log_level       | log_level    |                              | ログレベルを設定します。値は次のいずれかです: `debug`, `info`, `warning`, `error`, `critical` |
| /live/api/show_message        | message      |                              | Liveのステータスバーにメッセージを表示します                                                      |

### アプリケーションステータスメッセージ

これらのメッセージは、アプリケーションの状態が変化したときにクライアントに自動的に送信されます。

| Address       | Response params | Description                                                                                        |
|:--------------|:----------------|:---------------------------------------------------------------------------------------------------|
| /live/startup |                 | AbletonOSCが起動したときにクライアントアプリケーションに送信されます                                          |
| /live/error   | error_msg       | エラーが発生したときにクライアントアプリケーションに送信されます。詳細な診断については logs/abletonosc.log を参照してください |

</details>

---

## Song API

トップレベルのSongオブジェクトを表します。再生の開始/停止、シーンの作成/変更、キューポイントの作成/ジャンプ、グローバルパラメータ（テンポ、メトロノーム）の設定に使用されます。

<details>
<summary><b>ドキュメント</b>: Song API</summary>

### Song methods

| Address                           | Query params | Response params | Description                                                                              |
|:----------------------------------|:-------------|:----------------|:-----------------------------------------------------------------------------------------|
| /live/song/capture_midi           |              |                 | MIDIをキャプチャします                                                                             |
| /live/song/continue_playing       |              |                 | セッション再生を再開します                                                                  |
| /live/song/create_audio_track     | index        |                 | 指定されたインデックスに新しいオーディオトラックを作成します（-1 = リストの末尾）                       |
| /live/song/create_midi_track      | index        |                 | 指定されたインデックスに新しいMIDIトラックを作成します（-1 = リストの末尾）                        |
| /live/song/create_return_track    |              |                 | 新しいリターントラックを作成します                                                                |
| /live/song/create_scene           | index        |                 | 指定されたインデックスに新しいシーンを作成します（-1 = リストの末尾）                             |
| /live/song/cue_point/jump         | cue_point    |                 | 名前または数値インデックス（キューポイントのリストに基づく）で特定のキューポイントにジャンプします |
| /live/song/cue_point/add_or_delete |             |                 | カーソル位置にキューポイントを追加するか、存在する場合は削除します |
| /live/song/cue_point/set/name         | cue_point    |                 | インデックスを指定してキューポイントの名前を変更します |
| /live/song/delete_scene           | scene_index  |                 | シーンを削除します                                                                           |
| /live/song/delete_return_track    | track_index  |                 | リターントラックを削除します                                                                    |
| /live/song/delete_track           | track_index  |                 | トラックを削除します                                                                           |
| /live/song/duplicate_scene        | scene_index  |                 | シーンを複製します                                                                        |
| /live/song/duplicate_track        | track_index  |                 | トラックを複製します                                                                        |
| /live/song/jump_by                | time         |                 | 指定された時間（拍単位）だけ曲の位置をジャンプします                                       |
| /live/song/jump_to_next_cue       |              |                 | 次のキューマーカーへジャンプします                                                              |
| /live/song/jump_to_prev_cue       |              |                 | 前のキューマーカーへジャンプします                                                          |
| /live/song/redo                   |              |                 | 最後に元に戻した操作をやり直します                                                           |
| /live/song/start_playing          |              |                 | セッション再生を開始します                                                                   |
| /live/song/stop_playing           |              |                 | セッション再生を停止します                                                                    |
| /live/song/stop_all_clips         |              |                 | すべてのクリップの再生を停止します                                                              |
| /live/song/tap_tempo              |              |                 | "Tap Tempo" ボタンのタップを模倣します                                                   |
| /live/song/trigger_session_record |              |                 | セッションモードで録音をトリガーします                                                          |
| /live/song/undo                   |              |                 | 最後の操作を元に戻します                                                                  |

### Song properties

 - 任意のTrackプロパティの変更をリッスンするには、`/live/song/start_listen/<property>` を呼び出します
 - 応答は `/live/song/get/<property>` に送信され、パラメータは `<property_value>` です
 - これらのプロパティとそのパラメータの詳細については、[Live Object Model - Song](https://docs.cycling74.com/max8/vignettes/live_object_model#Song) のドキュメントを参照してください。
 
#### Getters

| Address                                    | Query params | Response params             | Description                                       |
|:-------------------------------------------|:-------------|:----------------------------|:--------------------------------------------------|
| /live/song/get/arrangement_overdub         |              | arrangement_overdub         | アレンジメントオーバーダブがオンかどうかを照会します           |
| /live/song/get/back_to_arranger            |              | back_to_arranger            | "back to arranger" が点灯しているかどうかを照会します           |
| /live/song/get/can_redo                    |              | can_redo                    | やり直しが可能かどうかを照会します                   |
| /live/song/get/can_undo                    |              | can_undo                    | 元に戻すことが可能かどうかを照会します                   |
| /live/song/get/clip_trigger_quantization   |              | clip_trigger_quantization   | 現在のクリップトリガークオンタイゼーションレベルを照会します |
| /live/song/get/current_song_time           |              | current_song_time           | 現在の曲の時間（拍単位）を照会します             |
| /live/song/get/groove_amount               |              | groove_amount               | 現在のグルーヴ量を照会します                   |
| /live/song/get/is_playing                  |              | is_playing                  | 曲が現在再生中かどうかを照会します       |
| /live/song/get/loop                        |              | loop                        | 曲が現在ループ中かどうかを照会します       |
| /live/song/get/loop_length                 |              | loop_length                 | 現在のループレングスを照会します                     |
| /live/song/get/loop_start                  |              | loop_start                  | 現在のループ開始点を照会します                |
| /live/song/get/metronome                   |              | metronome_on                | メトロノームのオン/オフを照会します                            |
| /live/song/get/midi_recording_quantization |              | midi_recording_quantization | 現在のMIDI録音クオンタイゼーションを照会します     |
| /live/song/get/nudge_down                  |              | nudge_down                  | ナッジダウンを照会します                                  |
| /live/song/get/nudge_up                    |              | nudge_up                    | ナッジアップを照会します                                    |
| /live/song/get/punch_in                    |              | punch_in                    | パンチインを照会します                                    |
| /live/song/get/punch_out                   |              | punch_out                   | パンチアウトを照会します                                   |
| /live/song/get/record_mode                 |              | record_mode                 | 現在のレコードモードを照会します                     |
| /live/song/get/root_note                 |              | root_note                 | 現在のルートノートを照会します                     |
| /live/song/get/scale_name                 |              | scale_name                 | 現在のスケール名を照会します                     |
| /live/song/get/session_record              |              | session_record              | セッション録音が有効かどうかを照会します           |
| /live/song/get/session_record_status       |              | session_record_status       | 現在のセッション録音ステータスを照会します           |
| /live/song/get/signature_denominator       |              | denominator                 | 現在の拍子の分母を照会します    |
| /live/song/get/signature_numerator         |              | numerator                   | 現在の拍子の分子を照会します      |
| /live/song/get/song_length                 |              | song_length                 | 曲のアレンジメントの長さ（拍単位）を照会します       |
| /live/song/get/tempo                       |              | tempo_bpm                   | 現在の曲のテンポを照会します                      |

#### Setters

| Address                                    | Query params                | Response params | Description                                             |
|:-------------------------------------------|:----------------------------|:----------------|:--------------------------------------------------------|
| /live/song/set/arrangement_overdub         | arrangement_overdub         |                 | アレンジメントオーバーダブを設定します (1=on, 0=off)                   |
| /live/song/set/back_to_arranger            | back_to_arranger            |                 | "back to arranger" が点灯しているかどうかを設定します (1=on, 0=off)。アレンジメントに戻るには `0` を送信します。     |
| /live/song/set/clip_trigger_quantization   | clip_trigger_quantization   |                 | 現在のクリップトリガークオンタイゼーションレベルを設定します         |
| /live/song/set/current_song_time           | current_song_time           |                 | 現在の曲の時間（拍単位）を設定します                     |
| /live/song/set/groove_amount               | groove_amount               |                 | 現在のグルーヴ量を設定します                           |
| /live/song/set/loop                        | loop                        |                 | 曲が現在ループ中かどうかを設定します (1=on, 0=off) |
| /live/song/set/loop_length                 | loop_length                 |                 | 現在のループレングスを設定します                             |
| /live/song/set/loop_start                  | loop_start                  |                 | 現在のループ開始点を設定します                        |
| /live/song/set/metronome                   | metronome_on                |                 | メトロノームを設定します (1=on, 0=off)                             |
| /live/song/set/midi_recording_quantization | midi_recording_quantization |                 | 現在のMIDI録音クオンタイゼーションを設定します             |
| /live/song/set/nudge_down                  | nudge_down                  |                 | ナッジダウンを設定します                                          |
| /live/song/set/nudge_up                    | nudge_up                    |                 | ナッジアップを設定します                                            |
| /live/song/set/punch_in                    | punch_in                    |                 | パンチインを設定します                                           |
| /live/song/set/punch_out                   | punch_out                   |                 | パンチアウトを設定します                                           |
| /live/song/set/record_mode                 | record_mode                 |                 | 現在のレコードモードを設定します                             |
| /live/song/set/session_record              | session_record              |                 | セッション録音が有効かどうかを設定します (1=on, 0=off)     |
| /live/song/set/signature_denominator       | signature_denominator       |                 | 拍子の分母を設定します                    |
| /live/song/set/signature_numerator         | signature_numerator         |                 | 拍子の分子を設定します                      |
| /live/song/set/record_mode                 | record_mode                 |                 | 現在のレコードモードを設定します                             |
| /live/song/set/tempo                       | tempo_bpm                   |                 | 現在の曲のテンポを設定します                              |

### Song: Properties of cue points, scenes and tracks

| Address                    | Query params | Response params        | Description                                                                 |
|:---------------------------|:-------------|:-----------------------|:----------------------------------------------------------------------------|
| /live/song/get/cue_points  |              | name, time, ...        | 曲のキューポイントのリストを照会します                                       |
| /live/song/get/num_scenes  |              | num_scenes             | シーン数を照会します                                                  |
| /live/song/get/num_tracks  |              | num_tracks             | トラック数を照会します                                                  |
| /live/song/get/track_names |              | [index_min, index_max] | トラック名を照会します（オプションで指定範囲）                          |
| /live/song/get/track_data  |              | [various]              | 複数のトラック/クリップのプロパティを一括照会します。詳細については以下を参照してください。 |


#### /live/song/get/track_data を使用したトラック/クリップデータの一括照会

多くの異なるトラックやクリップに関するデータを一度に照会できると便利な場合があります。たとえば、セットが最初に開かれたときに、クライアントの状態をAbletonセットと同期させる場合などです。これは `/live/song/get/track_data` APIを使用して実現でき、複数のトラックやクリップのユーザー指定のプロパティを照会できます。

プロパティは `track.property_name`、`clip.property_name`、または `clip_slot.property_name` の形式である必要があります。

例:
```
/live/song/get/track_data 0 12 track.name clip.name clip.length
```

トラック0..11を照会し、以下のような値の長いリストを返します:

```
[track_0_name, clip_0_0_name,   clip_0_1_name,   ... clip_0_7_name,
               clip_1_0_length, clip_0_1_length, ... clip_0_7_length,
 track_1_name, clip_1_0_name,   clip_1_1_name,   ... clip_1_7_name, ...]
```

### ビートイベント

各ビートごとにクライアントにステータスメッセージを送信するように要求するには、`/live/song/start_listen/beat` を呼び出します。各ビートごとに、`/live/song/get/beat` への応答が送信され、現在のビート番号を含むintパラメータが付きます。ビートイベントのリッスンを停止するには、`/live/song/stop_listen/beat` を呼び出します。

</details>

---

## View API

Liveのビュー（ユーザーインターフェース）を表します

<details>
<summary><b>ドキュメント</b>: View API</summary>

| Address                                | Query params             | Response params          | Description                                             |
|:---------------------------------------|:-------------------------|:-------------------------|:--------------------------------------------------------|
| /live/view/get/selected_scene          |                          | scene_index              | 選択されているシーンのインデックスを返します（最初のシーン=0）      |
| /live/view/get/selected_track          |                          | track_index              | 選択されているトラックのインデックスを返します（最初のトラック=0）      |
| /live/view/get/selected_clip           |                          | track_index, scene_index | 選択されているクリップのトラックとシーンのインデックスを返します  |
| /live/view/get/selected_device         |                          | track_index, device_index| 選択されているデバイスを取得します（最初のデバイス=0）              |
| /live/view/set/selected_scene          | scene_index              |                          | 選択するシーンを設定します（最初のシーン=0）                |
| /live/view/set/selected_track          | track_index              |                          | 選択するトラックを設定します（最初のトラック=0）                |
| /live/view/set/selected_clip           | track_index, scene_index |                          | 選択するクリップを設定します                                   |
| /live/view/set/selected_device         | track_index, device_index|                          | 選択するデバイスを設定します（最初のデバイス=0）              |
| /live/view/start_listen/selected_scene |                          | selected_scene           | 選択されているシーンのリッスンを開始します（最初のシーン=0） |
| /live/view/start_listen/selected_track |                          | selected_track           | 選択されているトラックのリッスンを開始します（最初のトラック=0）     |
| /live/view/stop_listen/selected_scene  |                          |                          | 選択されているシーンのリッスンを停止します（最初のシーン=0）  |
| /live/view/stop_listen/selected_track  |                          |                          | 選択されているトラックのリッスンを停止します（最初のトラック=0）      |
</details>

---

## Track API

オーディオ、MIDI、リターン、またはマスタートラックを表します。トラックオーディオパラメータ（ボリューム、パンニング、センド、ミュート、ソロ）の設定、再生中のクリップスロットのリッスン、デバイスの照会などに使用できます。また、アレンジメントビューのクリップを照会するためにも使用できます。

トラックの指定（`track_id`）には、数値インデックス（0から開始）のほかに、以下の形式が使用できます：
- **トラック名**: 例 `"FilterTrack"`
- **マスター**: `"master"`
- **リターン**: `"return A"`, `"return B"` ... または `"return 0"`, `"return 1"` ...
- **全トラック**: `"*"`

複数のトラックのプロパティを照会するには、[Song: Properties of cue points, scenes and tracks](#song-properties-of-cue-points-scenes-and-tracks) を参照してください。

<details>
<summary><b>ドキュメント</b>: Track API</summary>

### Track methods

| Address                    | Query params | Response params | Description             |
|:---------------------------|:-------------|:----------------|:------------------------|
| /live/track/stop_all_clips | track_id     |                 | トラック上のすべてのクリップを停止します |

### Track properties

 - 任意のTrackプロパティの変更をリッスンするには、`/live/track/start_listen/<property> <track_index>` を呼び出します
 - 応答は `/live/track/get/<property>` に送信され、パラメータは `<track_index> <property_value>` です

#### Getters

| Address                                           | Query params      | Response params            | Description                                       |
|:--------------------------------------------------|:------------------|:---------------------------|:--------------------------------------------------|
| /live/track/get/arm                               | track_id          | track_id, armed            | トラックがアームされているかどうかを照会します                      |
| /live/track/get/available_input_routing_channels  | track_id          | track_id, channel, ...     | 入力チャンネルをリストします (例: "1", "2", "1/2", ...)   |
| /live/track/get/available_input_routing_types     | track_id          | track_id, type, ...        | 入力ルートをリストします (例: "Ext. In", ...)           |
| /live/track/get/available_output_routing_channels | track_id          | track_id, channel, ...     | 出力チャンネルをリストします (例: "1", "2", "1/2", ...)  |
| /live/track/get/available_output_routing_types    | track_id          | track_id, type, ...        | 出力ルートをリストします (例: "Ext. Out", ...)         |
| /live/track/get/can_be_armed                      | track_id          | track_id, can_be_armed     | トラックがアーム可能かどうかを照会します                  |
| /live/track/get/color                             | track_id          | track_id, color            | トラックの色を照会します                                 |
| /live/track/get/color_index                       | track_id          | track_id, color_index      | トラックのカラーインデックスを照会します                           |
| /live/track/get/current_monitoring_state          | track_id          | track_id, state            | 現在のモニタリング状態を照会します (1=on, 0=off)      |
| /live/track/get/fired_slot_index                  | track_id          | track_id, index            | 現在ファイアされているスロットを照会します                        |
| /live/track/get/fold_state                        | track_id          | track_id, fold_state       | 折りたたみ状態を照会します（グループ用）                   |
| /live/track/get/has_audio_input                   | track_id          | track_id, has_audio_input  | has_audio_inputを照会します                             |
| /live/track/get/has_audio_output                  | track_id          | track_id, has_audio_output | has_audio_outputを照会します                            |
| /live/track/get/has_midi_input                    | track_id          | track_id, has_midi_input   | has_midi_inputを照会します                              |
| /live/track/get/has_midi_output                   | track_id          | track_id, has_midi_output  | has_midi_outputを照会します                             |
| /live/track/get/input_routing_channel             | track_id          | track_id, channel          | 現在の入力ルーティングチャンネルを照会します               |
| /live/track/get/input_routing_type                | track_id          | track_id, type             | 現在の入力ルーティングタイプを照会します                  |
| /live/track/get/output_routing_channel            | track_id          | track_id, channel          | 現在の出力ルーティングチャンネルを照会します              |
| /live/track/get/output_meter_left                 | track_id          | track_id, level            | 現在の出力レベル（左チャンネル）を照会します          |
| /live/track/get/output_meter_level                | track_id          | track_id, level            | 現在の出力レベル（両方のチャンネル）を照会します         |
| /live/track/get/output_meter_right                | track_id          | track_id, level            | 現在の出力レベル（右チャンネル）を照会します         |
| /live/track/get/output_routing_type               | track_id          | track_id, type             | 現在の出力ルーティングタイプを照会します                 |
| /live/track/get/is_foldable                       | track_id          | track_id, is_foldable      | トラックが折りたたみ可能（グループ）かどうかを照会します  |
| /live/track/get/is_grouped                        | track_id          | track_id, is_grouped       | トラックがグループ内にあるかどうかを照会します                 |
| /live/track/get/is_visible                        | track_id          | track_id, is_visible       | トラックが表示されているかどうかを照会します (1=on, 0=off)      |
| /live/track/get/mute                              | track_id          | track_id, mute             | トラックのミュートを照会します (1=on, 0=off)                    |
| /live/track/get/name                              | track_id          | track_id, name             | トラック名を照会します                                  |
| /live/track/get/panning                           | track_id          | track_id, panning          | トラックのパンニングを照会します                               |
| /live/track/get/playing_slot_index                | track_id          | track_id, index            | 現在再生中のスロットを照会します                      |
| /live/track/get/send                              | track_id, send_id | track_id, send_id, value   | トラックのセンドを照会します                                  |
| /live/track/get/solo                              | track_id          | track_id, solo             | トラックのソロのオン/オフを照会します                           |
| /live/track/get/volume                            | track_id          | track_id, volume           | トラックのボリュームを照会します                                |

#### Setters

| Address                                  | Query params             | Response params | Description                       |
|:-----------------------------------------|:-------------------------|:----------------|:----------------------------------|
| /live/track/set/arm                      | track_id, armed          |                 | トラックのアーム状態を設定します (1=on, 0=off) |
| /live/track/set/color                    | track_id, color          |                 | トラックの色を設定します                   |
| /live/track/set/color_index              | track_id, color_index    |                 | トラックのカラーインデックスを設定します             |
| /live/track/set/current_monitoring_state | track_id, state          |                 | モニタリングのオン/オフを設定します             |
| /live/track/set/fold_state               | track_id, fold_state     |                 | グループの折りたたみを設定します (1=on, 0=off)    |
| /live/track/set/input_routing_channel    | track_id, channel        |                 | 入力ルーティングチャンネルを設定します         |
| /live/track/set/input_routing_type       | track_id, type           |                 | 入力ルーティングタイプを設定します            |
| /live/track/set/mute                     | track_id, mute           |                 | トラックのミュートを設定します (1=on, 0=off)      |
| /live/track/set/name                     | track_id, name           |                 | トラック名を設定します                    |
| /live/track/set/output_routing_channel   | track_id, channel        |                 | 出力ルーティングチャンネルを設定します        |
| /live/track/set/output_routing_type      | track_id, type           |                 | 出力ルーティングタイプを設定します           |
| /live/track/set/panning                  | track_id, panning        |                 | トラックのパンニングを設定します                 |
| /live/track/set/send                     | track_id, send_id, value |                 | トラックのセンドを設定します                    |
| /live/track/set/solo                     | track_id, solo           |                 | トラックのソロを設定します (1=on, 0=off)      |
| /live/track/set/volume                   | track_id, volume         |                 | トラックのボリュームを設定します                  |

### Track: Properties of multiple clips

| Address                                      | Query params | Response params             | Description                                      |
|:---------------------------------------------|:-------------|:----------------------------|:-------------------------------------------------|
| /live/track/get/clips/name                   | track_id     | track_id, [name, ....]      | トラック上のすべてのクリップ名を照会します                    |
| /live/track/get/clips/length                 | track_id     | track_id, [length, ...]     | トラック上のすべてのクリップ長を照会します                  |
| /live/track/get/clips/color                  | track_id     | track_id, [color, ...]      | トラック上のすべてのクリップ色を照会します                   |
| /live/track/get/arrangement_clips/name       | track_id     | track_id, [name, ....]      | トラック上のすべてのアレンジメントビュークリップ名を照会します   |
| /live/track/get/arrangement_clips/length     | track_id     | track_id, [length, ...]     | トラック上のすべてのアレンジメントビュークリップ長を照会します |
| /live/track/get/arrangement_clips/start_time | track_id     | track_id, [start_time, ...] | トラック上のすべてのアレンジメントビュークリップ時間を照会します   |

### Track: Properties of devices
| Address                            | Query params | Response params        | Description                              |
|:-----------------------------------|:-------------|:-----------------------|:-----------------------------------------|
| /live/track/get/num_devices        | track_id     | track_id, num_devices  | トラック上のデバイス数を照会します |
| /live/track/get/devices/name       | track_id     | track_id, [name, ...]  | トラック上のすべてのデバイス名を照会します          |
| /live/track/get/devices/type       | track_id     | track_id, [type, ...]  | トラック上のすべてのデバイスタイプを照会します         |
| /live/track/get/devices/class_name | track_id     | track_id, [class, ...] | トラック上のすべてのデバイスクラス名を照会します    |

デバイスタイプ/クラス名の詳細については、[Device API](#device-api)を参照してください。
 
</details>

---

## Clip Slot API

クリップスロットは、クリップのコンテナを表します。クリップの作成、削除、存在確認に使用されます。

<details>
<summary><b>ドキュメント</b>: Clip Slot API</summary>

| Address                             | Query params                                                   | Response params                          | Description                                     |
|:------------------------------------|:---------------------------------------------------------------|:-----------------------------------------|:------------------------------------------------|
| /live/clip_slot/fire                | track_index, clip_index                                        |                                          | 指定されたクリップスロットの再生/一時停止をファイアします      |
| /live/clip_slot/create_clip         | track_index, clip_index, length                                |                                          | スロットにクリップを作成します                       |
| /live/clip_slot/delete_clip         | track_index, clip_index                                        |                                          | スロット内のクリップを削除します                     |
| /live/clip_slot/get/has_clip        | track_index, clip_index                                        | track_index, clip_index, has_clip        | スロットにクリップがあるかどうかを照会します               |
| /live/clip_slot/get/has_stop_button | track_index, clip_index                                        | track_index, clip_index, has_stop_button | スロットにストップボタンがあるかどうかを照会します        |
| /live/clip_slot/set/has_stop_button | track_index, clip_index, has_stop_button                       |                                          | ストップボタンを追加または削除します (1=on, 0=off)         |
| /live/clip_slot/duplicate_clip_to   | track_index, clip_index, target_track_index, target_clip_index |                                          | クリップを空のターゲットクリップスロットに複製します |

</details>

---

## Clip API

オーディオまたはMIDIクリップを表します。クリップの開始/停止、ノート、名前、ゲイン、ピッチ、色、再生状態/位置などの照会/変更に使用できます。

<details>
<summary><b>ドキュメント</b>: Clip API</summary>

| Address                                  | Query params                                                        | Response params                                                                        | Description                                                                                                                                              |
|:-----------------------------------------|:--------------------------------------------------------------------|:---------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| /live/clip/fire                          | track_id, clip_id                                                   |                                                                                        | クリップの再生を開始します                                                                                                                                      |
| /live/clip/stop                          | track_id, clip_id                                                   |                                                                                        | クリップの再生を停止します                                                                                                                                       |
| /live/clip/duplicate_loop                | track_id, clip_id                                                   |                                                                                        | クリップのループを複製します                                                                                                                                     |
| /live/clip/get/notes                     | track_id, clip_id, [start_pitch, pitch_span, start_time, time_span] | track_id, clip_id, pitch, start_time, duration, velocity, mute, [pitch, start_time...] | 指定されたクリップ内のノートを照会します（開始ピッチ/時間と時間/ピッチ範囲を含めることもできます）。                                                            |
| /live/clip/add/notes                     | track_id, clip_id, pitch, start_time, duration, velocity, mute, ... |                                                                                        | クリップに新しいMIDIノートを追加します。pitchはMIDIノートインデックス、start_timeとdurationはfloat単位の拍、velocityはMIDIベロシティインデックス、muteはtrue/falseです |
| /live/clip/remove/notes                  | [start_pitch, pitch_span, start_time, time_span]                    |                                                                                        | ピッチと時間の範囲でクリップからノートを削除します。範囲が指定されていない場合、すべてのノートが削除されます。注：2023-11時点で順序が変更されました。   |
| /live/clip/get/color                     | track_id, clip_id                                                   | track_id, clip_id, color                                                               | クリップの色を取得します                                                                                                                                           |
| /live/clip/set/color                     | track_id, clip_id, color                                            |                                                                                        | クリップの色を設定します                                                                                                                                           |
| /live/clip/get/color_index               | track_id, clip_id                                                   | track_id, clip_id, color_index                                                               | クリップのカラーインデックスを取得します (0-69)                                                                                                                                           |
| /live/clip/set/color_index               | track_id, clip_id, color_index                                      |                                                                                        | クリップのカラーインデックスを設定します (0-69)                                                                                                                                          |
| /live/clip/get/name                      | track_id, clip_id                                                   | track_id, clip_id, name                                                                | クリップ名を取得します                                                                                                                                            |
| /live/clip/set/name                      | track_id, clip_id, name                                             |                                                                                        | クリップ名を設定します                                                                                                                                            |
| /live/clip/get/gain                      | track_id, clip_id                                                   | track_id, clip_id, gain                                                                | クリップゲインを取得します                                                                                                                                            |
| /live/clip/set/gain                      | track_id, clip_id, gain                                             |                                                                                        | クリップゲインを設定します                                                                                                                                            |
| /live/clip/get/length                    | track_id, clip_id                                                   | track_id, clip_id, length                                                              | クリップ長を取得します                                                                                                                                          |
| /live/clip/get/sample_length              | track_id, clip_id                                                   | track_id, clip_id, sample_length                                                           | クリップのサンプル長を取得します                                                                                                                                 |
| /live/clip/get/start_time              | track_id, clip_id                                                   | track_id, clip_id, start_time                                                           | クリップの開始時間を取得します                                                                                                                                 |
| /live/clip/get/pitch_coarse              | track_id, clip_id                                                   | track_id, clip_id, semitones                                                           | クリップの粗調整リピッチを取得します                                                                                                                                 |
| /live/clip/set/pitch_coarse              | track_id, clip_id, semitones                                        |                                                                                        | クリップの粗調整リピッチを設定します                                                                                                                                 |
| /live/clip/get/pitch_fine                | track_id, clip_id                                                   | track_id, clip_id, cents                                                               | クリップの微調整リピッチを取得します                                                                                                                                   |
| /live/clip/set/pitch_fine                | track_id, clip_id, cents                                            |                                                                                        | クリップの微調整リピッチを設定します                                                                                                                                   |
| /live/clip/get/file_path                 | track_id, clip_id                                                   | track_id, clip_id, file_path                                                           | クリップのファイルパスを取得します                                                                                                                                       |
| /live/clip/get/is_audio_clip             | track_id, clip_id                                                   | track_id, clip_id, is_audio_clip                                                       | クリップがオーディオかどうかを照会します                                                                                                                              |
| /live/clip/get/is_midi_clip              | track_id, clip_id                                                   | track_id, clip_id, is_midi_clip                                                        | クリップがMIDIかどうかを照会します                                                                                                                               |
| /live/clip/get/is_playing                | track_id, clip_id                                                   | track_id, clip_id, is_playing                                                          | クリップが再生中かどうかを照会します                                                                                                                            |
| /live/clip/get/is_overdubbing                | track_id, clip_id                                                   | track_id, clip_id, is_overdubbing                                                          | クリップがオーバーダブ中かどうかを照会します                                                                                                                            |
| /live/clip/get/is_recording              | track_id, clip_id                                                   | track_id, clip_id, is_recording                                                        | クリップが録音中かどうかを照会します                                                                                                                          |
| /live/clip/get/will_record_on_start                | track_id, clip_id                                                   | track_id, clip_id, will_record_on_start                                                          | クリップが開始時に録音するかどうかを照会します                                                                                                                            |
| /live/clip/get/playing_position          | track_id, clip_id                                                   | track_id, clip_id, playing_position                                                    | クリップの再生位置を取得します                                                                                                                              |
| /live/clip/start_listen/playing_position | track_id, clip_id                                                   |                                                                                        | クリップの再生位置のリッスンを開始します。応答は /live/clip/get/playing_position に送信され、引数は track_id, clip_id, playing_position です         |
| /live/clip/stop_listen/playing_position  | track_id, clip_id                                                   |                                                                                        | クリップの再生位置のリッスンを停止します。                                                                                                              |
| /live/clip/get/loop_start                | track_id, clip_id                                                   | track_id, clip_id, loop_start                                                          | クリップのループ開始を取得します                                                                                                                                    |
| /live/clip/set/loop_start                | track_id, clip_id, loop_start                                       |                                                                                        | クリップのループ開始を設定します                                                                                                                                    |
| /live/clip/get/loop_end                  | track_id, clip_id                                                   | track_id, clip_id, loop_end                                                            | クリップのループ終了を取得します                                                                                                                                      |
| /live/clip/set/loop_end                  | track_id, clip_id, loop_end                                         |                                                                                        | クリップのループ終了を設定します                                                                                                                                      |
| /live/clip/get/warping                   | track_id, clip_id                                                   | track_id, clip_id, warping                                                             | クリップのワープモードを取得します                                                                                                                                     |
| /live/clip/set/warping                   | track_id, clip_id, warping                                          |                                                                                        | クリップのワープモードを設定します                                                                                                                                     |
| /live/clip/get/launch_mode                   | track_id, clip_id                                                   | track_id, clip_id, launch_mode                                                             | クリップのローンチモードを取得します (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)                                                                                                                                    |
| /live/clip/set/launch_mode                   | track_id, clip_id, launch_mode                                          |                                                                                        | クリップのローンチモードを設定します (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)                                                                                                                                     |
| /live/clip/get/launch_quantization                   | track_id, clip_id                                                   | track_id, clip_id, launch_quantization                                                             | クリップのローンチクオンタイゼーション値を取得します (0=Global, 1=None, 2=8Bars, 3=4Bars, 4=2Bars, 5=1Bar, 6=1/2, 7=1/2T, 8=1/4, 9=1/4T, 10=1/8, 11=1/8T, 12=1/16, 13=1/16T, 14=1/32)                                                                                                                                    |
| /live/clip/set/launch_quantization                   | track_id, clip_id, launch_quantization                                          |                                                                                        | クリップのローンチクオンタイゼーション値を設定します (0=Global, 1=None, 2=8Bars, 3=4Bars, 4=2Bars, 5=1Bar, 6=1/2, 7=1/2T, 8=1/4, 9=1/4T, 10=1/8, 11=1/8T, 12=1/16, 13=1/16T, 14=1/32)                                                                                                                                     |
| /live/clip/get/ram_mode                   | track_id, clip_id                                                   | track_id, clip_id, ram_mode                                                             | クリップのRAMモードを取得します (0=False, 1=True)                                                                                                      |
| /live/clip/set/ram_mode                   | track_id, clip_id, ram_mode                                          |                                                                                        | クリップのRAMモードを設定します (0=False, 1=True)                                                                                                                                     |
| /live/clip/get/warp_mode                   | track_id, clip_id                                                   | track_id, clip_id, warp_mode                                                             | クリップのワープモードを取得します (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Invalid/Error, 6=Pro)                                                                                                     |
| /live/clip/set/warp_mode                   | track_id, clip_id, warp_mode                                          |                                                                                        | クリップのワープモードを設定します (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Invalid/Error, 6=Pro)                                                                                                                                    |
| /live/clip/get/has_groove                   | track_id, clip_id                                                   | track_id, clip_id, has_groove                                                             | クリップのグルーヴ状態を取得します (0=False, 1=True)
| /live/clip/get/legato                   | track_id, clip_id                                                   | track_id, clip_id, legato                                                             | クリップのレガート状態を取得します (0=False, 1=True)                                                                                                      |
| /live/clip/set/legato                   | track_id, clip_id, legato                                          |                                                                                        | クリップのレガート状態を設定します (0=False, 1=True)                                                                                                                                     |
| /live/clip/get/position                   | track_id, clip_id                                                   | track_id, clip_id, position                                                             | クリップの位置（LoopStart）を取得します                                                                                                     |
| /live/clip/set/position                   | track_id, clip_id, position                                          |                                                                                        | クリップの位置（LoopStart）を設定します                                                                                                                                     |
| /live/clip/get/muted                   | track_id, clip_id                                                   | track_id, clip_id, muted                                                             | クリップのミュート状態を取得します (0=False, 1=True)                                                                                                      |
| /live/clip/set/muted                   | track_id, clip_id, muted                                          |                                                                                        | クリップのミュート状態を設定します (0=False, 1=True)                                                                                                                                     |
| /live/clip/get/velocity_amount              | track_id, clip_id                                                   | track_id, clip_id, velocity_amount                                                       | クリップのベロシティ量を取得します (0.0-1.0 aka 0% to 100%)                                                                                                                                  |
| /live/clip/set/velocity_amount              | track_id, clip_id, velocity_amount                                     |                                                                                        | クリップのベロシティ量を設定します (0.0-1.0 aka 0% to 100%)                                                                                               |
| /live/clip/get/start_marker              | track_id, clip_id                                                   | track_id, clip_id, start_marker                                                        | クリップの開始マーカーを取得します                                                                                                                                  |
| /live/clip/set/start_marker              | track_id, clip_id, start_marker                                     |                                                                                        | クリップの開始マーカーを浮動小数点ビート単位で設定します                                                                                               |
| /live/clip/get/end_marker                | track_id, clip_id                                                   | track_id, clip_id, end_marker                                                          | クリップの終了マーカーを取得します                                                                                                                                    |
| /live/clip/set/end_marker                | track_id, clip_id, end_marker                                       |                                                                                        | クリップの終了マーカーを浮動小数点ビート単位で設定します                                                                                                 |

</details>

---

## Scene API

シーンを表し、クリップの列を同時にトリガーするために使用されます。シーンの名前、色、テンポ、拍子はすべて設定および照会できます。

<details>
<summary><b>ドキュメント</b>: Scene API</summary>

### Scene methods

| Address                         | Query params | Response params | Description             |
|:--------------------------------|:-------------|:----------------|:------------------------|
| /live/scene/fire                | scene_id     |                 | 指定されたシーンをトリガーします |
| /live/scene/fire_as_selected    | scene_id     |                 | シーンをトリガーし、次のシーンを選択します |
| /live/scene/fire_selected       |              |                 | 選択されているシーンをトリガーし、次のシーンを選択します |

### Scene properties

 - 任意のSceneプロパティの変更をリッスンするには、`/live/scene/start_listen/<property> <scene_index>` を呼び出します
 - 応答は `/live/scene/get/<property>` に送信され、パラメータは `<scene_index> <property_value>` です

#### Getters

| Address                      | Query params      | Response params            | Description                                       |
|:-----------------------------|:------------------|:---------------------------|:--------------------------------------------------|
| /live/scene/get/color        | scene_id          | scene_id, color            | シーンの色を照会します                      |
| /live/scene/get/color_index  | scene_id          | scene_id, color_index      | シーンのカラーインデックスを照会します                |
| /live/scene/get/is_empty        | scene_id          | scene_id, is_empty            | シーンが空かどうかを照会します                      |
| /live/scene/get/is_triggered        | scene_id          | scene_id, is_triggered            | シーンがトリガー状態にあるかどうかを照会します  |
| /live/scene/get/name         | scene_id          | scene_id, name             | シーン名を照会します                      |
| /live/scene/get/tempo        | scene_id          | scene_id, tempo            | シーンのテンポを照会します |
| /live/scene/get/tempo_enabled       | scene_id          | scene_id, tempo_enabled            | シーンのテンポが有効かどうかを照会します |
| /live/scene/get/time_signature_numerator        | scene_id          | scene_id, numerator            | シーンの拍子の分子を照会します  |
| /live/scene/get/time_signature_denominator        | scene_id          | scene_id, denominator            | シーンの拍子の分母を照会します |
| /live/scene/get/time_signature_enabled        | scene_id          | scene_id, enabled            | シーンの拍子が有効かどうかを照会します |

#### Setters

| Address                                        | Query params             | Response params | Description                                  |
|:-----------------------------------------------|:-------------------------|:----------------|:---------------------------------------------|
| /live/scene/set/name                           | scene_id, name           |                 | シーン名を設定します                               |
| /live/scene/set/color                          | scene_id, color          |                 | シーンの色を設定します                              |
| /live/scene/set/color_index                    | scene_id, color_index    |                 | シーンのカラーインデックスを設定します                        |
| /live/scene/set/tempo                          | scene_id, tempo          |                 | シーンのテンポを設定します                              |
| /live/scene/set/tempo_enabled                  | scene_id, tempo_enabled  |                 | シーンのテンポが有効かどうかを設定します           |
| /live/scene/set/time_signature_numerator       | scene_id, numerator      |                 | シーンの拍子の分子を設定します           |
| /live/scene/set/time_signature_denominator     | scene_id, denominator    |                 | シーンの拍子の分母を設定します         |
| /live/scene/set/time_signature_enabled         | scene_id, enabled        |                 | シーンの拍子が有効かどうかを設定します  |


</details>

---

## Device API

インストゥルメントまたはエフェクトを表します。

デバイスの指定（`device_id`）には、数値インデックス（0から開始）のほかに、デバイス名（例: `"Auto Filter"`）を使用できます。トラックの指定（`track_id`）については [Track API](#track-api) と同様の形式が使用可能です。

<details>
<summary><b>ドキュメント</b>: Device API</summary>

### Device properties

- パラメータプロパティの変更をリッスンするには、`/live/device/start_listen/parameter/value <track_index> <device index> <parameter_index>` を呼び出します

| Address                                  | Query params                             | Response params                          | Description                                                                             |
|:-----------------------------------------|:-----------------------------------------|:-----------------------------------------|:----------------------------------------------------------------------------------------|
| /live/device/get/name                    | track_id, device_id                      | track_id, device_id, name                | デバイス名を取得します                                                                         |
| /live/device/get/class_name              | track_id, device_id                      | track_id, device_id, class_name          | デバイスクラス名を取得します                                                                   |
| /live/device/get/type                    | track_id, device_id                      | track_id, device_id, type                | デバイスタイプを取得します                                                                         |
| /live/device/get/num_parameters          | track_id, device_id                      | track_id, device_id, num_parameters      | デバイスによって公開されているパラメータの数を取得します                                      |
| /live/device/get/parameters/name         | track_id, device_id                      | track_id, device_id, [name, ...]         | デバイスによって公開されているパラメータ名のリストを取得します                                   |
| /live/device/get/parameters/value        | track_id, device_id                      | track_id, device_id, [value, ...]        | デバイスパラメータ値を取得します                                                         |
| /live/device/get/parameters/min          | track_id, device_id                      | track_id, device_id, [value, ...]        | デバイスパラメータの最小値を取得します                                                 |
| /live/device/get/parameters/max          | track_id, device_id                      | track_id, device_id, [value, ...]        | デバイスパラメータの最大値を取得します                                                 |
| /live/device/get/parameters/is_quantized | track_id, device_id                      | track_id, device_id, [value, ...]        | is_quantized設定のリストを取得します（つまり、パラメータがint/boolである必要があるかどうか） |
| /live/device/set/parameters/value        | track_id, device_id, value, value ...    |                                          | デバイスパラメータ値を設定します                                                         |
| /live/device/get/parameter/value         | track_id, device_id, parameter_id        | track_id, device_id, parameter_id, value | デバイスパラメータ値を取得します                                                            |
| /live/device/get/parameter/value_string  | track_id, device_id, parameter_id        | track_id, device_id, parameter_id, value | デバイスパラメータ値を読み取り可能な文字列（例: 2500 Hz）として取得します                         |
| /live/device/set/parameter/value         | track_id, device_id, parameter_id, value |                                          | デバイスパラメータ値を設定します                                                            |

デバイスの場合:

- `name` は人間が読める名前です
- `type` は 1 = audio_effect, 2 = instrument, 4 = midi_effect
- `class_name` はLiveのインストゥルメント/エフェクト名です（例: Operator, Reverb）。外部プラグインやラックの場合、AuPluginDevice, PluginDevice, InstrumentGroupDevice... などになります。

</details>


---

## MidiMap API

MIDI CCとLiveパラメータ間の割り当てを作成するために使用できます。

<details>
<summary><b>ドキュメント</b>: MidiMap API</summary>

### MidiMap methods

| Address                | Query params | Response params | Description             |
|:-----------------------|:-------------|:----------------|:------------------------|
| /live/midimap/map_cc   | track_id, device_id, param_id, channel, cc     |  | チャンネル `channel` のコントロールチェンジ `cc` が指定されたパラメータを制御するように割り当てを作成します。 |
                                                |

他のオブジェクトタイプ（およびLiveの内部API）との一貫性を保つため、**チャンネルはゼロからインデックス付けされる**ことに注意してください。したがって、MIDIチャンネル1はインデックス `0` で照会する必要があります。

</details>

---

# ユーティリティ

フレームワークにはコマンドラインコンソールユーティリティ `run-console.py` が含まれており、AbletonOSCにOSCクエリを送信するための迅速かつ簡単な方法として使用できます。例:

```
(1653)(AbletonOSC)$ ./run-console.py
AbletonOSC command console
Usage: /live/osc/command [params]
>>> /live/song/set/tempo 123.0
>>> /live/song/get/tempo
(123.0,)
>>> /live/song/get/track_names
('1-MIDI', '2-MIDI', '3-Audio', '4-Audio')
```

# 謝辞

[LiveOSC](https://livecontrol.q3f.org/ableton-liveapi/liveosc/) （このライブラリの精神的な前身）を作成した [Stu Fisher](https://github.com/stufisher/) （および他の著者）に感謝します。[Julien Bayle](https://structure-void.com/ableton-live-midi-remote-scripts/#liveAPI)
および [NSUSpray](https://nsuspray.github.io/Live_API_Doc/) には、[Hanz Petrov](http://remotescripts.blogspot.com/p/support-files.html) によるオリジナルの作業に基づいたXML APIドキュメントを提供していただき感謝します。

コードの貢献とフィードバックについて、以下の方々に深く感謝します:
- Jörn Lengwenings ([Coupe70](https://github.com/Coupe70))
- Bill Moser ([billmoser](https://github.com/billmoser))
- [stevmills](https://github.com/stevmills)
- Marco Buongiorno Nardelli ([marcobn](https://github.com/marcobn)) and Colin Stokes
- Mark Marijnissen ([markmarijnissen](https://github.com/markmarijnissen))
- [capturcus](https://github.com/capturcus)
- Esa Ruoho a.k.a. Lackluster ([esaruoho](https://github.com/esaruoho))
