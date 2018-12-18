# -*- coding: UTF-8 -*-

from BasicGenerator import BasicGenerator


class SubGenerator(BasicGenerator):
    """子类，主要是为了传入文件路径"""

    def __init__(self):
        self.lines = self.go('Project/Model/data.txt')

    def generate(self):
        print(self.loop_kinds(0, self.lines))


SubGenerator().generate()