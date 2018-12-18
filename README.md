# iGEM-Code-Generator
helper for igem

---
2016年参加了iGEM,之后陆陆续续各种原因又写了几次,发现使用Python将文本转化为网页十分好用,节省了非常多的时间.

所以这个脚本的主要功能是生成iGEM网页代码.

igem_2016_from_above_picture
![2016 igem image](img/2016igem_picture.jpg)

# Usage
- `main.py`控制使用哪个目录下的脚本
- `BasicGenerator.py`按照既定规则,生成网站元素
- `SubGenerator.py`主要用于传入目录.读取该目录下的`data.txt`

# 生成规则
- 空行将被跳过.用多种标注识别不同元素.
- 以`-img|url`开头的元素,将被渲染成`<img>`标签,`url`对应图片的地址
- 以`# `,`## `, `### `, `#### `开头的元素,将被渲染成一级\二级\三级\四级标题.
- 表格表示标注方法
```
-table|
cell # cell # cell
-table-end|
```
- 左右布局标注方法
```
-right|
-img|url
-middle|
-img|url
-right-end|
```
将被渲染成左右布局.