import numpy as np
import png
import pydicom

# from https://github.com/pydicom/pydicom/issues/352#issuecomment-406767850

def dicom2png(path):
    ds = pydicom.dcmread(path)

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    # Write the PNG file
    with open(path + '.png', 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)

    return path + '.png'

if __name__ == '__main__':
    path = 'Dicoms/144265'
    print(dicom2png(path))
