import os
import random
import unittest


class TestSequenceFunctions(unittest.TestCase):
    # 尝试使用 range()创建整数列表（导致“TypeError: 'range' object does not support item assignment”）
    # 有时你想要得到一个有序的整数列表，所以 range() 看上去是生成此列表的不错方式。然而，你需要记住 range() 返回的是 “range object”，而不是实际的 list 值。
    # 注意：在 Python 2 中 spam = range(10) 是能行的，因为在 Python 2 中 range() 返回的是list值，但是在 Python 3 中就会产生以上错误
    def setUp(self):
        print('测试开始执行')
        # self.seq = list(range(10))
        self.seq = range(2)
        print(" seq:", self.seq, '-->File "uni_test.py", line 14')
        

    # shuffle()方法将序列的所有元素随机排序
    # 1、语法
    # 以下是shuffle()方法的语法：
    # import random
    # random.shuffle(lst)
    # 注意：shuffle()是不能直接访问的，需要导入random模块，然后通过random静态对象调用该方法
    # 2、参数
    # lst 可以是一个序列或者元组
    # 3、返回值
    # 返回随机排序后的序列
    def test_shuffle(self):
        print('测试shuffle方法')
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))
        self.assertRaises(TypeError, random.shuffle, (1, 2, 3))

    def test_choice(self):
        print('测试choice方法')
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)
    # def test_a(self):
    #     print('测试方法')
    #     ook= (1==2-1)
    #     ook= (1==2-11)
    #     print(" ook:", ook, '-->File "uni_test.py", line 40')
    #
    #     element = random.choice(self.seq)
    #     self.assertTrue(ook)
    #
    def tearDown(self):
        print('测试执行结束')


if __name__ == '__main__':
    unittest.main()
