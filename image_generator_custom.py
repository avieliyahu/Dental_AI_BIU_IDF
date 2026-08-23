import cv2
import os
import numpy as np
import matplotlib.pyplot as plt # For visualization
#from tensorflow.keras.utils import to_categorical # To One-Hot-Encode the masks
from sklearn.utils import shuffle # To randomly shuffel the masks and images
import albumentations as A # For image augmentation

#def data_gen(img_folder, mask_folder, batch_size, imsize=[320,320,1], n_classes = 2, seed = 101, flip_up_down = True, flip_left_right = True, sample_weight = True):

def to_categorical(x, num_classes=None):
    """Converts a class vector (integers) to binary class matrix.

    E.g. for use with `categorical_crossentropy`.

    Args:
        x: Array-like with class values to be converted into a matrix
            (integers from 0 to `num_classes - 1`).
        num_classes: Total number of classes. If `None`, this would be inferred
            as `max(x) + 1`. Defaults to `None`.

    Returns:
        A binary matrix representation of the input as a NumPy array. The class
        axis is placed last.
    """

    x = np.array(x, dtype="int32")
    input_shape = x.shape
    # Shrink the last dimension if the shape is (..., 1).
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])

    x = x.reshape(-1)
    if not num_classes:
        num_classes = np.max(x) + 1
    batch_size = x.shape[0]
    categorical = np.zeros((batch_size, num_classes))
    categorical[np.arange(batch_size), x] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape).astype(np.float32)
    return categorical

def data_gen(img_folder, mask_folder, batch_size, imsize=[320,320,1], n_classes = 2, seed = 101, augment = True, hist_eq = False):
#def data_gen(img_folder, mask_folder, batch_size, imsize=[320,320,1], n_classes = 2, seed = 101, flip_up_down = True, flip_left_right = True, hist_eq = False):
    # Track how many pictures we used
    img_counter = 0
    # How many batches we used
    batch_num = 0
    
    # The path for the images and the masks
    imgs_path = np.sort(np.array([file for file in os.listdir(img_folder) if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".tif")]))
    #List of training images
    masks_path = np.sort(np.array([file for file in os.listdir(mask_folder) if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".tif")])) 
    #List of Mask images

    
    # Randomness
    np.random.seed(seed)
    # Shuffel both arrays in the same manner, that way the mask will always be the same as the original image
    imgs_path, masks_path = shuffle(imgs_path, masks_path)
    
    '''
    ### Testing: Make sure that every mask starts from 0 to n_classes-1

    def zero_to_n(pixel):
        return my_dict[pixel]
    ### Testing: Make sure that every mask starts from 0 to n_classes-1
    '''

    while (True):
        
        # Keep arrays to yield
        img = np.zeros((batch_size, imsize[0], imsize[1])).astype('float32')
        mask = np.zeros((batch_size, imsize[0], imsize[1])).astype('uint8')


        # Loop over every batch
        for i in range(img_counter, min(img_counter + batch_size, len(masks_path))): 
            
            # Rescale ONLY THE IMAGES
            
            if hist_eq:
                train_img = (cv2.equalizeHist(cv2.imread(os.path.join(img_folder, imgs_path[i]), cv2.IMREAD_GRAYSCALE))/255.0).astype('float32')
            else:
                train_img = (cv2.imread(os.path.join(img_folder, imgs_path[i]), cv2.IMREAD_GRAYSCALE)).astype('float32')
                                  

        
            #Image equalization
            #train_img = cv2.equalizeHist(train_img)/255.0

            # The masks are already Encoded
            train_mask = cv2.imread(os.path.join(mask_folder, masks_path[i]), cv2.IMREAD_GRAYSCALE)

            # Read an image from folder and resize (The resize function takes the arguments in reverse)
            train_img =  cv2.resize(train_img, (imsize[1], imsize[0]), interpolation = cv2.INTER_NEAREST)/255.0
            train_mask = cv2.resize(train_mask, (imsize[1], imsize[0]), interpolation = cv2.INTER_NEAREST)


            # Augmentations (added on 11/10/2025):
            if augment:
                # Declare an augmentation pipeline
                transform_image_mask = A.Compose([
                    
                    #A.RandomCrop(width= int(train_mask.shape[1] * 0.8), height= int(train_mask.shape[0]*0.8), p=1.0),
                    A.HorizontalFlip(p=0.5),
                    A.VerticalFlip(p=0.5),
                    #A.CoarseDropout(max_holes = 8, min_holes=1, max_height=0.15, min_height=0.1,max_width=0.15, min_width=0.1,
                    #                    fill_value=0, p=0.5),
    
                    A.RandomBrightnessContrast(brightness_limit=(0.1,-0.3), contrast_limit=(0.1,-0.3),p=0.7),

                    
                    A.Affine(
                    #    scale=(0.8, 1.2),      # Zoom in/out by 80-120%
                        rotate=(-25, 25),      # Rotate by -13 to +13 degrees
                    #    # translate_percent=(0, 0.1), # Optional: translate by 0-10%
                    #    # shear=(-10, 10),          # Optional: shear by -10 to +10 degrees
                        p=0.7
                    ),
                    
                ])
    
                # Augment an image
                transformed_img_mask = transform_image_mask(image=train_img, mask=train_mask)
                train_img = transformed_img_mask["image"]
                train_mask = transformed_img_mask["mask"]
                

            '''
            #Adding augmentation - Random flip
            if flip_left_right:
                if np.random.rand()>=0.5:
                    # Flip along the y axis = horizontal_flip (left becomes right and vice versa)
                    train_img = cv2.flip(train_img, 1)
                    train_mask = cv2.flip(train_mask, 1)
                    
            if flip_up_down: # Rotate 90 degrees clockwise or anti-clockwise
                if np.random.rand()>=0.5: # Flip half of the time
                    if np.random.rand()>=0.5:
                        train_img = cv2.rotate(train_img, cv2.ROTATE_90_CLOCKWISE)
                        train_mask = cv2.rotate(train_mask, cv2.ROTATE_90_CLOCKWISE)
                    else:
                        train_img = cv2.rotate(train_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                        train_mask = cv2.rotate(train_mask, cv2.ROTATE_90_COUNTERCLOCKWISE)
            '''


                    

            
            # Save the images in the array
            
            '''
            ### Testing: Make sure that every mask starts from 0 to n_classes-1
            my_dict = {} # Will map the values from each pixel value to [0 , n_classes -1]
            unique_val = np.unique(train_mask)
            for indx, val in enumerate(unique_val):
                my_dict[val]=indx
            applyall = np.vectorize(zero_to_n)
            train_mask = applyall(train_mask)
            ### Testing: Make sure that every mask starts from 0 to n_classes-1
            '''



            
            mask[i-img_counter] = train_mask
            img[i-img_counter] = train_img.astype(np.float32)

        # Add an extra dimension for the Neural Network
        #img = np.expand_dims(img,axis=-1)
        
        # Repeates the image for a 3D image
        img = np.repeat(img[:, :,:, np.newaxis], 3, axis=-1) # For Segmentation models
        #img = np.repeat(img[:, :,:, np.newaxis], 1, axis=-1)
        # One hot encode the mask
  
        mask = to_categorical(mask, num_classes=n_classes)

        
        # Take the next batch or stop if we exceed the maximal number of batches
        img_counter = min(img_counter + batch_size, len(masks_path))
        
       
        '''
        # If we want to give weights to our samples
        if sample_weight:
            weight_mat = [0.1,0.5,3]
            yield (img[0: img_counter - batch_num *batch_size ], mask[0: img_counter - batch_num *batch_size], sample_weight)
        else:
            yield (img[0: img_counter - batch_num *batch_size ], mask[0: img_counter - batch_num *batch_size])
        '''
            
        yield (img[0: img_counter - batch_num *batch_size ], mask[0: img_counter - batch_num *batch_size])
        batch_num+=1
        
        #print "randomizing again"
        if(img_counter == len(masks_path)):
            img_counter=0
            batch_num = 0
            imgs_path, masks_path = shuffle(imgs_path, masks_path)