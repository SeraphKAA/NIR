import matplotlib.pyplot as plt
from tkinter.messagebox import showerror
from tkinter import *
import numpy as np
import sympy as sp
from scipy.integrate import quad
import datetime

                                                    # Вариант 13
                                        # λ = 8, [a, b] = [2, 3], K(X,S) = 4(x^2+s^2), f(x) = 9x-7
                                        # ∫ - интеграл






def Graph(res, g_fun, ab):
    x = np.linspace(ab[0] - 3, ab[1] + 3, 500)  
    y = eval(str(res))

    g_array = np.array([g_fun(i) for i in x])

    plt.plot(x, y, label = "Метод конечных сумм")
    plt.plot(x, g_array, label = "Точное решение")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'График функции y= {res} и точное решение')
    plt.grid(True)
    plt.legend()
    plt.show()



def K_flag(flag, K_xs, xx, ss):
    K = lambda x, s: eval(K_xs)
    if flag:
        if isinstance(xx, int) or isinstance(xx, float):
            if xx >= ss:
                return K(xx, ss)
            else:
                return 0
    else:
        return K(xx, ss)



def open_error(): 
    showerror(title="Ошибка", message="Что-то пошло не так")



def Start():

    window = Tk()

    window.geometry('300x200')
    window.title("Метод конечных сумм")
                                            # λ = 8, [a, b] = [2, 3], K(X,S) = 4(x^2+s^2), f(x) = 9x-7


#---------------

    lbl = Label(window, text = "K(x,s) = ", font = "Arial 14 bold")     # K(x,s)
    lbl.place(relx = 0.16, rely = 0.1, anchor = CENTER)

    K_xs_ent = Entry(window, width = 8, font = "Arial 14")         
    K_xs_ent.place(relx = 0.46, rely = 0.1, anchor = CENTER)

#---------------


#---------------

    lb2 = Label(window, text = "f(x) = ", font = "Arial 14 bold")     # f(x)
    lb2.place(relx = 0.16, rely = 0.3, anchor = CENTER)

    func_X_ent = Entry(window, width = 8, font = "Arial 14")         
    func_X_ent.place(relx = 0.46, rely = 0.3, anchor = CENTER)

#---------------


#---------------

    lb3 = Label(window, text = "[a, b] = ", font = "Arial 14 bold")     # ГРАНИЦЫ ИНТЕГРАЛА
    lb3.place(relx = 0.16, rely = 0.5, anchor = CENTER)

    ab_ent = Entry(window, width = 3, font = "Arial 14")         
    ab_ent.place(relx = 0.36, rely = 0.5, anchor = CENTER)

#---------------


#---------------

    lb4 = Label(window, text = "λ = ", font = "Arial 14 bold")     # ЛЯМБДА
    lb4.place(relx = 0.16, rely = 0.7, anchor = CENTER)

    lyamda_ent = Entry(window, width = 3, font = "Arial 14")         
    lyamda_ent.place(relx = 0.36, rely = 0.7, anchor = CENTER)

#---------------




    def clicked():
        try:

            K_xs, func_X, ab, lyamda = K_xs_ent.get(), func_X_ent.get(), ab_ent.get().split(", "), int(lyamda_ent.get())
            if len(ab) != 2:
                raise(IndexError)

            x, s = np.linspace(-5, 5, 100), np.linspace(-5, 5, 100)
            eval(K_xs)
            eval(func_X)
            # K_xs, func_X, ab, lyamda = "4*(x**2 + s**2)", "9*x - 7", ["2", "3"], 8
            # K_xs, func_X, ab, lyamda = "6*(x**2 + s**2)", "4*x + 3", ["-1", "0"], 2
            # K_xs, func_X, ab, lyamda = "4*x**2 + s", "4*x + 1", ["0", "x"], 12

        except:
            showerror(title="Ошибка", message="Введите корректные значения")
            return
        
        n = 2
        flag = False    # if True - Вольтерра
        flag1 = True    # Метод трапеций(False) или симпсона(True)




        if ab[1].isdigit():
            for i, el in enumerate(ab): ab[i] = int(el)
        else:
            ab[0] = int(ab[0])
            ab[1] = ab[0] + 1
            flag = True

        
        # Вылавливание ошибок !!!

        if(ab[0] >= ab[1]):
            showerror(title="Ошибка", message="Значение верхнего предела меньше или равно значению нижнего предела")
            return
        
        if("x" in K_xs and "s" in K_xs):    pass
        else:
            showerror(title="Ошибка", message="Отсутствует x или s переменные в ядре")
            return

        if("x" not in func_X):
            showerror(title="Ошибка", message="Отсутсвует x переменная в функции f(x)")
            return



        # Ядро интегрального оператора
        K = lambda x, s: eval(K_xs) # "4*(x**2) + s"
        # Свободная функция
        f = lambda x: eval(func_X) # "4*x + 1"

        a, b = ab[0], ab[1]
        h = (b - a) / n

        A = np.zeros((n + 1, n + 1))
        bb = np.zeros(n + 1)
        # ss = [a, h, b]
        
        
        Oobshiy_vid_yrav = "y(x) - λ * ∫(a, b)K(x,s)φ(s)ds = f(x)"
        chastniy_vid_yrav = "y(x) - {0} * ∫({1}, {2}){3}y(s)ds = {4}".format(str(lyamda), str(ab[0]), str(ab[1]), K_xs, func_X)

        print("Общий вид интегрального уравнения")
        print(Oobshiy_vid_yrav)
        print("\nЧастный вид интегрального уравнения")
        print(chastniy_vid_yrav)


        # temp = (b-a)/6

        if flag1:
            mnozh = -lyamda * (b-a)/6
        else:
            mnozh = -lyamda * (b-a)/4

        mnozh = round(mnozh, ndigits = 4)
        # print(mnozh)
        # print(mnozh, lyamda, b, a, temp, lyamda*temp, "mnozhitel\'")

        for i in range(n+1):
            x = a + i * h   # левый край + шаг и тд
            
            for j in range(n+1):
                if i == j:
                    A[i, j] += 1
                match j:
                    case 0:
                        A[i, j] += (round(mnozh * K_flag(flag, K_xs, x, a), ndigits = 4)) # K(x, a)
                        # print(mnozh, K_flag(flag, K_xs, x, a))
                        # print(mnozh * K_flag(flag, K_xs, x, a))
                        # print("||", K_flag(flag, K_xs, x, a), K(x, a))
                    case 1:
                        if flag1:
                            A[i, j] += (round(mnozh * 4 * K_flag(flag, K_xs, x, a+h), ndigits = 4)) # K(x, a + h)
                        else:
                            A[i, j] += (round(mnozh * 2 * K_flag(flag, K_xs, x, a+h), ndigits = 4)) # K(x, a + h)
                        # print("||", K_flag(flag, K_xs, x, a + h), K(x, a + h))
                    case 2:
                        A[i, j] += (round(mnozh * K_flag(flag, K_xs, x, b), ndigits = 4)) # K(x, b)
                        # print("||", K_flag(flag, K_xs, x, b), K(x, b))
            bb[i] = f(x)

        for i in range(len(A)):
            if A[i][i] < 0:
                bb[i] *= -1
                for j in range(len(A[i])):
                    A[i][j] *= -1  # Инвертируем знак элемента по главной диагонали, чтобы было > 0

        print("\nМатрица коэффицентов системы уравнений и его вектор свободных членов")

        tes = []
        for i, item in enumerate(A):
            tes.append([])
            for j, item2 in enumerate(item):
                tes[i].append(item2)
            tes[i].append(bb[i])
            print(tes[i])

        test = sp.Matrix(tes)       # матрица коэф
        aaaa = sp.linsolve(test)
        aaaa = list(aaaa)           # решение для yi

        print("\nКорни системы уравнений")
        for i in range(n + 1):
            print(f"y{i} = {aaaa[0][i]:.4f}", end = "  ")

        
        if mnozh < 0: mnozh *= -1

        xx = sp.Symbol("x")
        if flag1:
            res_str = func_X + " + " + f"{mnozh:.4f}" + " * ((" + str(K(xx, a)) + f")*{aaaa[0][0]:.4f} + 4*({K(xx, a + h)})*{aaaa[0][1]:.4f} + ({K(xx, b)}) * {aaaa[0][2]:.4f})"        # пурга
        else:
            res_str = func_X + " + " + f"{mnozh:.4f}" + " * ((" + str(K(xx, a)) + f")*{aaaa[0][0]:.4f} + 2*({K(xx, a + h)})*{aaaa[0][1]:.4f} + ({K(xx, b)}) * {aaaa[0][2]:.4f})"        # пурга
        # res_str = func_X + " + " + f"{mnozh:.4f}" + " * ((" + str(K_flag(flag, K_xs, xx, a)) + f")*{aaaa[0][0]:.4f} + 4*({K_flag(flag, K_xs, xx, a + h)})*{aaaa[0][1]:.4f} + ({K_flag(flag, K_xs, xx, b)}) * {aaaa[0][2]:.4f})"        # пурга
        expr = sp.sympify(res_str)
        # Упрощаем выражение
        simplified_expression = sp.simplify(expr)


        print("\n--------res---------")
        print(res_str)
        print(f"Упрощенное выражение: {simplified_expression}")



        x, s = sp.symbols('x s')
        y_x = simplified_expression
        # print('y(x):', y_x)

        # y(s) при замене x на S
        y_s = y_x.subs(x, s)
        # print('y(s):', y_s)

        # g(x) с подстановкой y(s)
        g_x = eval(f'{K_xs} * ({y_s})')
        # print('g(x):', g_x)

        # Интеграл
        # print(f'g(x): {lyamda} * ({sp.integrate(g_x, (s, ab[0], ab[1]))}) + {func_X}')
        integral_expr = lyamda * sp.integrate(g_x, (s, ab[0], ab[1])) + sp.parse_expr(func_X)
        # print("Решение интеграла", sp.integrate(g_x, (s, ab[0], ab[1])))
        # print("Функция после решения интеграла:", integral_expr)

        # Преобразование интегрального выражения в функцию
        g_x_func = sp.lambdify(x, integral_expr, 'numpy')
        y_x_func = sp.lambdify(x, y_x, 'numpy')

        # Точки интервала
        interval_points1 = np.linspace(ab[0], ab[1], 100)
        interval_points = np.array(interval_points1[::2])

        # Вычисление значений функций в точках интервала
        g_x_values = np.array([g_x_func(xi) for xi in interval_points])
        y_x_values = np.array([y_x_func(xi) for xi in interval_points])



        # Вычисление погрешностей
        errors = np.abs(y_x_values - g_x_values)
        max_error = np.max(errors)
        min_error = np.min(errors)

        # print("Погрешности:", errors)
        print("Максимальная погрешность:", max_error)
        print("Минимальная погрешность:", min_error)

        Graph(simplified_expression ,g_x_func, ab)






#---------------

    btn = Button(window, text = "        ", command = clicked, font = "Arial 11")       # Кнопка запуска
    btn.place(relx=0.8, rely=0.8, anchor=CENTER)

#---------------

    window.mainloop()




                                            # λ = 8, [a, b] = [2, 3], K(X,S) = 4*(x**2+s**2), f(x) = 9*x-7


if __name__ == "__main__":

    # start_timer = datetime.datetime.now()
    Start()
    # finish_timer = datetime.datetime.now();   print('Время работы: ' + str(finish_timer - start_timer))