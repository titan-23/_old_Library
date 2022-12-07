# https://github.com/titanium-22/Library/blob/main/Graph/warshall_floyd.py


from typing import List
inf = float('inf')

'''Return min cost s.t. cost[a][b] -> a to b. / O(|V|^3)'''
def warshall_floyd(G: List[List[int]]) -> List[List[int]]:
  v = len(G)
  cost = [[inf]*v for _ in range(v)]
  for x in range(v):
    cost[x][x] = 0
    for xx, cc in G[x]:
      cost[x][xx] = cc
  for k in range(v):
    for i in range(v):
      for j in range(v):
        if cost[i][j] > cost[i][k] + cost[k][j]:
          cost[i][j] = cost[i][k] + cost[k][j]
  return cost
  '''
  for i in range(v):
    if cost[i][i] < 0:
      return 'NEGATIVE CYCLE'
  '''
