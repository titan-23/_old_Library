def cartesian_tree(a: list) -> list:
  '''Get cartesian_tree. / O(N)'''
  par = [-1] * len(a)
  left = [-1] * len(a)
  right = [-1] * len(a)
  path = []
  for i, aa in enumerate(a):
    pre = -1
    while path and aa < a[path[-1]]:
      pre = path.pop()
    if pre != -1:
      par[pre] = i
    if path:
      par[i] = path[-1]
    path.append(i)
  for i, p in enumerate(par):
    if p == -1:
      continue
    if i < p:
      left[p] = i
    else:
      right[p] = i
  return par, left, right


