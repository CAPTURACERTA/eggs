
def mmmm():
    m = []
    for i in range(6):
        l = []
        for j in range(5):
            l.append(f"B56_{i}{j} = 0")
        m.append(l)

    print(m)

m = [
    [1,2,3],
    [4,5,6],
    [7,8,9],
    [10,11,12]
]
print(m[::-1])