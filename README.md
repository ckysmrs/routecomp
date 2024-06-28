# routecomp

グラフデータからオイラー回路やオイラールートを生成するプログラムです。
鉄道路線の乗りつぶし等に利用してください。

## 実行方法
### オイラー回路の生成
```
python gen_eulerian_graph.py データファイル
```
データファイルから総コスト最小のオイラー回路を出力します。データファイルは複数指定できます。-lオプションによりデータファイルのリストを指定できます。

`python gen_eulerian_graph.py -h`でヘルプを表示します。

### オイラールートの生成
```
python gen_eulerian_route.py データファイル
```
データファイルからオイラールートの一例を出力します。

`python gen_eulerian_route.py -h`でヘルプを表示します。

回路の生成とルートの生成をパイプライン実行できます。
```
python gen_eulerian_graph.py データファイル | python gen_eulerian_route.py
```
PowerShellで文字化けするときはこちら。  
[Powershell上で、パイプで渡すと文字化けする。 #PowerShell - Qiita](https://qiita.com/EmEpsilon/items/7e8f72b9c58576b4c5a5)

### オイラー回路とオイラールートの生成
```
python routecomp.py データファイル
```
データファイルから総コスト最小のオイラー回路を生成し、オイラールートの一例を整形して出力します。データファイルは複数指定できます。-lオプションによりデータファイルのリストを指定できます。

`python routecomp.py -h`でヘルプを表示します。

## データファイルのフォーマット
辺の始点、終点、コストを空白区切りで記述します。

鉄道での乗り換え等、同じと見なすノードはコストにtransferと記述します。

\#以降はコメントになります。

## 用語集
Wikiに[用語集](https://github.com/ckysmrs/routecomp/wiki/%E7%94%A8%E8%AA%9E%E9%9B%86)があります。

## ライセンス
本リポジトリのソースコードは[MITライセンス](http://www.opensource.org/licenses/MIT)です。

binary_heap.py、blossom_matching.py、e_blossom_type.py、matching_graph.pyは https://github.com/dilsonpereira/Minimum-Cost-Perfect-Matching (Copyright (c) 2018 dilsonpereira)を元にしています。

binary_heap.py, blossom_matching.py, e_blossom_type.py and matching_graph.py are based on https://github.com/dilsonpereira/Minimum-Cost-Perfect-Matching (Copyright (c) 2018 dilsonpereira).