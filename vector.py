# -*- coding: UTF-8 -*-
from math import *
from decimal import *

'''
定义Vector类，该类用于向量的各类计算，共计定义了15个向量计算函数，分别如下：
1.两个向量的和
2.两个向量的差
3.标量乘法
4.计算向量的大小
5.向量标准化
6.两个向量的内积
7.两个向量之间的夹角
8.判断向量是否为零向量
9.判断向量是否正交
10.判断向量是否平行
11.计算给定向量的情况下，与基向量的正交向量
12.计算一个向量在另一个向量上的投影
13.计算两个向量的向量积
14.计算两个向量形成的平行四边形的面积
15.计算两个向量形成的三角形的面积

'''

# 设定十进制数学计算下，小数点的精度保留为30位
getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):

        # 若coordinate为none，则抛出异常，否则执行语句
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates]) # 将传入的参数转换为 元组 类型,Decimal确保所有坐标都为小数，而不是浮点数和整数
            self.dimension = len(coordinates)  # 计算 元组 长度

        # 若异常为 ValueError ，则将异常继续往上抛，上层没处理的话，整个程序会异常退出，输出 异常提示，并中断程序
        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        # 若异常为 TypeError ，则将异常继续往上抛，上层没处理的话，整个程序会异常退出，输出 异常提示，并中断程序
        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    # 把类的实例转化为字符串，print 时被调用
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    # 运算符 等于 重载，比较==时会被调用
    def __eq__(self, v):
        return self.coordinates == v.coordinates

    # 定义函数，计算两个向量的和
    def plus(self,v):
        new_coordinates = [x+y for x,y in zip(self.coordinates,v.coordinates)] #使用zip将向量x和向量y中对应的元素打包成一个元组，然后返回由这些元组组成的列表
        return Vector(new_coordinates) # 强制转换为Vector类并返回

    # 定义函数，计算两个向量的差
    def minus(self,v):
        new_coordinates = [x-y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(new_coordinates) # 强制转换为Vector类并返回

    # 定义函数，计算标量乘法
    def times_scalar(self,c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates] # Decimal 确定Vector对象外部的数字也被设置为小数，为了防止两个方向相同的单位向量相乘时因精度缺失导致向量内积大于1
        return Vector(new_coordinates) # 强制转换为Vector类并返回

    # 定义函数，计算向量的大小
    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared)) # sum 函数用来对系列进行求和计算

    # 定义函数，对向量进行归一化
    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1/magnitude) 
        except ZeroDivisionError as e: # 若 除(或取模)零，则抛出异常
            raise Exception('Can not normalize the zero vector')

    # 定义函数，用于计算两个向量的内积
    def dot(self,v):
        return (sum([x*y for x,y in zip(self.coordinates,v.coordinates)]))

    # 定义函数，用于计算两个向量之间的夹角
    def angle_with(self,v,in_degrees = False):
        try:
            u1 = self.normalized() # 标准化调用对象
            u2 = v.normalized()
            angle_in_radians = acos(u1.dot(u2)) #计算两个标准化向量的夹角

            if in_degrees:
                degrees_per_radians = 180.0 / pi
                return angle_in_radians * degrees_per_radians
            else:
                return angle_in_radians
        except ZeroDivisionError as e:
            raise Exception('Can not normalize the zero vector')


    # 判断一个向量是否为零向量,由于精度问题，引入公差，判断向量的大小若小于公差，则判定为零向量
    def is_zero(self,tolerance = 1e-10):
        return self.magnitude() < tolerance

    # 判断两个向量是否正交,由于精度问题，引入公差，若两个向量的内积小于公差，则判定为正交
    def is_orthogonal_to(self,v,tolerance = 1e-10):
        return abs(self.dot(v)) < tolerance

    # 判断两个向量是否平行
    def is_parallel_to(self,v):
        p = True
        if self.is_zero() or v.is_zero():
            return p
        else:
            a = round(self.coordinates[0]/v.coordinates[0],3) 
            for i in range(len(self.coordinates)): # range(5) 代表从0到5，不包含5，即[0,1,2,3,4]
                if(round(self.coordinates[i]/v.coordinates[i],3) != a): # 比较两个向量相同索引处的比值，若均相同，则表示两个向量平行
                    p =False
            return p


    # 计算给定向量的情况下，与基向量的正交向量
    def component_orthogonal_to(self,basic):
        try:
            projection = self.component_parallel_to(basic) # 计算一个向量在另一个向量上的投影
            return self.minus(projection)  # 计算基向量的正交向量
        except ZeroDivisionError:  # 若 除(或取模)零，则抛出异常
            raise ZeroDivisionError('Can not normalize the zero vector')

    # 定义函数，计算一个向量在另一个向量上的投影
    def component_parallel_to(self,basic):
        try:
            u = basic.normalized()  # 对基向量进行标准化，得出单位向量
            weight = self.dot(u)    # 计算向量与单位向量的 内积
            return u.times_scalar(weight)  # 将内积与单位向量相乘，即使用 标量乘法，并返回得到的新向量，这个向量即为向量 在 基向量 上的投影向量

        except ZeroDivisionError:  # 若 除(或取模)零，则抛出异常
            raise ZeroDivisionError('Can not normalize the zero vector')

    # 定义函数，计算两个向量的向量积
    def cross(self,v):
        try:
            x_1,y_1,z_1 = self.coordinates
            x_2,y_2,z_2 = v.coordinates
            new_coordinates = [ y_1*z_2 - y_2*z_1,
                                -(x_1*z_2 - x_2 *z_1),
                                x_1*y_2 - x_2*y_1 ]

            return Vector(new_coordinates)  # 强制转换为Vector类并返回
        except ValueError as e: #异常捕获，以防self或v在三维空间里不是向量
            if mes == 'need more than 2 values to unpack': # 如果两个向量是二维的，就向每个向量中添加为0的z轴坐标，然后再计算向量积
                self_embedded_in_R3 = Vector(self.coordinates + (0,))
                v_embedded_in_R3 = Vector(v.coordinates + (0,))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or msg == 'need more than 1 value to unpack'):
                raise Exception('Can not normalize the zero vector')
            else:
                raise e

    # 定义函数，用于计算两个向量形成的平行四边形的面积
    def area_of_parallelogram_with(self,v):
        cross_product = self.cross(v)
        return cross_product.magnitude()


    # 定义函数，用于计算两个向量形成的三角形的面积
    def area_of_triangle_with(self,v):
        return self.area_of_parallelogram_with(v) / 2
