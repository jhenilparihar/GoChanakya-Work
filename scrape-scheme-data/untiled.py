def func1():
    x =20
    def fun2():
        global x
        x = 25
    print("s",x)
    fun2()
    print("d",x)
func1()
print("f",x)