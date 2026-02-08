# 貢献

## テスト

ユニットテストをパスさせるための条件:

- Liveがデフォルトのオーディオ入力および出力デバイスで構成されていること。
- Liveが空のデフォルトセットで起動されていること。
- `Preferences > Record, Warp & Launch` で、`Count-In` が `None` に設定されていること（テストクリップの録音用）。

ユニットテストを実行するには、`pip3 install pytest` を実行し、Liveを起動して `AbletonOSC` ディレクトリに移動してから、以下を実行します。

```
pytest
```

## ライブリロード

AbletonOSCはハンドラーコードモジュールの動的リロードをサポートしているため、コードを変更するたびにLiveを再起動する必要はありません。

コードベースをリロードするには、OSCメッセージを `/live/api/reload` に送信してください。 

## ロギング

ロギングは、`self.logger` プロパティを介して、任意の `AbletonOSCHandler` クラスから実行できます。

AbletonOSCは、AbletonOSCディレクトリ内の `logs/abletonosc.log` に内部イベントを記録します。

## コンパイル時の問題のデバッグ

Liveの起動ログを表示するには：

```bash
LOG_DIR="$HOME/Library/Application Support/Ableton/Live Reports/Usage"
LOG_FILE=$(ls -atr "$LOG_DIR"/*.log | tail -1)
echo "Log path: $LOG_FILE"
tail -5000f "$LOG_FILE" | grep AbletonOSC
```
