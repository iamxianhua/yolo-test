#!/usr/bin/env python3
"""
YOLO 检测脚本（带分析功能）
基于原 yolo-test.py，集成了检测结果分析
"""

import numpy as np
import cv2 as cv
import os
import time
import argparse
from detection_analyzer import DetectionAnalyzer

# YOLO 配置
yolo_dir = os.path.dirname(os.path.abspath(__file__))
weightsPath = os.path.join(yolo_dir, 'cfg/yolov3.weights')
configPath = os.path.join(yolo_dir, 'cfg/yolov3.cfg')
labelsPath = os.path.join(yolo_dir, 'cfg/coco.names')

CONFIDENCE = 0.5  # 过滤弱检测的最小概率
THRESHOLD = 0.4   # 非最大值抑制阈值


def detect_objects(image_path, confidence=CONFIDENCE, threshold=THRESHOLD, show_result=True, analyze=True):
    """
    执行物体检测

    Args:
        image_path: 图片路径
        confidence: 置信度阈值
        threshold: NMS 阈值
        show_result: 是否显示结果
        analyze: 是否进行结果分析

    Returns:
        检测结果字典
    """
    print(f"\n{'='*60}")
    print(f"开始检测: {os.path.basename(image_path)}")
    print(f"{'='*60}")
    print(f"参数: CONFIDENCE={confidence}, THRESHOLD={threshold}")

    # 检查文件是否存在
    if not os.path.exists(weightsPath):
        print(f"❌ 权重文件不存在: {weightsPath}")
        print("请运行: wget https://pjreddie.com/media/files/yolov3.weights")
        print("并将文件放置到 cfg/ 目录")
        return None

    if not os.path.exists(image_path):
        print(f"❌ 图片文件不存在: {image_path}")
        return None

    # 加载网络
    print("[INFO] 加载 YOLO 模型...")
    net = cv.dnn.readNetFromDarknet(configPath, weightsPath)

    # 加载图片
    img = cv.imread(image_path)
    if img is None:
        print(f"❌ 无法读取图片: {image_path}")
        return None

    (H, W) = img.shape[:2]
    print(f"[INFO] 图片尺寸: {W}x{H}")

    # 转换为 blob 格式
    blobImg = cv.dnn.blobFromImage(img, 1.0/255.0, (416, 416), None, True, False)
    net.setInput(blobImg)

    # 前向传播
    outInfo = net.getUnconnectedOutLayersNames()
    start = time.time()
    layerOutputs = net.forward(outInfo)
    end = time.time()
    inference_time = end - start

    print(f"[INFO] YOLO 推理时间: {inference_time:.4f} 秒 ({inference_time*1000:.2f} ms)")

    # 处理检测结果
    boxes = []
    confidences = []
    classIDs = []

    # 过滤低置信度检测
    for out in layerOutputs:
        for detection in out:
            scores = detection[5:]
            classID = np.argmax(scores)
            conf = scores[classID]

            if conf > confidence:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(conf))
                classIDs.append(classID)

    # 应用 NMS
    idxs = cv.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    # 过滤后的结果
    final_boxes = []
    final_confidences = []
    final_classIDs = []

    if len(idxs) > 0:
        for i in idxs.flatten():
            final_boxes.append(boxes[i])
            final_confidences.append(confidences[i])
            final_classIDs.append(classIDs[i])

    # 加载标签
    with open(labelsPath, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')

    print(f"\n[INFO] 检测到 {len(final_boxes)} 个物体")

    # 绘制结果
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

    if len(final_boxes) > 0:
        for i, (box, conf, classID) in enumerate(zip(final_boxes, final_confidences, final_classIDs)):
            (x, y, w, h) = box
            color = [int(c) for c in COLORS[classID]]
            cv.rectangle(img, (x, y), (x+w, y+h), color, 2)
            text = "{}: {:.2%}".format(labels[classID], conf)
            cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 保存结果图片
    output_path = image_path.replace('.jpg', '_detected.jpg').replace('.png', '_detected.png')
    cv.imwrite(output_path, img)
    print(f"[INFO] 检测结果已保存: {output_path}")

    # 显示结果
    if show_result and len(final_boxes) > 0:
        cv.imshow('YOLO Detection Result', img)
        print("\n按任意键关闭窗口...")
        cv.waitKey(0)
        cv.destroyAllWindows()

    # 分析结果
    result = {
        'image_path': image_path,
        'boxes': final_boxes,
        'confidences': final_confidences,
        'classIDs': final_classIDs,
        'labels': labels,
        'inference_time': inference_time
    }

    if analyze and len(final_boxes) > 0:
        analyzer = DetectionAnalyzer()
        analyzer.analyze_detection_result(
            final_boxes,
            final_confidences,
            final_classIDs,
            labels,
            inference_time
        )
    elif len(final_boxes) == 0:
        print("\n⚠️  未检测到任何物体")
        print("建议:")
        print("  - 降低 CONFIDENCE 阈值（当前: {:.2f}）".format(confidence))
        print("  - 检查图片是否包含 COCO 数据集中的物体")
        print("  - 尝试使用其他图片")

    return result


def batch_detect(image_dir, pattern="*.jpg", **kwargs):
    """
    批量检测目录中的图片

    Args:
        image_dir: 图片目录
        pattern: 文件匹配模式
        **kwargs: 传递给 detect_objects 的参数
    """
    import glob

    image_files = glob.glob(os.path.join(image_dir, pattern))
    print(f"\n找到 {len(image_files)} 张图片")

    results = []
    for img_path in image_files:
        result = detect_objects(img_path, show_result=False, **kwargs)
        if result:
            results.append(result)

    # 汇总统计
    if results:
        print(f"\n{'='*60}")
        print("批量检测汇总")
        print(f"{'='*60}")
        total_objects = sum(len(r['boxes']) for r in results)
        avg_time = sum(r['inference_time'] for r in results) / len(results)
        avg_confidence = sum(sum(r['confidences'])/len(r['confidences']) if r['confidences'] else 0
                           for r in results) / len(results)

        print(f"处理图片数: {len(results)}")
        print(f"检测物体总数: {total_objects}")
        print(f"平均推理时间: {avg_time*1000:.2f} ms")
        print(f"平均置信度: {avg_confidence:.2%}")
        print(f"平均 FPS: {1/avg_time:.2f}")

    return results


def main():
    parser = argparse.ArgumentParser(description='YOLO 物体检测（带分析功能）')
    parser.add_argument('-i', '--image', type=str, default='data/person.jpg',
                       help='输入图片路径')
    parser.add_argument('-c', '--confidence', type=float, default=0.5,
                       help='置信度阈值 (默认: 0.5)')
    parser.add_argument('-t', '--threshold', type=float, default=0.4,
                       help='NMS 阈值 (默认: 0.4)')
    parser.add_argument('--no-show', action='store_true',
                       help='不显示检测结果窗口')
    parser.add_argument('--no-analyze', action='store_true',
                       help='不进行结果分析')
    parser.add_argument('-b', '--batch', type=str,
                       help='批量处理目录')
    parser.add_argument('-p', '--pattern', type=str, default='*.jpg',
                       help='批量处理时的文件匹配模式')

    args = parser.parse_args()

    if args.batch:
        # 批量处理
        batch_detect(
            args.batch,
            pattern=args.pattern,
            confidence=args.confidence,
            threshold=args.threshold,
            analyze=not args.no_analyze
        )
    else:
        # 单张图片检测
        detect_objects(
            args.image,
            confidence=args.confidence,
            threshold=args.threshold,
            show_result=not args.no_show,
            analyze=not args.no_analyze
        )


if __name__ == "__main__":
    main()
