def task1_2(array):
    left = 0
    right = len(array) - 1
    while True:
        ind = (left + right) // 2
        if left == right and array[ind] == 1:
            break
        if array[ind] == 0:
            if ind == 0 or array[ind - 1] == 1:
                return ind
            else:
                right = ind - 1
        else:
            left = ind + 1
    return -1

if __name__ == "__main__":
    array = [int(i) for i in input("Введите строку вида \"111000\": ")]
    print(task1_2(array))