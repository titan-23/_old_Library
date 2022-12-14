最終更新: 2022/12/14  
・いろいろ更新しました。  

_____
# [IntervalHeap](https://github.com/titanium-22/Library/blob/main/Heap/IntervalHeap.py)

IntervalHeapです。  
値の追加/最小値取得(pop)/最大値取得(pop) などができます。

### ```hq = IntervalHeap(a: Iterable[T]=[])```
Iterable aからIntervalHeapを構築します。 $\mathcal{O}(N)$ です。

### ```hq.add(key: T) -> None```
keyを1つ追加します。 $\mathcal{O}(logN)$ です。

### ```hq.pop_min() -> T```
hqの最小の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```hq.pop_max() -> T```
hqの最大の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```hq.get_min() -> T```
hqの最小の値を返します。 $\mathcal{O}(1)$ です。

### ```hq.get_max() -> T```
hqの最大の値を返します。 $\mathcal{O}(1)$ です。

### ```len(hq) / bool(hq) / str(hq)```
よしなに動きます。

_____
# [MinMaxSet](https://github.com/titanium-22/Library/blob/main/Heap/MinMaxSet.py)

内部でsetを持ち、データを管理します。  
値の追加/削除/存在判定/最小値取得(pop)/最大値取得(pop) などができます。  
計算量は償却だったりします。

### ```st = MinMaxSet(a: Iterable[T]=[])```
Iterable aからMinMaxSetを構築します。 $\mathcal{O}(N)$ です。

### ```st.add(key: T) -> None```
keyが既に存在していれば、何もしません。そうでなければkeyを1つ追加します。
$\mathcal{O}(logN)$ です。

### ```st.discard(key: T) -> bool```
keyが存在すれば、削除してTrueを返します。そうでなければ、何も削除せずにFalseを返します。 $\mathcal{O}(logN)$ です。

### ```st.popleft() -> T```
stの最小の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```st.pop() -> T```
stの最大の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```st.get_min() -> T```
stの最小の値を返します。 $\mathcal{O}(1)$ です。

### ```st.get_max() -> T```
stの最大の値を返します。 $\mathcal{O}(1)$ です。

### ```st.to_l() -> List[T]```
keyからなるListを返します。 $\mathcal{O}(NlogN)$ です。

### ```key in st / len(st) / bool(st) / str(st)```
よしなに動きます。


_____
# [MinMaxMultiSet](https://github.com/titanium-22/Library/blob/main/Heap/MinMaxMultiSet.py)

内部でCounterを持ち、データを管理します。  
値の追加/削除/存在判定/最小値取得(pop)/最大値取得(pop) などができます。  
計算量は償却だったりします。

### ```mst = MinMaxMultiSet(a: Iterable[T]=[])```
Iterable aからMinMaxMultiSetを構築します。 $\mathcal{O}(N)$ です。

### ```mst.add(key: T, val: int=1) -> None```
keyをval個追加します。$\mathcal{O}(logN)$ です。

### ```mst.discard(key: T, val: int=1) -> bool```
keyが存在しなければ何も削除せずにFalseを返します。
そうでなければ、keyをmin(mst.count(key), val)個削除し、Trueを返します。 $\mathcal{O}(logN)$ です。

### ```mst.popleft() -> T```
mstの最小の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```mst.pop() -> T```
mstの最大の値を削除し返します。 $\mathcal{O}(logN)$ です。

### ```mst.get_min() -> T```
mstの最小の値を返します。 $\mathcal{O}(1)$ です。

### ```mst.get_max() -> T```
mstの最大の値を返します。 $\mathcal{O}(1)$ です。

### ```mst.count(key: T) -> int```
keyの個数を返します。 $\mathcal{O}(1)$ です。

### ```mst.to_l() -> Limst[T]```
keyからなるListを返します。 $\mathcal{O}(NlogN)$ です。

### ```key in mst / len(mst) / bool(mst) / str(mst)```
よしなに動きます。
