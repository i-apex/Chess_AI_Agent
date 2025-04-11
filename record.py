import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from PIL import ImageChops
from moviepy import ImageSequenceClip

frames_dir = "frames"
png_dir = "converted_frames"
video_output = "output_video.mp4"
fps = 2  # Slower video

# Function to trim white background (RGB-based)
def trim_white(img):
    img = img.convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1000x1000")

driver = webdriver.Chrome(options=chrome_options)

# Ensure PNG directory exists
os.makedirs(png_dir, exist_ok=True)

svg_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".svg")])
png_files = []

print("Rendering and cropping SVGs to PNGs...")
for i, svg in enumerate(svg_files):
    svg_path = os.path.abspath(os.path.join(frames_dir, svg))
    url = "file:///" + svg_path.replace("\\", "/")

    driver.get(url)
    screenshot_path = os.path.join(png_dir, f"frame_{i:04d}.png")
    driver.save_screenshot(screenshot_path)

    # Trim white background (not just transparent)
    img = Image.open(screenshot_path)
    cropped = trim_white(img)
    cropped.save(screenshot_path)
    png_files.append(screenshot_path)

driver.quit()

print("Creating video with lower fps...")
clip = ImageSequenceClip(png_files, fps=fps)
clip.write_videofile(video_output, codec="libx264")

print("🎥 Done! Video saved as:", video_output)
