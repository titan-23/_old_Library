最終更新：2022/11/22

_____
# [LazyQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/LazyQuadraticDivisionv.py)
遅延評価ができます。内部で平方分割を利用しています。  
※恒等写像はいりません(内部で恒等写像をNoneとして場合分けしています)。

### ```qd = LazyQuadraticDivision(n_or_a, op, mapping, composition, e)```
列aからLazyQuadraticDivisionを構築します。その他引数は遅延セグ木のアレです。時間計算量O(N)です。  
n_or_aをintにすると、n個のeからなる配列からLazyQuadraticDivisionを構築します。

### ```qd.apply(l, r, f)```
区間[l, r)にfを適用します。時間計算量O(√N)です。

### ```qd.all_apply(f)```
区間[0, N)にfを適用します。時間計算量O(√N)です。

### ```qd[indx]```
indx番目を取得できます。時間計算量O(√N)です。

### ```st[indx] = key```
setitemできます。時間計算量O(√N)です。

### ```st.prod(l, r)```
区間[l, r)にopを適用した結果を返します。時間計算量O(√N)です。

### ```qd.all_prod()```
区間[0, n)にopを適用した結果を返します。時間計算量O(√N)です。

