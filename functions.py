def shrinktitle(name):
    cnt = 0
    now = 0
    for i in name:
      now += 1
      if i == '/':
         cnt = now
    b = name[cnt:now]
    return b
