# SplayTree

## SplayTree
列を扱えるSplayTreeです。以下の操作が償却計算量？O(logN)でできます。よしなに。
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

## SplayTreeSet
setとしてのSplayTreeです。未完成です。よしなに。
