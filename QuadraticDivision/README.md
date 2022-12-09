最終更新：2022/12/09  
・readmeを整備しました  
更新予定  
・  

_____
# [LazyQuadraticDivision](https://github.com/titanium-22/Library/blob/main/QuadraticDivision/LazyQuadraticDivision.py)
区間の総積取得・区間への作用適用クエリをそれぞれ時間計算量 $\mathcal{O}(\sqrt{N})$ で処理できるデータ構造です。計算量が $\mathcal{O}(\sqrt{N})$ になった遅延セグ木ともみなせます。  
定数倍が軽いのでそこまで遅くはないはずです。  


### ```qd = LazyQuadraticDivision(n_or_a, op, mapping, composition, e)```
列 $\mathsf{a}$ から $\mathsf{LazyQuadraticDivision}$ を構築します。その他引数は遅延セグ木のアレです。時間計算量 $\mathcal{O}(N)$ です。  
$\mathsf{n}$ を $\mathsf{int}$ にすると、 $\mathsf{n}$ 個の $\mathsf{e}$ からなる配列で $\mathsf{LazyQuadraticDivision}$ を構築します。

### ```qd.apply(l, r, f)```
区間 $\mathsf{\left[l, r\right)}$ に $f$ を適用します。時間計算量 $\mathcal{O}(\sqrt{N})$ です。

### ```qd.all_apply(f)```
区間 $\mathsf{\left[0, N\right)}$ に $f$ を適用します。時間計算量 $\mathcal{O}(\sqrt{N})$ です。

### ```qd[k]```
$k$ 番目の値を返します。時間計算量 $\mathcal{O}(\sqrt{N})$ です。

### ```qd[k] = key```
$k$ 番目の値を $key$ に変更します。時間計算量 $\mathcal{O}(\sqrt{N})$ です。

### ```qd.prod(l, r)```
区間 $\mathsf{\left[l, r\right)}$ に $op$ を適用した総積を返します。時間計算量 $\mathcal{O}(\sqrt{N})$ です。

### ```qd.all_prod()```
区間 $\mathsf{\left[0, N\right)}$ に $op$ を適用した総積を返します。時間計算量 $\mathcal{O}(\sqrt{N})$ です。
