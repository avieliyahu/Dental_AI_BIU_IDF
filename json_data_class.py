import cv2 # For adding polygons to images
import numpy as np # For math
import matplotlib.pyplot as plt # For visualization
import os # For working with directories
import json # For reading JSON files
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter import Tk

'''import matplotlib as mpl
fig_size = (17,10)
mpl.rcParams['figure.figsize'] = (17,10)'''

class JSON_data():
    '''
    This class will help with reading the various JSON files that the dentists will provide.
    
    Methods:
        choose_images(img_path:str)->str
        save_annotatios_mask(img_path:str, mask_path:str)
        plot_image(img_path:str, mask:str = True, bbox:str = True)
        
    '''
    
    def __init__(self, color_dict):
        
        '''self.color_dict = {'Tooth':(1,1,1), 'Bone':(2,2,2), 'Restoretion':(3,3,3),
                          'Caries':(4,4,4), 'Caries secondary':(5,5,5), 'Endodontia':(6,6,6), 'Pulp':(7,7,7), 'Crown':(8,8,8)}'''
        self.color_dict = color_dict
    
    def choose_images(self,img_path:str) -> str:
        '''
        Choose images to show, and return the file path
        
        Input:
            img_path:str - The path to the images folder
            
        Output:
            files_path:str - The files path for each image
        '''
        root = Tk()
        root.withdraw()
        # To show the dialog at the front, we need both:
        # 1: root.wm_attributes('-topmost', 1)
        root.wm_attributes('-topmost', 1)
        # 2: parent = root 
        files_path = askopenfilenames(parent=root, initialdir = img_path,
                                      title= 'Choose the images you want to see',\
                                      filetypes=[("Images", ".jpg .png .tif")])
        # show an "Open" dialog box and return the path to the selected file
        return(files_path)
    
    def save_annotatios_mask(self, img_path:str, mask_path:str):
        '''
        Takes a JSON annotation from labelme, extracts the data and save the mask.
        train_val_test - String, wheter the data is from train, test or val.
        
        Input:
            img_path:str - The path to the images folder.
            mask_path:str - The path to the masks folder.
            
        Output:
            None, saves the annotations.
        '''
        
        # Choose the images directory
        os.chdir(img_path)
        
        # Find all the JSON files
        json_path =[]
        for file in os.listdir():
            if (file.endswith(".json")):
                json_path.append(file)
        
        if len(json_path): # If there are json files in the folder, continue
            '''if type(img_path) == str:
                img_path = [img_path] # Make sure that we have a list, for the loop'''
            
            # Check if all the directories are present, if not create them:
            if not os.path.exists(mask_path):
                os.mkdir(mask_path)
            
            for annot in json_path: # Read every file in the path,
                with open(annot, encoding="utf8") as my_file: # Open each JSON file
                    my_data = json.load(my_file) # Takes the actual data
    
                    # The keys we're interesed in my_data are:
                    # 'shapes' - Has the labels and coordinates, it's a list of dictionaries with 2 important keys:
                        # 'label' - Says which label the annotation is
                        # 'points' - Takes the coordinates
                    # 'imagePath' - Shows the image path
                    # 'imageHeight' & 'imageWidth' - For obvious reasons
                    # 'imageData' - I don't really know how to extract the data, maybe I should drop it
                    
    
                    # Get the coordinates and labels for each annotation:
                    coord, labels = [],[]
                    for data_point in my_data['shapes']:
                        # Make sure we're only looking for labels from the labels dictionary
                        if data_point['label'] in self.color_dict:
                            labels.append(data_point['label'])
                            coord.append( np.reshape(data_point['points'],(-1,2)) )  # Takes all the coordinates in a 2d array  
                        
                    # Making a blank image for the mask
                    
                    # Using the JSON dimensions is unreliable, we should use the images' dimension
                    mask_img = np.zeros((my_data['imageHeight'],my_data['imageWidth'],1)) 
                    #img_shape = cv2.imread(annot.replace('json','tif')).shape[:2]
                    #mask_img = np.zeros((img_shape[0], img_shape[1] ,1))
                        
                    ''' # We have a problem with overlapping annotations: which annotatiob should be painted first?
                    # My logic says that the bigger annotation should be the first, and then the smaller ones, so we won't
                    # Get a situation where we don't annotate caries because we them annotated the tooth on top of it.
                    
                    # Sort the labels, make sure that 'tooth' (The largest) is first.
                    labels = np.array(labels)
                    coord = np.array(coord,dtype=object)
                    
                    labels_indx = np.argsort(labels, axis=-1, kind=None, order=None)[::-1] # Reverse order, tooth first
                    labels = labels[labels_indx]
                    coord = coord[labels_indx]
                    '''
                    for pnt_num, point in enumerate (coord): # A
                        
                        '''
                        # 1) If there IS an if statement, use this code
                        
                        if not (labels[pnt_num] == 'Furcation lesion' or labels[pnt_num] =='Lesion' or 
                                labels[pnt_num] == 'Orthodontic retainer' or labels[pnt_num] == 'Implant'):
                                
                                
                        #if labels[pnt_num] =='Tooth' or  labels[pnt_num] =='Bone':
                        #if labels[pnt_num] =='Caries' or labels[pnt_num] =='Tooth filling' or  labels[pnt_num] =='Secondary caries' or  labels[pnt_num] =='Bone loss':
                        #if labels[pnt_num] =='Tooth filling':
                        if labels[pnt_num] =='Crown':
                        
                        

                        
                       
                            print('Remove the if and the indentation at line 122!!!')
                            
                            vertices = np.array(point,np.int32) # cv2 requires int32 points
                            pts = vertices.reshape(-1,1,2) # cv2 requires this format

                            # Mask
                            cv2.fillPoly(mask_img,[pts],color=self.color_dict[labels[pnt_num]]) # Adds the polygon to the original image
                        
                        # 1) If there IS an if statement, use this code
                        '''
                        
                        #'''
                        #2) If there IS NO condition, use this part
                        
                        vertices = np.array(point,np.int32) # cv2 requires int32 points
                        pts = vertices.reshape(-1,1,2) # cv2 requires this format

                        # Mask
                        cv2.fillPoly(mask_img,[pts],color=self.color_dict[labels[pnt_num]]) # Adds the polygon to the original image
                        
                        #2) If there IS NO condition, use this part
                        #'''
                    new_file_name = annot.replace('.json','.png') # Change from json to png
                    new_file_name = new_file_name.replace('Image','Mask') # Change from Image to Mask
                    file_name = os.path.join(mask_path, new_file_name)
                    cv2.imwrite(filename=file_name, img=mask_img)
                    '''print(coord)
                    print()
                    print(labels)'''
                
        else: # If there are no JSON files
            print('No JSON data files in directory!')
    
    def save_bbox(self, img_path:str, bbox_path:str):
        '''
        Takes a JSON annotation from labelme, extracts the data and saves a bounding box as a YOLO format
        train_val_test - String, wheter the data is from train, test or val.
        Input:
            img_path:str - The path to the images folder.
            bbox_path:str - The path to the bounding boxes folder.

        Output:
            None, saves the annotations.
        '''
        os.chdir(img_path)
        
        # Find all the JSON files
        json_path =[]
        for file in os.listdir():
            if (file.endswith(".json")):
                json_path.append(file)
        
        if len(json_path): # If there are json files in the folder, continue
            if type(img_path) == str:
                img_path = [img_path] # Make sure that we have a list, for the loop
            
            # Check if all the directories are present, if not creat them:                            
                                  
            if not os.path.exists(bbox_path):
                os.mkdir(bbox_path)
   
    
            for annot in json_path: # Read every file in the path
                YOLO_text = os.path.join(bbox_path, annot.replace('json','txt'))
                with open(annot, encoding="utf8") as my_file: # Open each JSON file
                    my_data = json.load(my_file) # Takes the actual data
    
                    # The keys we're interesed in my_data are:
                    # 'shapes' - Has the labels and coordinates, it's a list of dictionaries with 2 important keys:
                        # 'label' - Says which label the annotation is
                        # 'points' - Takes the coordinates
                    # 'imagePath' - Shows the image path
                    # 'imageHeight' & 'imageWidth' - For obvious reasons
                    # 'imageData' - Can extract the data using labelme.utils.img_b64_to_arr
    
                    # Get the coordinates and labels for each annotation:
                    coord, labels = [],[] # Save the coordinates & labels
                    for data_point in my_data['shapes']:
                        labels.append(data_point['label'])
                        coord.append( np.reshape(data_point['points'],(-1,2)) )  # Takes all the coordinates in a 2d array
    
                    # Making a blank image for the mask
                    bb_img = np.zeros((my_data['imageHeight'],my_data['imageWidth'])) # For bounding box
                    
                    # For bounding box, checks if a txt file exists, if so delete it
                    if os.path.exists(YOLO_text):
                            os.remove(YOLO_text)
                    for pnt_num, point in enumerate (coord):
                        vertices = np.array(point,np.int32) # cv2 requires int32 points
       
                        # Make bounding box
                        pt1 = (vertices[:,0].min(),vertices[:,1].min())
                        pt2 = (vertices[:,0].max(),vertices[:,1].max())
                       
                        
                        # YOLO format: Class, x (center), y (center), width, height
                        with open(YOLO_text,mode='a') as YOLO:
                            
                            
                            YOLO.write(str(self.color_dict[labels[pnt_num]][0]-1) + ' '+
                                       str((pt1[0]+pt2[0])/(2*my_data['imageWidth'])) + ' ' +
                                       str((pt1[1]+pt2[1])/(2*my_data['imageHeight'])) + ' ' + 
                                       str((pt2[0]-pt1[0])/my_data['imageWidth']) + ' ' + 
                                       str((pt2[1]-pt1[1])/my_data['imageHeight'])+'\n')

                            
                            #YOLO.write('0 '+
                            #           str((pt1[0]+pt2[0])/(2*my_data['imageWidth'])) + ' ' +
                            #           str((pt1[1]+pt2[1])/(2*my_data['imageHeight'])) + ' ' + 
                            #           str((pt2[0]-pt1[0])/my_data['imageWidth']) + ' ' + 
                            #           str((pt2[1]-pt1[1])/my_data['imageHeight'])+'\n')

        else:
            print('No JSON data files in directory!')
            
    
    def plot_image(self,img_path:str, mask:str = True, bbox:str = True):
        '''
        Plots the images with the annotations
        
        Input - 
                img_path:str - The path of the images
                mask:str - Wheter or not to plot the polygons
                bbox:str - Wheter or not to plot the bounding boxes
                
        Output - None, plots the image
        
        
        
        '''
        # First, take the image path
        files_path = self.choose_images(img_path)
        
        for file_num, file_path in enumerate(files_path):
            # Change the directory to the image's
            os.chdir(os.path.dirname(file_path))
            # Take only the filename
            filename = file_path[len(os.getcwd())+1:]
            data_json = filename[:filename.find('.')]+'.json'
            
            
            if data_json in os.listdir(): # If there are json files in the folder, continue
                with open(data_json, encoding="utf8") as my_file: # Open each JSON file
                    my_data = json.load(my_file) # Takes the actual data
    
                    # The keys we're interesed in my_data are:
                    # 'shapes' - Has the labels and coordinates, it's a list of dictionaries with 2 important keys:
                        # 'label' - Says which label the annotation is
                        # 'points' - Takes the coordinates
                    # 'imagePath' - Shows the image path
                    # 'imageHeight' & 'imageWidth' - For obvious reasons
                    # 'imageData' - I don't really know how to extract the data, maybe I should drop it
                    
                    
                    
                    coord, labels = [],[] # Save the coordinates & labels
                
                    for indx, data_point in enumerate(my_data['shapes']):
                        labels.append(data_point['label'])
                        coord.append( np.reshape(data_point['points'],(-1,2)) )  # Takes all the coordinates in a 2d array            
                        # Making a blank image for the mask
                        mask_img = np.zeros((my_data['imageHeight'],my_data['imageWidth'],1)) 
                        
                    # Sort the labels, make sure that 'tooth' (The largest) is first.
                    labels = np.array(labels)
                    coord = np.array(coord,dtype=object)
                    
                    labels_indx = np.argsort(labels, axis=-1, kind=None, order=None)[::-1] # Reverse order, tooth first
                    labels = labels[labels_indx]
                    coord = coord[labels_indx]
                    
                    my_img = cv2.imread(files_path[file_num],cv2.IMREAD_COLOR)            
                    if mask:
                            
                        my_img = cv2.cvtColor(my_img, cv2.COLOR_BGR2RGB)
        
                        # Making a blank image for the mask
                       # mask_img = np.zeros((my_data['imageHeight'],my_data['imageWidth'])) 
                        
                    if bbox:
                        # Annotate an image:
                        my_img2 = np.copy(my_img)
        
                        # Making a blank image for the mask
                    #    bb_img = np.zeros((my_data['imageHeight'],my_data['imageWidth'])) # For bounding box
                    
                    
                    
                    for pnt_num, point in enumerate (coord): # A
                            vertices = np.array(point,np.int32) # cv2 requires int32 points
                            pts = vertices.reshape(-1,1,2) # cv2 requires this format

                            # Mask
                            cv2.fillPoly(mask_img,[pts],color=self.color_dict[labels[pnt_num]]) # Adds the polygon to the original image
                    
                    
                            if mask:
                                    # Add the polygon & Text:
                                    # 1) Original image
                                    cv2.polylines(my_img,[pts],isClosed=True ,color=self.color_dict[labels[pnt_num]], thickness=2)
                                    # Adds the polygon to the original image


                                    font = cv2.FONT_HERSHEY_SIMPLEX
                                    cv2.putText(my_img,text=labels[pnt_num],
                                                org=(vertices[:,0].min(),vertices[:,1].min()),fontFace=font,
                                                fontScale= 1 ,color=self.color_dict[labels[pnt_num]], thickness=1 ,lineType=cv2.LINE_AA)

                                        # 2) Mask
                                  #cv2.fillPoly(mask_img,[pts],color=(255,0,0)) # Adds the polygon to the original image
                            if bbox:
                                # Bounding box:

                                # Make bounding box
                                pt1 = (vertices[:,0].min(),vertices[:,1].min())
                                pt2 = (vertices[:,0].max(),vertices[:,1].max())

                                # 1: Original image
                              #  cv2.rectangle(img=bb_img,pt1=pt1, pt2=pt2,color=(255,0,255),thickness=1)

                                # 2: Mask image
                                cv2.rectangle(img=my_img2,pt1=pt1, pt2=pt2,color=self.color_dict[labels[pnt_num]],thickness=2)

                    
                    
                    if mask:
                        '''
                        plt.figure()
                        plt.imshow(mask_img)
                        plt.title('Segmentation: '+ data_json)
                        '''
                        plt.figure()
                        plt.imshow(my_img)
                        plt.title('Segmentation: '+ data_json)
                    if bbox:
                        '''
                        plt.figure()
                        plt.imshow(bb_img)
                        plt.title('Bounding box: '+ data_json)
                        '''
                        plt.figure()
                        plt.imshow(my_img2)
                        plt.title('Bounding box: '+ data_json)
    
            else:
                print('No JSON data files in directory!')

        
