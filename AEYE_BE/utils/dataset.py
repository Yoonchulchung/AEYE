import io

from django.db.models.fields.files import ImageFieldFile
from PIL import Image


def img_to_bytes(img_file : ImageFieldFile) -> io.BytesIO:
    buffer = io.BytesIO()
    
    try:    
        img_file.open(mode='rb')
        pil_image = Image.open(img_file)

        if pil_image.mode == 'RGBA':
            pil_image = pil_image.convert('RGB')

        pil_image.save(buffer, format="JPEG") 
        return buffer.getvalue() 
        
    except Exception as e:
        print(f"Error converting image to PIL: {e}")
        return None
    finally:
        if not img_file.closed:
            img_file.close()