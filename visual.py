#!/usr/bin/env python3

import cv2
# face detection and croping
from facenet_pytorch import MTCNN
from PIL import Image
from numpy import asarray
import torch
from imutils.video import FileVideoStream
import cv2
import time
import glob
from matplotlib import pyplot
from tqdm.notebook import tqdm
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class FastMTCNN(object):
    """Fast MTCNN implementation."""
    
    def __init__(self, stride, resize=1, *args, **kwargs):
        """Constructor for FastMTCNN class.
        
        Arguments:
            stride (int): The detection stride. Faces will be detected every `stride` frames
                and remembered for `stride-1` frames.
        
        Keyword arguments:
            resize (float): Fractional frame scaling. [default: {1}]
            *args: Arguments to pass to the MTCNN constructor. See help(MTCNN).
            **kwargs: Keyword arguments to pass to the MTCNN constructor. See help(MTCNN).
       """
        self.stride = stride
        self.resize = resize
        self.mtcnn = MTCNN(*args, **kwargs)
        
    def __call__(self, frames):
        """Detect faces in frames using strided MTCNN."""
        if self.resize != 1:
            frames = [
                cv2.resize(f, (int(f.shape[1] * self.resize), int(f.shape[0] * self.resize)))
                    for f in frames
            ]
                      
        boxes, probs = self.mtcnn.detect(frames[::self.stride])

        faces = []
        for i, frame in enumerate(frames):
            box_ind = int(i / self.stride)
            if boxes[box_ind] is None:
                continue
            for box in boxes[box_ind]:
                box = [int(b) for b in box]
                faces.append(frame[box[1]:box[3], box[0]:box[2]])
        
        return faces
    

# define our extractor
fast_mtcnn = FastMTCNN(
stride=4,
resize=0.5,
margin=14,
factor=0.6,
keep_all=True,
device=device
)
filenames = "yogesh.jpeg"
def extract_faces(fast_mtcnn,image):
    faces_detected = 0
      # Read the image
    # image = cv2.imread(filename)
        # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Detect faces using fast_mtcnn
    faces = fast_mtcnn([image_rgb])
        # Count the number of detected faces
    faces_detected += len(faces)
        
    print(f'Image:, faces detected: {len(faces)}')

    print(f'Total faces detected: {faces_detected}')
    # resize pixels to the model size
    image = Image.fromarray(faces[0])
    image = image.resize((160,160))
    face_array = asarray(image)
    print(face_array[0][0])
    return face_array


# face = extract_faces(fast_mtcnn, image)
# pyplot.imshow(face)




def applyTransform(img, message):
#    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.putText(img, message, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
    img = cv2.resize(img, (780, 540),interpolation = cv2.INTER_LINEAR)
    start = time.time()
    pixels = extract_faces(fast_mtcnn,img)
    #print(pixels[0])
    end = time.time()
    print(f"Face extraction time : {end-start} seconds")
    # print(pixels)
    pyplot.imshow(pixels)
    # embedder = FaceNet()
    # print(embedder.embeddings(pixels))
    # cv2.imshow("Video", pixels)
    # cv2.waitKey(1)



# extract a single face from a given photograph


# load the photo and extract the face

