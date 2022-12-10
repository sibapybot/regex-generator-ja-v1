# regex-generator-ja-v1.0.0

このライブラリは複数のテキストを渡すことで自動でパターンを検出し出力してくれるコードです。<br>
<br>
<br>
パターンを検出するテキストを多く入れ過ぎると処理に時間がかかるときがあります。<br>
<br>
また、`run`関数を実行すると正規表現が返されますが、MeCabの使用上スペースなどは除去されます。<br>
よって、同じパターンかどうか確認するときは <ins>必ず`is_true`関数を使用</ins> してください。<br>

使い方<br>
```py
from RegexGeneratorJa.generator import run,is_true

#パターンを検出するためのテキストは3つぐらいがオススメ
texts = ["a testだあああああああ！！！asfdaa testだあああああああ！！！ ","a testだあああああああ！！！barbhah ethbe  testだあああああああ！！！","a testだあああああああ！！！agfnl testだあああああああ！！！"]
#パターンを取得する
pattern = run(texts)

#同じパターンかチェックする
check = is_true("a testだあああああああ！！！asfdaasdaedea testだあああああああ！！！ ",pattern=pattern)
print(check)

```
