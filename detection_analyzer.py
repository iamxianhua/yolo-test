#!/usr/bin/env python3
"""
YOLO 检测结果分析工具
配合 yolo-detection-analysis skill 使用
"""

import json
import time
from datetime import datetime


class DetectionAnalyzer:
    """检测结果分析器"""

    def __init__(self):
        self.results_history = []

    def analyze_detection_result(self, boxes, confidences, classIDs, labels, inference_time=None):
        """
        分析单次检测结果

        Args:
            boxes: 检测框列表
            confidences: 置信度列表
            classIDs: 类别 ID 列表
            labels: 类别标签列表
            inference_time: 推理时间（秒）
        """
        print("\n" + "=" * 60)
        print("YOLO 检测结果分析报告")
        print("=" * 60)
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # 基本统计
        total_detections = len(boxes)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        print("[基本信息]")
        print(f"  检测框数量: {total_detections}")
        print(f"  平均置信度: {avg_confidence:.2%}")

        if inference_time:
            fps = 1.0 / inference_time if inference_time > 0 else 0
            print(f"  推理时间: {inference_time*1000:.2f} ms")
            print(f"  FPS: {fps:.2f}")

        # 类别分布
        class_distribution = {}
        for cid in classIDs:
            class_name = labels[cid]
            class_distribution[class_name] = class_distribution.get(class_name, 0) + 1

        print(f"\n[检测类别分布]")
        for class_name, count in sorted(class_distribution.items(), key=lambda x: x[1], reverse=True):
            print(f"  {class_name}: {count} 个")

        # 置信度分析
        confidence_levels = {
            'high': [],      # > 0.8
            'medium': [],    # 0.5-0.8
            'low': []        # < 0.5
        }

        for i, conf in enumerate(confidences):
            if conf > 0.8:
                confidence_levels['high'].append((i, conf))
            elif conf > 0.5:
                confidence_levels['medium'].append((i, conf))
            else:
                confidence_levels['low'].append((i, conf))

        print(f"\n[置信度分布]")
        print(f"  高置信度 (>0.8): {len(confidence_levels['high'])} 个 "
              f"[{len(confidence_levels['high'])/total_detections*100:.1f}%]" if total_detections > 0 else "")
        print(f"  中等置信度 (0.5-0.8): {len(confidence_levels['medium'])} 个 "
              f"[{len(confidence_levels['medium'])/total_detections*100:.1f}%]" if total_detections > 0 else "")
        print(f"  低置信度 (<0.5): {len(confidence_levels['low'])} 个 "
              f"[{len(confidence_levels['low'])/total_detections*100:.1f}%]" if total_detections > 0 else "")

        # 详细检测列表
        print(f"\n[检测详情]")
        detections = list(zip(range(len(boxes)), boxes, confidences, classIDs))
        detections.sort(key=lambda x: x[2], reverse=True)  # 按置信度排序

        for idx, box, conf, cid in detections:
            class_name = labels[cid]
            quality = self._get_quality_label(conf)
            print(f"  #{idx+1}: {class_name:<15} 置信度: {conf:.2%}  {quality}")

        # 质量评估
        print(f"\n[质量评估]")
        self._assess_quality(confidence_levels, total_detections, avg_confidence)

        # 优化建议
        print(f"\n[优化建议]")
        self._provide_recommendations(confidence_levels, total_detections, avg_confidence, inference_time)

        # 保存到历史
        result_record = {
            'timestamp': datetime.now().isoformat(),
            'total_detections': total_detections,
            'avg_confidence': avg_confidence,
            'class_distribution': class_distribution,
            'confidence_levels': {
                'high': len(confidence_levels['high']),
                'medium': len(confidence_levels['medium']),
                'low': len(confidence_levels['low'])
            },
            'inference_time': inference_time
        }
        self.results_history.append(result_record)

        print("\n" + "=" * 60)

        return result_record

    def _get_quality_label(self, confidence):
        """获取质量标签"""
        if confidence > 0.8:
            return "✅ 优秀"
        elif confidence > 0.6:
            return "✅ 良好"
        elif confidence > 0.5:
            return "⚠️  一般"
        else:
            return "❌ 较差"

    def _assess_quality(self, confidence_levels, total, avg_conf):
        """评估整体质量"""
        high_ratio = len(confidence_levels['high']) / total if total > 0 else 0
        low_ratio = len(confidence_levels['low']) / total if total > 0 else 0

        print("  优点:")
        if high_ratio > 0.5:
            print(f"    ✅ 超过一半的检测具有高置信度 ({high_ratio*100:.1f}%)")
        if avg_conf > 0.7:
            print(f"    ✅ 平均置信度较高 ({avg_conf:.2%})")
        if low_ratio == 0:
            print(f"    ✅ 没有低置信度检测，质量稳定")

        print("\n  问题:")
        if high_ratio < 0.3:
            print(f"    ❌ 高置信度检测较少 ({high_ratio*100:.1f}%)，可能需要调整模型或参数")
        if avg_conf < 0.6:
            print(f"    ❌ 平均置信度偏低 ({avg_conf:.2%})")
        if low_ratio > 0.2:
            print(f"    ❌ 存在较多低置信度检测 ({low_ratio*100:.1f}%)，可能有误检")

        if high_ratio >= 0.5 and low_ratio == 0:
            print("\n  总体评价: 🌟 检测质量优秀")
        elif high_ratio >= 0.3 and avg_conf >= 0.6:
            print("\n  总体评价: ✅ 检测质量良好")
        elif avg_conf >= 0.5:
            print("\n  总体评价: ⚠️  检测质量一般，有改进空间")
        else:
            print("\n  总体评价: ❌ 检测质量较差，需要优化")

    def _provide_recommendations(self, confidence_levels, total, avg_conf, inference_time):
        """提供优化建议"""
        recommendations = []

        # 置信度阈值建议
        low_ratio = len(confidence_levels['low']) / total if total > 0 else 0
        high_ratio = len(confidence_levels['high']) / total if total > 0 else 0

        if low_ratio > 0.2:
            recommendations.append(
                "📌 检测到较多低置信度结果，建议提高 CONFIDENCE 阈值到 0.6-0.7 以减少误检"
            )
        elif high_ratio < 0.3 and avg_conf < 0.6:
            recommendations.append(
                "📌 整体置信度偏低，建议检查输入图像质量或考虑使用更高质量的模型"
            )

        # 性能优化建议
        if inference_time:
            if inference_time > 0.3:
                recommendations.append(
                    f"⚡ 推理时间较长 ({inference_time*1000:.0f}ms)，建议："
                    f"\n     - 减小输入尺寸 (如从 416x416 到 320x320)"
                    f"\n     - 使用 GPU 加速"
                    f"\n     - 考虑使用更轻量的模型"
                )
            elif inference_time > 0.1:
                recommendations.append(
                    f"⚡ 推理时间适中 ({inference_time*1000:.0f}ms)，如需提升："
                    f"\n     - 可尝试使用 GPU 加速"
                    f"\n     - 或适当减小输入尺寸"
                )
            else:
                recommendations.append(
                    f"✅ 推理速度优秀 ({inference_time*1000:.0f}ms)，满足实时检测需求"
                )

        # NMS 建议
        if total > 10 and avg_conf > 0.7:
            recommendations.append(
                "📌 检测数量较多且置信度高，如有重复框，可适当降低 THRESHOLD (NMS) 到 0.3"
            )

        # 输出建议
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  ✅ 当前参数配置良好，无需调整")

    def compare_with_history(self):
        """与历史记录对比"""
        if len(self.results_history) < 2:
            print("历史记录不足，无法对比")
            return

        print("\n" + "=" * 60)
        print("历史对比分析")
        print("=" * 60)

        latest = self.results_history[-1]
        previous = self.results_history[-2]

        print(f"\n最新 vs 上次:")
        print(f"  检测数量: {latest['total_detections']} vs {previous['total_detections']} "
              f"({'↑' if latest['total_detections'] > previous['total_detections'] else '↓'})")
        print(f"  平均置信度: {latest['avg_confidence']:.2%} vs {previous['avg_confidence']:.2%} "
              f"({'↑' if latest['avg_confidence'] > previous['avg_confidence'] else '↓'})")

        if latest['inference_time'] and previous['inference_time']:
            print(f"  推理时间: {latest['inference_time']*1000:.2f}ms vs {previous['inference_time']*1000:.2f}ms "
                  f"({'↓ 更快' if latest['inference_time'] < previous['inference_time'] else '↑ 更慢'})")

    def export_report(self, filename="detection_report.json"):
        """导出分析报告"""
        report = {
            'analysis_time': datetime.now().isoformat(),
            'total_analyses': len(self.results_history),
            'history': self.results_history
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n分析报告已导出到: {filename}")


# 便捷函数
def quick_analyze(boxes, confidences, classIDs, labels, inference_time=None):
    """快速分析检测结果"""
    analyzer = DetectionAnalyzer()
    return analyzer.analyze_detection_result(boxes, confidences, classIDs, labels, inference_time)


if __name__ == "__main__":
    # 示例用法
    print("YOLO 检测结果分析工具")
    print("\n使用方法:")
    print("1. 在您的检测脚本中导入此模块:")
    print("   from detection_analyzer import DetectionAnalyzer, quick_analyze")
    print("\n2. 在检测完成后调用分析函数:")
    print("   analyzer = DetectionAnalyzer()")
    print("   analyzer.analyze_detection_result(boxes, confidences, classIDs, labels, inference_time)")
    print("\n3. 或使用快速分析:")
    print("   quick_analyze(boxes, confidences, classIDs, labels, inference_time)")

    # 模拟示例
    print("\n" + "=" * 60)
    print("运行示例分析...")
    print("=" * 60)

    # 模拟检测数据
    labels = ['person', 'car', 'dog', 'bicycle']
    boxes = [[10, 20, 100, 200], [150, 50, 80, 120], [300, 100, 50, 80]]
    confidences = [0.85, 0.62, 0.48]
    classIDs = [0, 1, 0]
    inference_time = 0.15

    quick_analyze(boxes, confidences, classIDs, labels, inference_time)
