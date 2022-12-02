最終更新: 2022/12/02  
・いろいろ変更しました。  

計算量は償却だったり最悪だったりします。詳しくは各READMEを読んでください。  
以下の木があります。  
・AVLTree  
・ScapegoatTree  
・SplayTree  


# 列を扱うBinaryTree #

### ```bt.merge(other)```
btにotherをマージします。mergeした後にotherを使うとマズイです。

### ```bt.split(k)```
btをkでsplitします。

### ```bt.prod(l, r)```
区間[l, r)の総積を取得します。l >= rのとき単位元を返します。

### ```bt.all_prod()```
区間[0, n)の総積を取得します。O(1)です。

### ```bt.insert(k, key)```
k番目にkeyを挿入します。

### ```bt.append(key) / appendleft(key)```
先頭/末尾にkeyを追加します。

### ```bt.pop(k=-1) / .popleft()```
末尾(k番目)/先頭の値を削除し、その値を返します。

### ```bt[k]```
k番目の値を返します。

### ```bt[k] = key```
k番目の値をkeyに更新します。

### ```bt.copy()```
copyします。O(N)です。

### ```bt.clear()```
clearします。O(1)です。

### ```bt.to_l()```
keyからなるリストを返します。O(1)です。

# 遅延評価できる木
列を扱うBinaryTreeに咥えて以下の操作ができます。

### ```bt.reverse(l, r)```
区間[l, r)を反転します。reverseメソッドを使うなら、opには可換性が求められます。

### ```bt.apply(l, r, f)```
区間[l, r)にfを適用します。

### ```bt.all_apply(f)```
区間[0, n)にfを適用します。O(1)です。

# 集合としてのBinarySearchTree

### ```x in bst / x not in bst```
存在判定です。

### ```bst[k]```
昇順k番目の値を返します。

### ```bst.add(key)```
keyが存在しないならkeyを追加し、Trueを返します。keyが存在するなら何も追加せず、Falseを返します。

### ```bst.discard(key)```
keyが存在するならkeyを削除し、Trueを返します。keyが存在しないなら何もせず、Falseを返します。

### ```bst.le(key) / .lt(key) / .ge(key) / gt(key)```
key(以下の/より小さい/以上の/より大きい)値で(最大/最大/最小/最小)の値を返します。存在しなければNoneを返します。

### ```bst.index(key) / .index_right(key)```
key(より小さい/以下の)要素の数を返します。

### ```bst.pop(k=-1) / .popleft()```
(最大(昇順k番目)/最小)の値を削除し、その値を返します。

### ```bst.clear()```
clearします。O(1)です。

### ```bst.to_l()```
keyを昇順に並べたリストを返します。O(N)です。

# MultiSet
Setに加えて、以下の操作ができます。  
valの値に関わらず、O(logN)で動作します。

### ```bst.add(key, val=1)```
val個のkeyを追加します。

### ```bst.discard(key, val=1)```
keyをval個削除します。valがkeyの数より大きいときは、keyを全て削除します。  
keyが無いときFalseを、そうでないときTrueを返します。

### ```bst.dicard_all(key)```
keyを全て削除します。

### ```bst.count(key)```
含まれるkeyの数を返します。

### ```bst.index_keys(key) / index_right_keys(key)```
key(より小さい/以下の)要素の種類数を返します。

### ```bst.to_l_items()```
keyで昇順に並べたリストを返します。各要素は(key, st.count(key))です。

### ```bst.keys() / values() / items()```
よしなに動きます。

### ```bst.get_elm(k)```
要素の重複を除いたときの、昇順k番目のkeyを返します。

### ```bst.len_elm()```
stの要素の種類数を返します。

### ```bst.show()```
よしなにprintします。
