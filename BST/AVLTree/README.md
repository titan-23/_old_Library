最終更新：2022/12/03  
・いろいろ更新しました。

※計算量を明示していないものはすべてO(logN)の計算量です。

_____
# [LazyAVLTree](https://github.com/titanium-22/Library/blob/main/BST/AVLTree/LazyAVLTree.py)
遅延伝播反転可能平衡二分木です。アホの定数倍をしています(定数倍が大きい方向にアホです)。  
※恒等写像はいりません(内部で恒等写像をNoneとして場合分けしています)。

### ```avl = LazyAVLTree(a, op, mapping, composition)```
列aからLazyAVLTreeを構築します。その他引数は遅延セグ木のアレです。時間計算量O(N)です。  
op, mapping, compositionは省略可能です。

### ```avl.merge(other)```
stにotherをmergeできます。

### ```avl.split(indx)```
x, y = avl.split(indx)で、indx番目で左右に分けたAVLTreeをつくりx, yに代入できます。avlは破壊されます。(xの長さがindx。)

### ```avl.insert(indx, key)```
indxにkeyをinsesrtできます。

### ```avl.pop(indx)```
indx番目を削除しその値を返します。

### ```avl[indx]```
indx番目を取得できます。

### ```avl.prod(l, r)```
区間[l, r)にopを適用した結果を返します。単位元を取得していないので、l < rが必要です。

### ```avl.reverse(l, r)```
区間[l, r)を反転します。reverse()メソッドを一度でも使用するならopには可換性が求められます(可換性がない場合、嘘の動作をします)。

### ```avl.apply(l, r, f)```
区間[l, r)にfを適用します。

### ```avl.to_l()```
Nodeのkeyからなるリストを返します。計算量はO(N)です。
