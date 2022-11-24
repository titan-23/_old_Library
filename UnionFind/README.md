最終更新：2022/11/24

- 型アノテーションをつけました。
- ```_find```を```root```に変更しました。
- ```compress_path```を消しました。

更新予定  
- 内部をdefaultdictで管理するバージョンも作りたいです。  

_____
# [UnionFind](https://github.com/titanium-22/Library/blob/main/UnionFind/UnionFind.py)
UnionFindです。素集合データ構造です。 
以下、α(N)をアッカーマン関数の逆関数とします(よく分かっていない)。  


### ```uf = UnionFind(n)```
n個の要素からなるUnionFindを構築します。時間計算量O(N)です。
- n: int, 0 < n
- 戻り値の型: None

### ```uf.root(x)```
要素xを含む集合の代表元を返します。
- x: int, 0 ≤ x < n
- 戻り値の型: int

### ```uf.unite(x, y)```
要素xを含む集合と要素yを含む集合を併合します。時間計算量O(α(N))です。
- x: int, 0 ≤ x < n
- y: int, 0 ≤ y < n
- 戻り値の型: None

### ```uf.same(x, y)```
要素xと要素yが同じ集合に属するならTrueを、そうでないならFalseを返します。時間計算量O(α(N))です。
- x: int, 0 ≤ x < n
- y: int, 0 ≤ y < n
- 戻り値の型: bool

### ```uf.size(x)```
要素xを含む集合の要素数を返します。時間計算量O(α(N))です。
- x: int, 0 ≤ x < n
- 戻り値の型: int

### ```uf.members(x)```
要素xを含む集合を返します。時間計算量O(size(x))です(！)。
- x: int, 0 ≤ x < n
- 戻り値の型: Set[int]

### ```uf.all_roots()```
全ての集合の代表元からなるリストを返します。時間計算量O(N)です。
- 戻り値の型: List[int]

### ```uf.group_count()```
ufの集合の総数を返します。時間計算量O(1)です。
- 戻り値の型: int

### ```uf.all_group_members()```
keyに代表元、valueにkeyを代表元とする集合のリストをもつdefaultdictを返します。時間計算量O(Nα(N))です。
- 戻り値の型: defaultdict[List[int]]

### ```uf.claer()```
集合を工場出荷状態に戻します。時間計算量O(N)です。
- 戻り値の型: None

### ```str(uf)```
よしなにします。時間計算量O(Nα(N))です。
- 戻り値の型: str
