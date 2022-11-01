# SplayTree

_____
## [SplayTree](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTree.py)
列を扱えるSplayTreeです。以下の操作が償却計算量？O(logN)でできます。生後3日目くらいの幼木です。よしなに。
### st = SplayTree(a, op=myfunc)
列aをSplayTreeにします。
### merge
st.merge(other)で、stにotherをmergeできます。
### split
x, y = st.split(indx)で、indx番目で左右に分けたSplayTreeをつくりx, yに代入できます。indx番目がどっちに行くかくは忘れました。
### insert
st.insert(indx, key)で、indxにkeyをinsesrtできます。
### pop
st.pop(indx)で、indx番目を削除しその値を返します。
### __getitem__
左からk番目を取得できます。
### __setitem__
setitemできます。
### prod
セグ木的なアレです。

_____
## [SplayTreeSet](https://github.com/titanium-22/Library/blob/main/BST/SplayTree/SplayTreeSet.py)
setとしてのSplayTreeです。未完成です。よしなに。
