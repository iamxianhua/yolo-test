# YOLO 检测结果分析 Skill 使用指南

## 概述

这个 skill 和配套工具可以帮助您深入分析 YOLO 检测结果，评估检测质量，并提供优化建议。

## 文件说明

### 1. Claude Code Skill
📁 `.claude/skills/yolo-detection-analysis/SKILL.md`
- Claude Code 自动识别的技能文件
- 当您询问检测结果、准确率、性能时自动激活
- 提供专业的分析指导和优化建议

### 2. 检测分析工具
📄 `detection_analyzer.py`
- 独立的检测结果分析工具
- 可集成到任何 YOLO 检测脚本中
- 提供详细的统计和可视化报告

### 3. 集成示例脚本
📄 `yolo-test-with-analysis.py`
- 基于原 `yolo-test.py` 的增强版本
- 自动集成了检测分析功能
- 支持单张和批量图片检测

---

## 快速开始

### 方式 1：使用集成脚本（推荐）

检测单张图片并分析：
```bash
python3 yolo-test-with-analysis.py -i data/person.jpg
```

调整参数进行检测：
```bash
python3 yolo-test-with-analysis.py -i data/dog.jpg -c 0.6 -t 0.3
```

批量检测目录中的所有图片：
```bash
python3 yolo-test-with-analysis.py -b data/ -p "*.jpg"
```

不显示窗口（服务器环境）：
```bash
python3 yolo-test-with-analysis.py -i data/kite.jpg --no-show
```

### 方式 2：集成到现有代码

在您的检测脚本中添加：

```python
from detection_analyzer import DetectionAnalyzer, quick_analyze

# ... 您的 YOLO 检测代码 ...

# 检测完成后，添加分析
quick_analyze(boxes, confidences, classIDs, labels, inference_time)
```

完整示例：
```python
import numpy as np
import cv2 as cv
from detection_analyzer import quick_analyze

# 加载模型和检测...
# (您的现有代码)

# 在得到检测结果后：
if len(boxes) > 0:
    # 分析结果
    quick_analyze(
        boxes=boxes,
        confidences=confidences,
        classIDs=classIDs,
        labels=labels,
        inference_time=end_time - start_time
    )
```

### 方式 3：向 Claude 提问（自动使用 Skill）

在 Claude Code 中直接询问：

```
"我的 YOLO 检测到 3 个人，置信度是 0.85、0.62、0.48，质量如何？"

"YOLO 检测速度很慢，每张图要 500ms，怎么优化？"

"检测结果总是有很多误检，如何减少？"

"如何提高小物体的检测准确率？"
```

Claude 会自动应用 `yolo-detection-analysis` skill，提供专业分析。

---

## 分析报告示例

运行检测后，您会看到类似这样的分析报告：

```
============================================================
YOLO 检测结果分析报告
============================================================
分析时间: 2026-01-07 10:30:15

[基本信息]
  检测框数量: 5
  平均置信度: 72.40%
  推理时间: 125.00 ms
  FPS: 8.00

[检测类别分布]
  person: 3 个
  car: 1 个
  bicycle: 1 个

[置信度分布]
  高置信度 (>0.8): 2 个 [40.0%]
  中等置信度 (0.5-0.8): 2 个 [40.0%]
  低置信度 (<0.5): 1 个 [20.0%]

[检测详情]
  #1: person          置信度: 89.50%  ✅ 优秀
  #2: car             置信度: 85.20%  ✅ 优秀
  #3: person          置信度: 68.30%  ✅ 良好
  #4: bicycle         置信度: 62.10%  ✅ 良好
  #5: person          置信度: 47.00%  ❌ 较差

[质量评估]
  优点:
    ✅ 平均置信度较高 (72.40%)

  问题:
    ❌ 存在较多低置信度检测 (20.0%)，可能有误检

  总体评价: ✅ 检测质量良好

[优化建议]
  1. 📌 检测到较多低置信度结果，建议提高 CONFIDENCE 阈值到 0.6-0.7 以减少误检
  2. ⚡ 推理时间适中 (125ms)，如需提升：
     - 可尝试使用 GPU 加速
     - 或适当减小输入尺寸

============================================================
```

---

## 命令行参数

### yolo-test-with-analysis.py 参数

| 参数 | 简写 | 说明 | 默认值 | 示例 |
|------|------|------|--------|------|
| --image | -i | 输入图片路径 | data/person.jpg | `-i dog.jpg` |
| --confidence | -c | 置信度阈值 | 0.5 | `-c 0.6` |
| --threshold | -t | NMS 阈值 | 0.4 | `-t 0.3` |
| --no-show | - | 不显示窗口 | False | `--no-show` |
| --no-analyze | - | 不分析结果 | False | `--no-analyze` |
| --batch | -b | 批量处理目录 | - | `-b data/` |
| --pattern | -p | 文件匹配模式 | *.jpg | `-p "*.png"` |

---

## 使用场景

### 场景 1：调试检测质量

**问题**：不确定当前参数是否合适

**解决方案**：
```bash
# 使用默认参数检测
python3 yolo-test-with-analysis.py -i data/person.jpg

# 查看分析报告中的建议
# 根据建议调整参数
python3 yolo-test-with-analysis.py -i data/person.jpg -c 0.65 -t 0.35

# 对比效果
```

### 场景 2：批量评估

**问题**：需要评估模型在整个数据集上的表现

**解决方案**：
```bash
# 批量处理所有图片
python3 yolo-test-with-analysis.py -b data/ --no-show

# 查看汇总统计
```

### 场景 3：性能优化

**问题**：检测速度不够快

**解决方案**：
```bash
# 测试当前性能
python3 yolo-test-with-analysis.py -i data/kite.jpg

# 查看报告中的性能建议
# 尝试减小输入尺寸（需修改代码中的 (416,416)）
# 或使用 GPU 加速
```

### 场景 4：对比不同参数

**问题**：想找到最佳参数组合

**解决方案**：
```bash
# 测试不同的置信度阈值
python3 yolo-test-with-analysis.py -i test.jpg -c 0.4
python3 yolo-test-with-analysis.py -i test.jpg -c 0.5
python3 yolo-test-with-analysis.py -i test.jpg -c 0.6
python3 yolo-test-with-analysis.py -i test.jpg -c 0.7

# 对比分析报告，选择最佳值
```

---

## 高级功能

### 1. 导出分析报告

修改代码以导出 JSON 报告：

```python
from detection_analyzer import DetectionAnalyzer

analyzer = DetectionAnalyzer()

# 分析多次检测
analyzer.analyze_detection_result(boxes1, confidences1, ...)
analyzer.analyze_detection_result(boxes2, confidences2, ...)

# 导出历史报告
analyzer.export_report("my_analysis.json")
```

### 2. 历史对比

```python
# 分析多次后
analyzer.compare_with_history()
```

### 3. 自定义分析逻辑

继承 `DetectionAnalyzer` 类添加自定义功能：

```python
from detection_analyzer import DetectionAnalyzer

class MyAnalyzer(DetectionAnalyzer):
    def analyze_small_objects(self, boxes):
        """自定义：分析小物体检测情况"""
        small_boxes = [b for b in boxes if b[2]*b[3] < 1000]
        print(f"检测到 {len(small_boxes)} 个小物体")
```

---

## 与 Claude Skill 配合

### Skill 自动激活场景

当您在 Claude Code 中提问以下类型问题时，skill 会自动激活：

✅ **检测质量相关**：
- "这个检测结果好不好？"
- "置信度 0.6 算高还是低？"
- "为什么有这么多重复的框？"

✅ **性能优化相关**：
- "如何提高检测速度？"
- "推理时间太长怎么办？"
- "能实时检测吗？"

✅ **参数调整相关**：
- "CONFIDENCE 应该设置多少？"
- "NMS 阈值如何调整？"
- "如何减少误检？"

✅ **问题诊断相关**：
- "为什么检测不到小物体？"
- "漏检太多怎么办？"
- "边界框不准确如何解决？"

### Skill 提供的帮助

- 📊 **详细分析指导**：逐步分析检测结果
- 💡 **优化建议**：针对性的参数调整建议
- 🔍 **问题诊断**：识别常见问题并提供解决方案
- 📈 **性能评估**：评估检测速度和资源使用
- ✅ **最佳实践**：遵循 YOLO 检测的业界标准

---

## 常见问题

### Q: 需要安装额外依赖吗？

A: 不需要。`detection_analyzer.py` 只使用 Python 标准库。

### Q: 可以用于其他 YOLO 版本吗？

A: 可以。只要检测结果格式相同（boxes, confidences, classIDs），就能使用。

### Q: 分析会影响检测速度吗？

A: 分析本身非常快（<10ms），不会显著影响性能。

### Q: 如何只运行检测不分析？

A: 使用 `--no-analyze` 参数：
```bash
python3 yolo-test-with-analysis.py -i test.jpg --no-analyze
```

### Q: Skill 和工具有什么区别？

A:
- **Skill**：提供理论指导和建议，通过 Claude 对话激活
- **工具**：实际分析检测数据，生成报告

两者配合使用效果最佳！

---

## 技巧和建议

### 💡 提示 1：参数调优流程

1. 使用默认参数检测
2. 查看分析报告
3. 根据建议调整参数
4. 重新检测并对比
5. 重复直到满意

### 💡 提示 2：性能基准

记录不同配置的性能数据：
```bash
# 创建性能日志
echo "Config,Time(ms),FPS,Detections" > performance.csv

# 测试不同配置并记录
# (手动或脚本化)
```

### 💡 提示 3：可视化对比

保存不同参数的检测结果图片，直观对比效果。

### 💡 提示 4：询问 Claude

遇到问题时，直接向 Claude 描述：
```
"我用 YOLO 检测了一张有 5 个人的照片，但只检测到 3 个，
置信度是 0.7、0.6、0.52。为什么会漏检？如何改进？"
```

Claude 会利用 skill 知识给出专业建议。

---

## 更新日志

**v1.0** (2026-01-07)
- ✅ 创建 YOLO 检测分析 Skill
- ✅ 开发 detection_analyzer.py 工具
- ✅ 创建集成示例脚本
- ✅ 支持单张和批量检测
- ✅ 提供详细分析报告
- ✅ 参数化配置

---

## 贡献与反馈

如有问题或建议，请：
1. 向 Claude 提问（自动使用 skill）
2. 检查分析报告中的建议
3. 参考 `.claude/skills/yolo-detection-analysis/SKILL.md`

---

## 许可证

MIT License - 自由使用和修改
