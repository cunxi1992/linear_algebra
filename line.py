# -*- coding: UTF-8 -*-
from decimal import Decimal, getcontext
from vector import Vector

'''
定义Line类，该类用于计算两条直线的交点，定义的函数分别如下：
1、判断两条直线是否平行
2、判断两条直线是否重合
3、判断两条直线唯一交点
4、计算直线的基准点
5、获取直线的第一个非零系数


'''

getcontext().prec = 30

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    # normal_vector表示法向量
    # constant_term直线等式的常量
    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2
        if not normal_vector:
            all_zeros = ['0'] * self.dimension # 初始化一个list ['0','0']，函数里面用了 Decimal 处理 就可以用 ['0']，这个会把字符串转换成10进制的数
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0') # constant_term = 0
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()

    # 求ax+by=c的基准点:
    # 假设x=0 => (0,c/b); y轴上的一个点
    # 假设y=0 => (c/a,0); x轴上的一个点
    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates # 向量Vector对象不是iterable的，所以要用 .coordinates 将其转化为iterable
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension # 初始化一个list ['0','0']

            initial_index = Line.first_nonzero_index(n) # 找出法向量的第一个不是0的位置index,比如[1,2]返回0
            initial_coefficient = n[initial_index] # 取出这个位置上的数

            basepoint_coords[initial_index] = c / Decimal(initial_coefficient) # 用系数除以该数,并放入到该数的位置index
            self.basepoint = Vector(basepoint_coords) # 基准点为 [basepoint_coords[initial_index],0],或 [0,basepoint_coords[initial_index]]

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod # 静态方法,第一个不是0的index位置,例如[1,2]返回0,[0,2]返回1
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable): # enumerate 返回索引及索引处的值
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    # 两条直线是否平行
    def is_parallel_to(self, l):
        n1 = self.normal_vector # 直线l1的法向量
        n2 = l.normal_vector # 直线l2的法向量
        return n1.is_parallel_to(n2) # 定义:两条直线的法向量平行,则两条直线平行

    # 两条直线是否重合
    def isEqualTo(self,l):
        p1 = self.basepoint # l1上的一个点,我们找基准点比较方便
        p2 = l.basepoint # l2上的一个点
        v =  p1.minus(p2) # 连接两个点的向量
        n = self.normal_vector # 直线l1的法向量
        return v.is_orthogonal_to(n) # 定义:与两条直线的法向量都正交,则两条直线重合,is_orthogonal_to

    # 计算两条直线的交点
    def intersection_with(self,l):
        isParalle = self.is_parallel_to(l)
        if isParalle:
            if(self.isEqualTo(l)):
                print("两条直线重合,有无数个交点.")
            else:
                print("两条直线平行,没有交点.")
        else:
            # 两条直线不平行，计算唯一交点
            A,B = self.normal_vector.coordinates # Ax+By=K1
            K1 = self.constant_term
            C,D= l.normal_vector.coordinates # Cx+Dy=K2
            K2 =l.constant_term
            x = D*K1 - B*K2
            y = -C*K1 + A*K2
            times = Decimal('1')/(A*D-B*C)
            print("两条直线有唯一交点.")
            return Vector([x,y]).times_scalar(times)


class MyDecimal(Decimal):

    # 检测某个数字是否在误差范围0内
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


