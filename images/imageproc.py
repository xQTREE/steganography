from PIL import Image
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

original_images_names=['amusement.jpg','apple.jpg', 'flower.jpg', 'house.jpg', 'man.jpg' ]
encoded_images_names=['amusement-enc.png','apple-enc.png', 'flower-enc.png', 'house-enc.png', 'man-enc.png' ]
image_path = 'steganography\\images\\flower.jpg'  # Replace with the path to your image
image = Image.open(image_path)

# Step 2: Convert the image to a NumPy array
image_np = np.array(image)

# Step 3: Split the image into Red, Green, and Blue channels
r, g, b = image_np[:,:,0], image_np[:,:,1], image_np[:,:,2]

# Step 4: Plot overlapping histograms for each channel using seaborn
plt.figure(figsize=(8, 6))

# Red channel
sns.histplot(r.ravel(), color='red', bins=256, label='Red', alpha=0.5)

# Green channel
sns.histplot(g.ravel(), color='green', bins=256, label='Green', alpha=0.5)

# Blue channel
sns.histplot(b.ravel(), color='blue', bins=256, label='Blue', alpha=0.5)

# Add title and labels
plt.title('RGB Histogram')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')

# Show legend
plt.legend()

# Display the plot
plt.show()

original_images=[np.array(Image.open(name).convert('L')) for name in original_images_names]
encoded_images=[np.array(Image.open(name).convert('L')) for name in encoded_images_names]

original_images=[img.astype(np.float64)for img in original_images]
encoded_images=[img.astype(np.float64)for img in encoded_images]

def calculate_mse_psnr(original_image, encoded_image):
    mse=np.mean((original_image-encoded_image)**2)
    if(mse==0):
        psnr=float('inf')
    else:
        max_pixel_value=255.0
        psnr=10*math.log10(max_pixel_value**2/mse)

    return mse, psnr

mse_value=[]        
psnr_value=[]

for i in range(5):
    mse, psnr=calculate_mse_psnr(original_images[i],encoded_images[i])
    mse_value.append(mse)
    psnr_value.append(psnr)

data={
    'Image':['amusement', 'apple', 'flower', 'house', 'man' ],
    'Mse':mse_value,
    'psnr':psnr_value
}
df=pd.DataFrame(data)
print(df)