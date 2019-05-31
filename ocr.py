import os
# imagemagik
from wand.image import Image
from wand.color import Color
# default image module
try:
    from PIL import Image as P_image
except ImportError:
    import Image as P_image
# ocr engine
import pytesseract
# opencv
import cv2


def ocr_process(filename, resolution=450, page_seg_method='3'):
    """ This function converts a PDF into images,
        preprocess them using the OpenCV module (unnecessary for formal invoice),
        and then feed them into Tesseract Ocr engine (a popular free OCR solution).

        The resolution parameter will be feed into OCR engine, so it is directly linked to the running speed.
    """
    # Create an empty string variable
    txt = ""

    # Using imagemagik module to load PDF pages and convert them into images
    all_pages = Image(filename=filename, resolution=resolution)
    for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}-{}.png'.format(image_filename, i)
            path_filename = os.path.join('converted_image', image_filename)

            # create a file in the current directory
            try:
                os.mkdir('converted_image')
            except:
                pass

            # save the image to the file
            img.save(filename=path_filename)  # save it to the output path

            # turn the image to black and white
            im = cv2.imread(path_filename)
            im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # Unnecessary for formal invoice
#             # 2. 用adaptive threshold对图像进行二值化处理
#             im_inv = cv2.adaptiveThreshold(im_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,2)

#             # 3. 进行降噪处理
#             kernel = 1/16*np.array([[1,2,1],[2,4,2],[1,2,1]])
#             im_blur = cv2.filter2D(im_inv, -1, kernel)

            # create another file to save the image
            try:
                os.mkdir('preprocessed_image')
            except:
                pass

            # save the image to preprocessed_image
            path_filename2 = os.path.join('preprocessed_image', image_filename)
            cv2.imwrite(path_filename2, im_gray)

            # Run the Tesseract OCR engine on each image and return the strings
            txt = "".join([txt, pytesseract.image_to_string(
                P_image.open(path_filename2), lang="eng",
                config='--psm ' + page_seg_method)])
    return txt


# for testing purpose only - print out ocr result
# txt = ocr_process(
#     'test_image/03-19 AvePoint Inc. Inv 106203.pdf', page_seg_method='6')

# with open("test6.txt", 'w') as file:
#     data = file.write(txt)
#     file.close()
