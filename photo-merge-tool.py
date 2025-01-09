import os
import random
import logging
import argparse
from PIL import Image, ImageOps

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_image_files_from_folder(folder_path):
    """获取文件夹中的所有图片文件"""
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    try:
        files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
        if not files:
            logging.warning(f"文件夹 {folder_path} 中没有符合要求的图片文件。")
        return files
    except FileNotFoundError:
        logging.error(f"文件夹 {folder_path} 未找到！")
        raise

def get_next_output_filename(output_folder, prefix="combined_", extension=".jpg"):
    """获取下一个可用的文件名，避免覆盖"""
    try:
        existing_files = os.listdir(output_folder)
        existing_files = [f for f in existing_files if f.startswith(prefix) and f.endswith(extension)]
        
        # 如果没有任何文件，返回第一个文件名
        if not existing_files:
            return os.path.join(output_folder, f"{prefix}1{extension}")
        
        # 提取现有文件的编号并找到最大的编号
        max_num = 0
        for file in existing_files:
            try:
                num = int(file[len(prefix):-len(extension)])  # 提取文件名中的数字部分
                max_num = max(max_num, num)
            except ValueError:
                pass  # 如果无法提取数字，跳过这个文件
        
        # 返回下一个编号的文件名
        return os.path.join(output_folder, f"{prefix}{max_num + 1}{extension}")
    except Exception as e:
        logging.error(f"生成输出文件名时出错：{e}")
        raise

def merge_images_to_4_3_vertical(image1_path, image2_path, output_path, image1_offset=0):
    """
    将两张图片合并为竖版 4:3 的图片（保持完整显示并适量填充空白）
    image1_offset：第一张图片的垂直偏移量，单位：像素
    """
    try:
        target_width = 1200
        target_height = 1600  # 4:3 的竖版比例

        # 打开图片
        image1 = open_image_safely(image1_path)
        image2 = open_image_safely(image2_path)

        if not image1 or not image2:
            raise ValueError(f"图片打开失败：{image1_path} 或 {image2_path}")

        # 计算单张图片的目标大小
        half_height = target_height // 2  # 每张图片占目标图片的一半

        # 使用 ImageOps.pad 保持比例缩放并填充
        image1 = ImageOps.pad(image1, (target_width, half_height), color=(255, 255, 255))
        image2 = ImageOps.pad(image2, (target_width, half_height), color=(255, 255, 255))

        # 创建目标画布
        combined_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))

        # 第一张图片的位置（根据偏移量调整）
        combined_image.paste(image1, (0, image1_offset))  # 将第一张图片按偏移量粘贴

        # 第二张图片的位置始终固定在画布的下方
        combined_image.paste(image2, (0, image1.height))  # 第二张图片粘贴在第一张图片下方，位置固定

        # 保存结果
        combined_image.save(output_path)
        logging.info(f"合并图片已保存到：{output_path}")
    except Exception as e:
        logging.error(f"图片合并失败：{e}")
        raise

def open_image_safely(image_path):
    """尝试打开图片，捕获异常并返回 None"""
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        logging.error(f"文件 {image_path} 未找到！")
    except IOError:
        logging.error(f"无法打开文件 {image_path}！")
    return None

def generate_random_combinations(folder_path, num_images=5, image1_offset=0):
    """
    从文件夹中随机选择两张图片合并为竖版 4:3 图片
    确保每次运行时不重复使用已经使用过的图片
    """
    try:
        image_files = get_image_files_from_folder(folder_path)
        if len(image_files) < 2:
            raise ValueError(f"文件夹中的图片数量不足：{len(image_files)}，无法选择两张图片进行合并")
        
        output_folder = os.path.join(folder_path, "output")
        os.makedirs(output_folder, exist_ok=True)

        used_images = set()  # 用来记录已经使用过的图片
        remaining_images = set(image_files)  # 用来记录未使用过的图片

        for i in range(num_images):
            if len(remaining_images) < 2:
                logging.warning("剩余的图片不足两张，停止生成新的合并图像。")
                break

            # 随机选择两张图片，并确保它们没有被用过
            image1_path, image2_path = random.sample(list(remaining_images), 2)

            # 更新已使用图片和剩余图片的集合
            used_images.update([image1_path, image2_path])
            remaining_images.difference_update([image1_path, image2_path])

            # 获取下一个可用的输出文件名，避免覆盖
            output_path = get_next_output_filename(output_folder, prefix="combined_", extension=".jpg")

            # 合并图片并传入偏移量
            merge_images_to_4_3_vertical(
                os.path.join(folder_path, image1_path),
                os.path.join(folder_path, image2_path),
                output_path,
                image1_offset
            )
    except Exception as e:
        logging.error(f"生成合并图片时出错：{e}")
        raise

def combine_specific_images(folder_path, image1_name, image2_name, output_name="combined_specific.jpg", image1_offset=0):
    """
    合并指定的两张图片
    """
    try:
        output_folder = os.path.join(folder_path, "output")
        os.makedirs(output_folder, exist_ok=True)
        
        # 使用提供的输出文件名
        output_path = os.path.join(output_folder, output_name)

        merge_images_to_4_3_vertical(
            os.path.join(folder_path, image1_name),
            os.path.join(folder_path, image2_name),
            output_path,
            image1_offset
        )
    except Exception as e:
        logging.error(f"合并指定图片时出错：{e}")
        raise

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="图片合并工具")
    parser.add_argument("folder_path", type=str, help="图片文件夹路径")
    parser.add_argument("--num_images", type=int, default=5, help="生成的合并图片数量")
    parser.add_argument("--offset", type=int, default=0, help="第一张图片的偏移量")
    return parser.parse_args()

if __name__ == "__main__":
    # 解析命令行参数
    args = parse_args()
    
    # 合并指定的两张图片
    #combine_specific_images(args.folder_path, "幻灯片3.jpg", "幻灯片4.jpg", "幻灯片合并.jpg", image1_offset=args.offset)
    
    # 如果需要生成多张随机图片合并，可以取消注释以下代码
    generate_random_combinations(args.folder_path, num_images=args.num_images, image1_offset=args.offset)
