#!/usr/bin/env python3
"""
YOLO 检测分析演示
展示 detection_analyzer 的功能，使用模拟数据
"""

from detection_analyzer import DetectionAnalyzer
import random
import time

def demo_single_detection():
    """演示：单张图片检测分析"""
    print("=" * 70)
    print("演示 1: 单张图片检测分析")
    print("=" * 70)

    # 模拟检测结果：person.jpg
    labels = ['person', 'bicycle', 'car', 'motorbike', 'bus', 'dog', 'cat']

    # 模拟检测到 5 个物体
    boxes = [
        [50, 100, 120, 300],   # person 1
        [200, 80, 100, 280],   # person 2
        [400, 150, 80, 200],   # bicycle
        [320, 90, 110, 290],   # person 3
        [600, 200, 60, 80]     # dog
    ]

    confidences = [0.89, 0.75, 0.68, 0.52, 0.45]
    classIDs = [0, 0, 1, 0, 5]  # person, person, bicycle, person, dog
    inference_time = 0.125  # 125ms

    analyzer = DetectionAnalyzer()
    analyzer.analyze_detection_result(boxes, confidences, classIDs, labels, inference_time)

    return analyzer

def demo_high_quality_detection():
    """演示 2: 高质量检测结果"""
    print("\n" * 2)
    print("=" * 70)
    print("演示 2: 高质量检测结果（所有检测都是高置信度）")
    print("=" * 70)

    labels = ['person', 'bicycle', 'car', 'motorbike', 'bus', 'dog', 'cat']

    # 高质量检测：所有置信度都很高
    boxes = [
        [50, 100, 120, 300],
        [200, 80, 100, 280],
        [400, 150, 80, 200]
    ]

    confidences = [0.92, 0.88, 0.85]
    classIDs = [0, 1, 2]  # person, bicycle, car
    inference_time = 0.045  # 45ms - 很快

    analyzer = DetectionAnalyzer()
    analyzer.analyze_detection_result(boxes, confidences, classIDs, labels, inference_time)

    return analyzer

def demo_poor_quality_detection():
    """演示 3: 低质量检测结果"""
    print("\n" * 2)
    print("=" * 70)
    print("演示 3: 低质量检测结果（很多低置信度检测）")
    print("=" * 70)

    labels = ['person', 'bicycle', 'car', 'motorbike', 'bus', 'dog', 'cat']

    # 低质量检测：很多低置信度
    boxes = [
        [50, 100, 120, 300],
        [200, 80, 100, 280],
        [400, 150, 80, 200],
        [320, 90, 110, 290],
        [600, 200, 60, 80],
        [100, 300, 40, 50],
        [500, 400, 30, 40]
    ]

    confidences = [0.58, 0.52, 0.48, 0.45, 0.42, 0.38, 0.35]
    classIDs = [0, 0, 1, 2, 5, 0, 1]
    inference_time = 0.420  # 420ms - 很慢

    analyzer = DetectionAnalyzer()
    analyzer.analyze_detection_result(boxes, confidences, classIDs, labels, inference_time)

    return analyzer

def demo_batch_analysis():
    """演示 4: 批量检测分析"""
    print("\n" * 2)
    print("=" * 70)
    print("演示 4: 批量检测统计")
    print("=" * 70)

    labels = ['person', 'bicycle', 'car', 'motorbike', 'bus', 'dog', 'cat']
    analyzer = DetectionAnalyzer()

    # 模拟处理 5 张图片
    for i in range(5):
        num_detections = random.randint(2, 6)
        boxes = [[random.randint(0, 600), random.randint(0, 400),
                 random.randint(50, 150), random.randint(100, 300)]
                for _ in range(num_detections)]
        confidences = [random.uniform(0.4, 0.95) for _ in range(num_detections)]
        classIDs = [random.randint(0, 6) for _ in range(num_detections)]
        inference_time = random.uniform(0.08, 0.25)

        print(f"\n处理图片 {i+1}/5...")
        analyzer.analyze_detection_result(boxes, confidences, classIDs, labels, inference_time)
        time.sleep(0.5)

    # 显示历史对比
    print("\n" * 2)
    analyzer.compare_with_history()

    # 导出报告
    analyzer.export_report("demo_analysis_report.json")

    return analyzer

def demo_comparison():
    """演示 5: 参数对比"""
    print("\n" * 2)
    print("=" * 70)
    print("演示 5: 不同参数设置对比")
    print("=" * 70)

    labels = ['person', 'bicycle', 'car', 'motorbike', 'bus', 'dog', 'cat']

    # 同一张图片，不同参数
    all_boxes = [
        [50, 100, 120, 300],
        [200, 80, 100, 280],
        [400, 150, 80, 200],
        [320, 90, 110, 290],
        [600, 200, 60, 80]
    ]
    all_confidences = [0.89, 0.75, 0.68, 0.52, 0.45]
    all_classIDs = [0, 0, 1, 0, 5]

    print("\n--- 参数组 1: CONFIDENCE=0.5 (默认) ---")
    analyzer1 = DetectionAnalyzer()
    # 所有检测都通过
    analyzer1.analyze_detection_result(all_boxes, all_confidences, all_classIDs, labels, 0.125)

    print("\n" * 2)
    print("--- 参数组 2: CONFIDENCE=0.6 (提高阈值) ---")
    analyzer2 = DetectionAnalyzer()
    # 只保留置信度 >= 0.6 的检测
    filtered_boxes = [b for b, c in zip(all_boxes, all_confidences) if c >= 0.6]
    filtered_confidences = [c for c in all_confidences if c >= 0.6]
    filtered_classIDs = [cid for cid, c in zip(all_classIDs, all_confidences) if c >= 0.6]
    analyzer2.analyze_detection_result(filtered_boxes, filtered_confidences, filtered_classIDs, labels, 0.125)

    print("\n" * 2)
    print("--- 参数组 3: CONFIDENCE=0.7 (进一步提高) ---")
    analyzer3 = DetectionAnalyzer()
    # 只保留置信度 >= 0.7 的检测
    filtered_boxes2 = [b for b, c in zip(all_boxes, all_confidences) if c >= 0.7]
    filtered_confidences2 = [c for c in all_confidences if c >= 0.7]
    filtered_classIDs2 = [cid for cid, c in zip(all_classIDs, all_confidences) if c >= 0.7]
    analyzer3.analyze_detection_result(filtered_boxes2, filtered_confidences2, filtered_classIDs2, labels, 0.125)

def main():
    """运行所有演示"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 15 + "YOLO 检测结果分析工具 - 完整演示" + " " * 15 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")

    print("本演示将展示分析工具在不同场景下的功能：")
    print("  1. 单张图片检测分析")
    print("  2. 高质量检测结果")
    print("  3. 低质量检测结果")
    print("  4. 批量检测统计")
    print("  5. 不同参数设置对比")
    print("\n按 Enter 开始演示...")
    input()

    # 运行演示
    demo_single_detection()

    input("\n按 Enter 继续下一个演示...")
    demo_high_quality_detection()

    input("\n按 Enter 继续下一个演示...")
    demo_poor_quality_detection()

    input("\n按 Enter 继续下一个演示...")
    demo_batch_analysis()

    input("\n按 Enter 继续下一个演示...")
    demo_comparison()

    print("\n" * 2)
    print("=" * 70)
    print("演示完成！")
    print("=" * 70)
    print("\n总结:")
    print("  ✅ 分析工具可以评估检测质量（优秀/良好/一般/较差）")
    print("  ✅ 提供置信度分布统计（高/中/低）")
    print("  ✅ 计算性能指标（推理时间、FPS）")
    print("  ✅ 给出针对性的优化建议")
    print("  ✅ 支持批量分析和历史对比")
    print("  ✅ 可导出 JSON 格式报告")
    print("\n当您有 yolov3.weights 文件后，可以使用:")
    print("  python3 yolo-test-with-analysis.py -i data/person.jpg")
    print("\n获取真实的检测分析结果！")
    print()

if __name__ == "__main__":
    main()
