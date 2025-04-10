# Arcaea Chart Content Sorter

<p align="center">
  <a href="/docs/README_zh-cn.md">简体中文</a>
</p>

This sorter provides a utility to sort content in Arcaea .aff chart files according to specified rules, **making it easier to compare the essential differences between two chart files.**

## Core Library (`ArcaeaLib.py`)

`ArcaeaLib.py` based on [Arcaea-Infinity/ArcaeaLib](https://github.com/Arcaea-Infinity/ArcaeaLib), has been updated with the following changes:

1.  **Floating-Point Tap Lane Support:**
    *   The `Tap` class and its parser (`ParseTap`) now correctly handle **floating-point numbers** for lane positions (e.g., `(1000,1.5);`). This allows compatibility with charts using fractional lanes.
2.  **Internal Bug Fixes:** Addressed internal sorting issues within the `Aff.Refresh` method to prevent `TypeError` during chart loading.

## Sorting Script (`sort_chart.py`)

**Function:** Sorts all chart events based on a deterministic order.

1.  **Primary Key:** Event Start Time (`StartTime`).
2.  **Secondary Key:** Event Type (A predefined order like Timing, Tap, Hold, Arc, etc.).
3.  **Tertiary Keys:** Type-specific attributes (e.g., `Lane` for Taps, `Color`/`XStart`/`YStart` etc. for Arcs) to ensure a consistent order even when multiple events of the same type occur at the exact same time.
4. Sorting respects `timinggroup` blocks; events remain within their original group but are sorted internally.

## Usage

```bash
python sort_chart.py <path_to_your_chart.aff>
```

**Example:**

```bash
python sort_chart.py 2.aff
```

This command will load `2.aff`, sort its contents, and save the result to `2_sorted.aff`.

## Support

If you like this project, please give it a star! Your support is the greatest motivation for me to continue developing!

If you have any issues, please submit an issue!

If you have any good modification suggestions, please submit a Pull Request!

<div style="text-align: center;">
    <img src="./docs/appreciation.png" style="height:150px;">
</div>

<center>Thank you for your support! ❤</center>
<br>

> If possible, please leave your personal homepage in the "sponsor notes". Thank you for your support!