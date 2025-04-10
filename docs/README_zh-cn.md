# Arcaea 谱面内容排序工具

对谱面里的条目按照固定规则排序，可以**更容易地比较两个谱面文件之间的关键差异。**

## 核心依赖 (`ArcaeaLib.py`)

`ArcaeaLib.py` 基于 [Arcaea-Infinity/ArcaeaLib](https://github.com/Arcaea-Infinity/ArcaeaLib)，并进行了以下更新：

1.  **浮点 Tap Lane 支持:**
    *   `Tap` 类及其解析器 (`ParseTap`) 现在可以正确处理 **浮点数** 的轨道位置 (例如，`(1000,1.5);`)。这使得它能够兼容使用小数轨道的谱面。
2.  **内部 Bug 修复:** 修复了 `Aff.Refresh` 方法中的内部排序问题，以防止谱面加载期间出现 `TypeError`。

## 排序脚本 (`sort_chart.py`)

**功能:** 根据确定的顺序对所有谱面事件进行排序。

1.  **主键:** 事件开始时间 (`StartTime`).
2.  **次要键:** 事件类型 (预定义的顺序，如 Timing, Tap, Hold, Arc 等).
3.  **三级键:** 类型特定的属性 (例如，Taps 的 `Lane`，Arcs 的 `Color`/`XStart`/`YStart` 等)，以确保即使在同一时间发生多个相同类型的事件时也能保持一致的顺序。
4.  `timinggroup` 环境内的内容，将在环境中独立排序。

## 用法

````bash
python sort_chart.py <你的谱面文件路径.aff>
````

**示例:**

````bash
python sort_chart.py 2.aff
````

此命令将加载 `2.aff`，对其内容进行排序，并将结果保存到 `2_sorted.aff`。

## 支持

喜欢的话请给一个 star！您的支持是我持续开发的最大动力！

如果有问题，请提交 issue！

如果有好的修改方案，请提交 Pull Request！

<div style="text-align: center;">
    <img src="../docs/appreciation.png" style="height:150px;">
</div>

<center>感谢支持！❤</center>
<br>

> 如果可以，请在“赞助备注”中留下个人主页，谢谢支持！