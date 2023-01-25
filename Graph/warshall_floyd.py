from typing import List
inf = float('inf')

'''Return min dist s.t. dist[a][b] -> a to b. / O(|n|^3)'''
def warshall_floyd(G: List[List[int]]) -> List[List[int]]:
  n = len(G)
  # dist = [dijkstra(G, s) for s in range(n)]
  dist = [[inf]*n for _ in range(n)]
  for v in range(n):
    dist[v][v] = 0
    for x, c in G[v]:
      dist[x][x] = c
  for k in range(v):
    for i in range(v):
      if dist[i][k] == inf: continue
      for j in range(v):
        if dist[i][j] > dist[i][k] + dist[k][j]:
          dist[i][j] = dist[i][k] + dist[k][j]
        # elif dist[i][j] == dist[i][k] + dist[k][j]:
        #   dist[i][j] = dist[i][k] + dist[k][j]
  '''
  for i in range(v):
    if dist[i][i] < 0:
      return 'NEGATIVE CYCLE'
  '''
  return dist
