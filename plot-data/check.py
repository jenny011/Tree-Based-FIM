from os import path

def check(path1, path2):
    f1 = open(path1, 'r')
    f2 = open(path2, 'r')
    n = 1
    while True:
        r1 = f1.read(n)
        r2 = f2.read(n)
        if r1 != r2:
            return False
    f1.close()
    f2.close()
    return True


if __name__ == '__main__':
    experiment1 = "fpGrowth"
    experiment2 = "freno"
    
    filepath1 = path.join(".", experiment1, "retail")
    filepath2 = path.join(".", experiment2, "retail")
    
    data = {}
    result = 'result01.txt'
    resultpath1 = path.join(filepath1, result)
    resultpath2 = path.join(filepath2, result)
    print(check(resultpath1, resultpath2))

    # experiment3 = "Freno"
    # filepath3 = path.join(".", experiment3, "retail")