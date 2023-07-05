# listen12lx-music
a simple tool to trans song lists data from listen1 to lx-music

这是一个用于转换 [Listen 1](https://listen1.github.io/listen1/) 与 [lx music](https://github.lxmusic.folltoshe.com/) 的歌单数据文件的脚本

已实现从 listen 1 -> lx music，
逆向等需要时再实现

# 用法
1. 导出 listen1 的数据文件
2. 找到 lx music [数据目录](https://github.lxmusic.folltoshe.com/desktop/document/data-path.html)下的 lx.data.db
3. 使用脚本
   ```
   $python transform.py $FILENAME.json lx.data.db
   ```
