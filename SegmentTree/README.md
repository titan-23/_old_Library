最終更新：2022/11/25

- 型アノテーションをつけました。

更新予定  


_____
# [SegmentTree](https://github.com/titanium-22/Library/blob/main/SegmentTree/SegmentTree.py)
SegmentTreeです。  
ACLのsegtreeを大々的に参考にしてます。

### ```seg = SegmentTree(n_or_a, op, e)```
第1引数n_or_aがintのとき、eを初期値として長さnのSegmentTreeを構築します。  
第1引数n_or_aがIterableのとき、aからSegmentTreeを構築します。  
いずれも時間計算量O(N)です。
- n_or_a: Union[int, Iterable]
- 戻り値の型: None

