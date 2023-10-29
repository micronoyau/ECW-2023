with open("unknown.txt", "r") as f:
    s = dict()
    for l in f:
        for token in l.strip().split():
            if not token in s:
                s[token] = 0
            s[token] += 1
    print(sorted(list(s.keys())))
    print(len(s))
    print(s)

