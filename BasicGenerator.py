# -*- coding: UTF-8 -*-

import codecs
import string


class BasicGenerator:
    """基础的生成类"""
    id_count = 0
    anchor_count = 0

    def generateContent(self, i, lines):
        line = lines[i]
        # 所有的匹配规则都是自己定的
        # 不同规则给不同的class，然后给class样式
        if line.startswith("#### "):
            """四级标题"""
            return '<div class="forth-level" >' + line.replace('#### ', '') + '</div>', i + 1
        elif line.startswith("### "):
            """三级标题"""
            return '<div class="third-level" >' + line.replace('### ', '') + '</div>', i + 1
        elif line.startswith("## "):
            """二级标题"""
            self.id_count += 1
            return '<div class="second-level" id="a' + str(self.id_count) + '" >' + line.replace('## ',
                                                                                                 '') + '</div>', i + 1
        elif line.startswith("# "):
            """一级标题"""
            self.id_count += 1
            return '<div class="first-level" id="a' + str(self.id_count) + '"  >' + line.replace('# ',
                                                                                                 '') + '</div>', i + 1
        elif line.startswith("-img|"):
            """图片"""
            item = line.split('|')
            # if len(item) == 2:
            return '<img class="my-img" src="' + item[1] + '" />', i + 1
            # else:
            #     if str.strip(item[2]) == "":
            #         return '<img class="my-img" src="' + item[1] + '" />', i + 1
            #     return '<div class="my-formula-img">' \
            #            '<img class="my-img" src="' + item[1] + '" />' \
            #         '<span>' + item[2] + '</span></div>', i + 1
        else:
            """内容"""
            return '<p class="my-content" >' + line + '</p>', i + 1

    def generateTeam(self, line):
        temp_arr = []
        target_html = []
        img_arr = []

        try:
            val = int(line)
            if len(temp_arr):
                temp_arr.append('</div>\n</div>')
                target_html.append('\n'.join(temp_arr))
                temp_arr.clear()

        except ValueError:
            if len(temp_arr) == 0:
                temp_arr.append('<div class="slider__item">')

            if line.startswith("-img|"):
                """图片"""
                temp_arr.append('<img class="my-img" src="' + line.replace('-img|', '') + '" />')
                img_arr.append('<a href="#' + str(len(target_html)) +
                               '"><img src="' + line.replace('-img|', '') + '" alt="" /></a>')
                temp_arr.append('<div class="slider__caption">')
            else:
                """内容"""
                temp_arr.append('<p class="my-content" >' + line + '</p>')

        # Teacher

        try:
            val = int(line)
            if len(temp_arr):
                temp_arr.append('</div>')
                target_html.append('\n'.join(temp_arr))
                temp_arr.clear()

        except ValueError:
            if len(temp_arr) == 0:
                temp_arr.append('<div class="teacher-item">')

            if line.startswith("-img|"):
                """图片"""
                temp_arr.append('<img class="my-img" src="' + line.replace('-img|', '') + '" />')
            elif line.startswith("# "):
                """一级标题"""
                temp_arr.append('<div class="first-level" >' + line.replace('# ', '') + '</div>')
            else:
                """内容"""
                temp_arr.append('<p class="my-content" >' + line + '</p>')

        return '\n'.join(target_html), '\n'.join(img_arr)

    def generateTable(self, i, lines):
        target_html = []
        pos = i
        target_html.append('<table>')

        while not lines[pos].startswith("-table-end|"):
            item = lines[pos]
            _tr = ['<tr>']
            if pos == i:
                # 页头
                words = item.split('#')
                for word in words:
                    _tr.append('<td>' + word + '</td>')
            else:
                # 内容
                words = item.split('#')
                for word in words:
                    _tr.append('<td>' + word + '</td>')
            _tr.append('</tr>')
            target_html.append('\n'.join(_tr))
            pos += 1

        target_html.append('</table>')
        # 跳到下一行
        pos += 1
        return '\n'.join(target_html), pos

    def generateRight(self, i, lines):
        target_html = []
        pos = i
        target_html.append('<div class="content-wrapper">')

        left = ['<div class="content-left">']
        right = ['<div class="content-right">']
        while not lines[pos].startswith("-middle|"):
            item = lines[pos]
            if item.startswith('-img|'):
                left.append('<img class="my-img" src="' + item.replace('-img|', '') + '" />')
            else:
                left.append('<p class="my-content" >' + item + '</p>')
            pos += 1
        left.append('</div>')
        pos += 1

        while not lines[pos].startswith("-right-end|"):
            item = lines[pos]
            if item.startswith('-img|'):
                right.append('<img class="my-img" src="' + item.replace('-img|', '') + '" />')
            else:
                right.append('<p class="my-content" >' + item + '</p>')
            pos += 1
        right.append('</div>')

        target_html.append('\n'.join(left))
        target_html.append('\n'.join(right))
        target_html.append('</div>')
        pos += 1

        return '\n'.join(target_html), pos

    def generateNav(self, lines):
        navs = ['<div id="my-sidebar">',
                '<div class="sidebar__inner">',
                '<div class="side-top">',
                '<img src="http://2018.igem.org/wiki/images/5/53/T--CIEI-BJ--Team--logo.jpg" alt="side_top">',
                # '<img src="http://2017.igem.org/wiki/images/0/09/T--CIEI-China--Home--logo.jpg" alt="side_top">',
                '</div>',
                '<ul class="page-anchors">']

        nav_lis = []
        first_level = False
        second_level = False
        for line in lines:
            if line.startswith("## "):
                self.anchor_count += 1
                if first_level:
                    nav_lis.append('<ul>')
                if second_level:
                    nav_lis.append('</li>')

                second_level = True
                first_level = False
                nav_lis.append('<li><a href="#a' + str(self.anchor_count)
                               + '">' + line.replace("## ", '') + '</a>')

            elif line.startswith("# "):
                self.anchor_count += 1
                if second_level:
                    nav_lis.append('</li>')
                    nav_lis.append('</ul></li>')

                second_level = False
                first_level = True
                nav_lis.append('<li><a href="#a' + str(self.anchor_count)
                               + '">' + line.replace("# ", '') + '</a>')

        if second_level:
            nav_lis.append('</li>')
            nav_lis.append('</ul>')
        if first_level:
            nav_lis.append('</li>')

        navs.append('\n'.join(nav_lis))

        navs.append('</ul>')
        navs.append('</div>')
        navs.append('</div>')

        return '\n'.join(navs)

    def loop_kinds(self, i, lines):
        target = []
        while i < len(lines):
            item = lines[i]
            if item.startswith("-table|"):
                table, pos = self.generateTable(i + 1, lines)
                target.append(table)
            elif item.startswith("-right|"):
                right, pos = self.generateRight(i + 1, lines)
                target.append(right)
            else:
                content, pos = self.generateContent(i, lines)
                target.append(content)
            i = pos

        # 生成左侧导航
        print('<div id="my-container">')
        print(self.generateNav(lines))
        # print('<!--导航内容分割线-->')
        target.insert(0, '<div id="my-adjust-content"><div id="adjust-padder">')
        target.append('</div>')
        target.append('</div>')
        target.append('</div>')
        target.append('')
        target.append('<script type="text/javascript">'
                      "var a = new StickySidebar('#my-sidebar', {"
                      "	topSpacing: 50,"
                      "	containerSelector: '#my-container',"
                      "	innerWrapperSelector: '.sidebar__inner'"
                      '});</script>')
        return '\n'.join(target)

    def go(self, file):
        f_in = codecs.open(file, 'r', 'utf-8')
        lines = []

        for line in f_in:
            """剔除无用行"""
            line = line.strip()
            if len(line) <= 0:
                continue

            lines.append(line)

        f_in.close()

        return lines
