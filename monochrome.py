from PIL import Image

def convert_to_monochrome(image_path, output_path):
    image = Image.open(image_path)
    monochrome_image = image.convert(mode="L")

    monochrome_image.save(output_path)

if __name__ == "__main__":
    input_image_path = "images/input/image.png"
    output_image_path = "images/output/monochrome_image.png"
    convert_to_monochrome(input_image_path, output_image_path)
