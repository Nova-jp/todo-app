def shrinktitle(name):
    cnt = 0
    now = 0
    for i in name:
        if i == '/':
            cnt = now
        now += 1
    if cnt != 0:
      cnt+=1
    b = name[cnt:now]
    return b
