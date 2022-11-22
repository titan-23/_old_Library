最終更新：2022/11/22

・アップロードしました。  
・定数倍は劣りますが、内部をdefaultdictで管理するバージョンも作りたいです。

_____
# [UnionFind](https://github.com/titanium-22/Library/blob/main/UnionFind/UnionFind.py)
UnionFindです。素集合データ構造です。  
以下、α(N)をアッカーマン関数の逆関数とします(よく分かっていない)。

### ```uf = UnionFind(n)```
要素数nからなるUnionFindを構築します。時間計算量O(N)です。

### ```uf.unite(x, y)```
要素xを含む集合と要素yを含む集合を併合します。時間計算量O(α(N))です。

### ```uf.same(x, y)```
要素xと要素yが同じ集合に属するならTrueを、そうでないならFalseを返します。時間計算量O(α(N))です。

### ```uf.size(x)```
要素xを含む集合の要素数を返します。時間計算量O(α(N))です。

### ```uf.members(x)```
要素xを含む集合の要素をsetで返します。時間計算量O(size(x))です(！)。

### ```uf.roots(x)```
要素xを含む集合の代表元を返します。時間計算量O(α(N))です。

### ```uf.group_count()```
ufの集合の総数を返します。時間計算量O(1)です。

### ```uf.all_group_members()```
keyに代表元、valueにkeyを代表元とする集合のリストをもつdefaultdictを返します。時間計算量O(Nα(N))です。

### ```uf.compress_path()```
パス圧縮をします。すなわち、要素数が2以上の集合の任意の要素の親が代表元になります。時間計算量O(Nα(N))です。

### ```uf.claer()```
集合を工場出荷状態に戻します。時間計算量O(N))です。

### ```str(uf)```
よしなにします。時間計算量O(Nα(N))です。

