#Картозия,домашнее здание №1, задание 1
def fibonacci(n):
    memo = {}
    a,b = 1,1
    if n not in memo:
        for i in range(n-1):
            a,b = b, a+b
            memo[n] = a
    return memo[n]

#print(fibonacci(10))


