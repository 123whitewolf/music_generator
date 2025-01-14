from PIL import Image
import os

def extract_photo(file_path):
    photo_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]
    photos = []
    for file in os.listdir(file_path):
        file_extension = os.path.splitext(file)[1].lower()
        if file_extension in photo_extensions:
            photos.append(os.path.join(file_path, file))
    return photos
def change_photo_format(photo_list:list):
    for photo_path in photo_list:
        try:
            #Get photo name
            file_name = os.path.basename(photo_path)
           #Generate a new photo name
            new_file_name = os.path.splitext(file_name)[0]+".jpg"
            #Generate a new photo path
            new_photo_path = os.path.join(save_path,new_file_name)
            webp_image = Image.open(photo_path)
            webp_image.save(new_photo_path, "JPEG")
        except Exception as e:
            print(f"Error: {e}")
        
if __name__ =="__main__":
     file_path  = "资料\图片"
     save_path = "资料\图片"
     print(extract_photo(file_path))
     change_photo_format(extract_photo(file_path))
