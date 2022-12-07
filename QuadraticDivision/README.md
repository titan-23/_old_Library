最終更新：2022/11/22

・バグがあるかもしれません。もう少し整備するつもりです。

_____
# [LazyQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/LazyQuadraticDivision.py)
計算量がO(√N)になった遅延セグ木です。定数倍が軽いのでそこまで遅くはないはずです。  


### ```qd = LazyQuadraticDivision(n_or_a, op, mapping, composition, e)```
列aからLazyQuadraticDivisionを構築します。その他引数は遅延セグ木のアレです。時間計算量O(N)です。  
nをintにすると、n個のeからなる配列でLazyQuadraticDivisionを構築します。

### ```qd.apply(l, r, f)```
区間[l, r)にfを適用します。時間計算量O(√N)です。

### ```qd.all_apply(f)```
区間[0, N)にfを適用します。時間計算量O(√N)です。

### ```qd[indx]```
indx番目を取得できます。時間計算量O(√N)です。

### ```qd[indx] = key```
setitemできます。時間計算量O(√N)です。

### ```qd.prod(l, r)```
区間[l, r)にopを適用した結果を返します。時間計算量O(√N)です。

### ```qd.all_prod()```
区間[0, N)にopを適用した結果を返します。時間計算量O(√N)です。

