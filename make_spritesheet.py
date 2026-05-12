from PIL import Image
import os
import glob

# ===== 改这里 =====
folder = r"D:\A\pj\nakama\assets\weapon\Lightning Arrow\PNG"
output = r"D:\A\pj\nakama\assets\weapon\Lightning_Arrow.png"
# ==================

# 按文件名顺序读取所有PNG
files = sorted(glob.glob(os.path.join(folder, "*.png")))
print(f"找到 {len(files)} 张图片:")
for f in files:
    print(" ", os.path.basename(f))

frames = [Image.open(f).convert("RGBA") for f in files]

# 所有帧宽高必须一样，取第一帧的尺寸
frame_w = frames[0].width
frame_h = frames[0].height

# 创建一张横向拼接的大图
spritesheet = Image.new("RGBA", (frame_w * len(frames), frame_h))
for i, frame in enumerate(frames):
    spritesheet.paste(frame, (i * frame_w, 0))

spritesheet.save(output)
print(f"\n完成！已保存到: {output}")
print(f"spritesheet 尺寸: {spritesheet.width} x {spritesheet.height}")
print(f"帧数: {len(frames)}，每帧: {frame_w} x {frame_h}")
