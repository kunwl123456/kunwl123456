# 🤖 CSDN 数据自动更新指南

## 📋 功能说明

自动爬取你的 CSDN 博客统计数据，并更新到 GitHub Profile README 中：
- 📊 博客访问量
- 📝 原创文章数
- 🏆 CSDN 排名
- 👍 获得点赞数

## 🚀 使用方法

### 方法一：在 GitHub 仓库中使用（推荐）

#### 1. 创建同名仓库
在 GitHub 创建一个与你用户名同名的仓库（如 `kunwl123456/kunwl123456`）

#### 2. 上传文件
将以下文件上传到仓库：
```
kunwl123456/
├── README.md
├── .github/
│   └── workflows/
│       └── update-csdn-stats.yml
└── scripts/
    ├── update_csdn_stats.py
    └── requirements.txt
```

#### 3. 启用 GitHub Actions
- 进入仓库的 `Settings` → `Actions` → `General`
- 确保 Actions 权限设置为允许读写

#### 4. 自动运行
- 每天北京时间早上 8 点自动运行
- 或在 Actions 页面手动触发

### 方法二：本地测试

#### 1. 安装依赖
```bash
cd scripts
pip install -r requirements.txt
```

#### 2. 运行脚本
```bash
python update_csdn_stats.py
```

#### 3. 查看结果
脚本会自动更新 `README.md` 中的数据

## 📝 README 格式要求

你的 README 中必须包含以下格式的代码块：

```cpp
map<string, int> achievements = {
    {"博客访问量", 667317},
    {"原创文章", 438},
    {"CSDN排名", 14014},
    {"获得点赞", 1107}
};
```

脚本会自动识别并更新这些数字。

## 🔧 自定义配置

### 修改更新频率

编辑 `.github/workflows/update-csdn-stats.yml`：

```yaml
on:
  schedule:
    # 修改 cron 表达式
    - cron: '0 0 * * *'  # 每天 UTC 0点（北京时间8点）
    # - cron: '0 */6 * * *'  # 每6小时一次
    # - cron: '0 0 * * 1'  # 每周一
```

### 修改 CSDN 地址

编辑 `scripts/update_csdn_stats.py`：

```python
CSDN_URL = "https://blog.csdn.net/你的CSDN用户名"
```

## ⚠️ 注意事项

1. **GitHub Actions 权限**
   - 确保仓库启用了 Actions
   - 给予 Actions 写权限（Settings → Actions → Workflow permissions → Read and write）

2. **爬虫限制**
   - CSDN 可能有反爬虫机制
   - 建议不要设置过于频繁的更新（每天一次足够）

3. **数据准确性**
   - CSDN 页面结构变化可能导致爬取失败
   - 脚本会在控制台输出详细日志

4. **备用方案**
   - 如果自动更新失败，可以手动运行脚本
   - 或者在 Actions 页面查看错误日志

## 🐛 故障排查

### 问题1：Actions 没有运行
**解决方案**：
- 检查 `.github/workflows/` 文件路径是否正确
- 确保仓库启用了 Actions

### 问题2：数据没有更新
**解决方案**：
- 查看 Actions 运行日志
- 本地测试脚本是否能正常获取数据
- 检查 CSDN 页面结构是否改变

### 问题3：权限错误
**解决方案**：
- Settings → Actions → Workflow permissions
- 选择 "Read and write permissions"
- 勾选 "Allow GitHub Actions to create and approve pull requests"

## 📊 效果展示

更新前：
```cpp
{"博客访问量", 667317}
```

自动更新后：
```cpp
{"博客访问量", 680000}  // 实时数据
```

## 💡 进阶功能

### 添加徽章显示

在 README 中添加动态徽章：

```markdown
![CSDN访问](https://img.shields.io/badge/dynamic/json?color=red&label=CSDN访问&query=views&url=YOUR_API_ENDPOINT)
```

### 多数据源支持

可以扩展脚本支持：
- GitHub Stats
- LeetCode 数据
- 博客园数据
- 掘金数据

## 🔗 相关资源

- [GitHub Actions 文档](https://docs.github.com/actions)
- [CSDN API（非官方）](https://github.com/topics/csdn-api)
- [Beautiful Soup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## 📧 问题反馈

如有问题，请在仓库中提 Issue。

