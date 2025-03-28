import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np

def augment_images(input_dir, output_dir, target_count):
    os.makedirs(output_dir, exist_ok=True)
    
    existing_images = os.listdir(input_dir)
    current_count = len(existing_images)
    
    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    for img_file in existing_images:
        if img_file.startswith('.') or not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        img_path = os.path.join(input_dir, img_file)
        img = Image.open(img_path)
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = img_array.reshape((1,) + img_array.shape)
        
        i = 0
        for batch in datagen.flow(img_array, batch_size=1, save_to_dir=output_dir, save_prefix='aug', save_format='jpeg'):
            current_count += 1
            i += 1
            if current_count >= target_count or i > 5:
                break


augment_images('train/lavender', 'train/augmented/lavender', 400)
augment_images('train/snowdrop', 'train/augmented/snowdrop', 400)

print("Success")
