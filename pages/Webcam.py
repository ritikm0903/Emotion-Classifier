import cv2
import streamlit as st
from deepface import DeepFace
import time

import streamlit.components.v1 as components
from PIL import Image

st.components.v1.html("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Camera Emotion Capture</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: left;
            align-items: left;
            height: 100vh;
            margin: 10px;
            background-color:rgb(14, 17, 23) ;
           
          }

          #camera-container {
            display: flex;
            align-items: center;
          }

          #camera {
            margin-bottom: 33px;
            width: 100px;
            height: 100px;
            position: relative;
            margin-right: 20px;
          }

          #camera img {
            width: 100%;
            height: 100%;
          }

          #lens {
            width: 20px;
            height: 20px;
            background-color: #fff;
            border-radius: 50%;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
          }

          #emotions {
            font-size: 22px;
            transform: scale(1.5);
            font-weight: bold;
            color: #333;
        }

        #emotion-text {
            font-size: 16px;
            text-align: center;
            color: #333;
            margin-top: 5px;
        }
        </style>
        <script>
            window.onload = function() {
              const emotions = ["😐", "😃", "😢", "😠", "😲", "😍"];
              let index = 0;

              function changeEmotion() {
                index = (index + 1) % emotions.length;
                document.getElementById('emotions').innerText = emotions[index];
                document.getElementById('emotion-text').innerText = getEmotionText(emotions[index]);
                setTimeout(changeEmotion, 1000);
              }

              function getEmotionText(emotion) {
                switch(emotion) {
                  case "😐":
                    return "Neutral";
                  case "😃":
                    return "Happy";
                  case "😢":
                    return "Sad";
                  case "😠":
                    return "Angry";
                  case "😲":
                    return "Surprised";
                  case "😍":
                    return "In Love";
                  default:
                    return "Unknown";
                }
              }

              changeEmotion();
            }
          </script>
        </head>
        <body>

        <div id="camera-container">
  <div id="camera">
        <img src="https://static.gameloop.com/img/d50dfdfd520653389a47e87016a21863.png?imageMogr2/thumbnail/172.8x172.8/format/webp" alt="Online Image">

  </div>

          <div>
            
            <div id="emotions">😐</div>
            <div id="emotion-text" style="color:white;">Neutral</div>
          </div>
        </div>

        </body>
        </html>
    """, height=100)


def redirect(url):
    """Create a JavaScript function to redirect the user to the specified URL."""
    return f"""
    <script>
        window.location.href = "{url}";
    </script>
    """


# Function to analyze facial attributes using DeepFace
def analyze_frame(frame):
    result = DeepFace.analyze(img_path=frame, actions=['emotion'], enforce_detection=False, detector_backend="opencv", align=True, silent=True)
    return result
def overlay_text_on_frame(frame, texts):
    overlay = frame.copy()
    alpha = 0.9  # Adjust the transparency of the overlay
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 100), (255, 255, 255), -1)  # White rectangle
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    text_position = 15 # Where the first text is put into the overlay
    for text in texts:
        cv2.putText(frame, text, (10, text_position), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        text_position += 20

    return frame
def facesentiment():
    stframe = st.image([])  # Placeholder for the webcam feed

    # Add start/stop button
    is_camera_on = False
    button_start = st.button("Start Camera")
    button_stop = st.button("Stop Camera")

    # Flag to track if 'SAD' emotion has been detected before
    sad_emotion_detected_before = False

    while True:
        if button_start:
            is_camera_on = True
            cap = cv2.VideoCapture(0)  # Initialize the camera
            button_start = False  # Reset the button state

        if button_stop:
            is_camera_on = False
            button_stop = False  # Reset the button state

        if not is_camera_on:
            stframe.empty()  # Clear the frame
            continue

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Analyze the frame using DeepFace
        result = analyze_frame(frame)

        # Extract the face coordinates
        face_coordinates = result[0]["region"]
        x, y, w, h = face_coordinates['x'], face_coordinates['y'], face_coordinates['w'], face_coordinates['h']

        # Draw bounding box around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = f"Emotion: {result[0]['dominant_emotion']}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Check if 'dominant_race' key exists in the result dictionary
        # if 'dominant_race' in result[0]:
        #     text_race = f"Race: {result[0]['dominant_race']}"
        #     cv2.putText(frame, text_race, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        # Convert the BGR frame to RGB for Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        texts = [
            f"Face Confidence: {round(result[0]['face_confidence'], 3)}",
            # f"Race: {result[0]['dominant_race']}",
            f"Dominant Emotion: {result[0]['dominant_emotion']} {round(result[0]['emotion'][result[0]['dominant_emotion']], 1)}",
        ]

        frame_with_overlay = overlay_text_on_frame(frame_rgb, texts)

        # Display the frame in Streamlit
        stframe.image(frame_rgb, channels="RGB")

        # Check if the detected emotion is 'SAD'
        if result[0]['dominant_emotion'] == 'sad' and not sad_emotion_detected_before:
            st.write("Sad emotion detected. Please fill out the form provided below.")
            components.html(redirect("http://localhost:8501/form"))
            sad_emotion_detected_before = True

        # Release the camera when stop button is clicked
        if button_stop:
            cap.release()  # Release the camera
            break
#  Image tag  in  the Webcam <img src="		http://localhost:8503/media/ad4cc0e42c6c55b0fc7dd1b8ccaa640a1b629b2504a8354687811a25.png" alt="Camera Icon">
   
def main():
    # Face Analysis Application #
    # st.title("Real Time Face Emotion Detection Application")
    activities = ["Webcam Face Detection", "About"]
    choice = st.sidebar.selectbox("Select Activity", activities)
    st.sidebar.markdown(
        """""")
    if choice == "Webcam Face Detection":
        html_temp_home1 = """<div style="background-color:#6D7B8D;padding:10px">
                                            <h4 style="color:white;text-align:center;">
                                            Real time face emotion recognition of webcam feed using OpenCV, DeepFace and Streamlit.</h4>
                                            </div>
                                            </br>"""
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        facesentiment()
    

    elif choice == "About":
        st.subheader("About this app")

        html_temp4 = """   
                     
<div>

<p>DeepFace is the facial recognition system used by Facebook for tagging images. It was proposed by researchers at Facebook AI Research (FAIR) at the 2014 IEEE Computer Vision and Pattern Recognition Conference (CVPR). </p>

  <div>
  <p>In modern face recognition there are 4 steps:  </p>
   <ul>
    <li>Detect</li>
    <li>Align</li>
    <li>Represent</li>
    <li>Classify</li>
   </ul>
  </div>

  <p>
   This approach focuses on alignment and representation of facial images. We will discuss these two part in detail. 
  </p>

  <div>
  <h1>Alignment:</h1>
  <p>The goal of this alignment part is to generate frontal face from the input image that may contain faces from different pose and angles. The method proposed in this paper used 3D frontalization of faces based on the fiducial (face feature points) to extract the frontal face. The whole alignment process is done in the following steps: </p>

   <ul>
    <li>Given an input image, we first identify the face using six fiducial points. These six fiducial points are 2 eyes, tip of the nose and 3 points on the lips. These feature points are used to detect faces in the image. 
    </li>
        <img src="https://media.geeksforgeeks.org/wp-content/uploads/20200313163045/step14.png" alt="pic1"/>

   </ul>

   <ul>
    <li>In this step we generate the 2D-face image cropped from the original image using 6 fiducial points.  
    </li>
        <img src="https://media.geeksforgeeks.org/wp-content/uploads/20200313163516/step28.png" alt="pic1"/>
        </br>

   </ul>

   <ul>
    <li>In the third step, we apply the 67 fiducial point map with their corresponding Delaunay Triangulation on the 2D-aligned cropped image. This step is done in order to align the out of plane rotations. In this step, we also generate a 3D-model using a generic 2D to 3D model generator and plot 67 fiducial points on that manually. 
    </li>
        <img src="https://media.geeksforgeeks.org/wp-content/uploads/20200313170455/step36.png" alt="pic1"/>
        <p>67 fiducial points with Delaunay triangulation</p>
        </br>

   </ul>

   <ul>
   <p></p>
        <img src="https://media.geeksforgeeks.org/wp-content/uploads/20200313173414/step3b.png" alt="pic1"/>
        <p>3D shape generated from the align 2D-crop image</p>
        </br>
   </ul>

   <ul>
   <p></p>
           <img src="https://media.geeksforgeeks.org/wp-content/uploads/20200313173616/visibility1.png" alt="pic1"/>
        <p>Visibility map of 2D shape in 3D (darker triangles are less visible as compared to light triangles)</p>
      </br>
   </ul>

   <li>Then we try to establish a relation between 2D and 3D using given relation 
   </br>
   <h3> X2d = X3d\P </h3>
   <p>which can be calculated by the following relation:</p>
   <h4>loss\left ( \p\right ) = r^sum r  </h4>

   <p>and ∑        is a covariance matrix and dimensions of (67 x 2) x (67 x 2), X3d        is (67 x 2) x 8 and        [Tex]\overrightarrow{P}        [/Tex] has dimensions of (2 x 4). We are using Cholesky decomposition to convert that loss function into ordinary least square. </p>

           
   </li>
<img src="https://media.geeksforgeeks.org/wp-content/uploads/20200316171612/67_ficudial_point_mapping.png" alt="pic1"/>

<p>67 fiducial point mapping on 2D-3D affine face.</p>


  </div>

  <div>
   <h2>Representation and Classification Architecture: </h2>
   <p>
   </br>
   DeepFace is trained for multi-class face recognition i.e. to classify the images of multiple peoples based on their identities. 
It takes input into a 3D-aligned RGB image of 152*152. This image is then passed the Convolution layer with 32 filters and size 11*11*3 and a 3*3 max-pooling layer with the stride of 2. This is followed by another convolution layer of 16 filters and size 9*9*16. The purpose of these layers to extract low-level features from the image edges and textures. </br>

The next three layers are locally connected layers, a type of fully connected layer that has different types of filters in a different feature map. This helps in improving the model because different regions of the face have different discrimination ability so it is better to have different types of feature maps to distinguish these facial regions.
   </p>
<img src="https://media.geeksforgeeks.org/wp-content/uploads/20200316180536/deepface-representation-architectutre.png" alt="pic1" style="width:950px;" />

</br></br>
<p>The last two layers of the model are fully connected layers. These layers help in establishing a correlation between two distant parts of the face. Example: Position and shape of eyes and position and shape of the mouth. The output of the second last fully connected layer is used as a face representation and the output of the last layer is the softmax layer K classes for the classification of the face. </br> </br>
The total number of parameters in this network is 120 million approximately with most of them (~95%) comes from the final fully connected layers. The interesting property of this network is the feature map/vector generated during the training of this model amazingly sparse. For Example, 75% of the values in topmost layers is 0. This may be because of this network uses ReLU activation function in every convolution network which is essentially max(0, x). This network also uses Drop-out Regularization which also contributed to sparsity. However, Dropout is only applied to the first fully connected layer. </br> </br>
In the final stages of this network, we also normalize the feature to be between 0 and 1. This also reduces the effect of illumination changes across. We also perform an L2-regularization after this normalization. </p>
  </div>

  <div>
  <h2>Verification Metric: </h2>
  </br>
  <p>We need to define some metric that measures whether two input images belong to the same class or not. There are two methods: supervised and unsupervised with supervised having better accuracy than unsupervised. It is intuitive because while training on particular target dataset one is able to improve the accuracy by fine-tuning the model according to it. For Example, Labeled Faces in the Wild (LFW) dataset has 75% of faces are male, training on LFW may introduce some bias and add some generalization which is not suitable while testing on other face recognition datasets. However, training using a small dataset may reduce generalization when used on other datasets. In these cases, the unsupervised similarity metric is better. This paper uses the inner product of two feature vectors generated from representation architecture for unsupervised similarity. This paper also uses two supervised verification metrics. These are 

</p>
  </div>


  <div>
   <h1>Training and Results </h1> </br>
   <p>DeepFace is trained and experimented on the following three datasets </p>
   <ul>
    <li> SFC dataset: </li>
    </br>
    <p>This is the dataset generated by Facebook itself. It contains nearly 4.4 million images of 4030 peoples each having 800 to 1200 face images. For the testing purpose, they take 5% most recent images from each class. The model is trained using a standard feed-forward network with SGD with momentum = 0.9, batch size = 128 and the learning rate is the same for all the layer i.e 0.01. 
The model is trained on three subsets of dataset 1.5k people (1.5 M images), 3k people (3.3 M images) and 4k people (4.4 M images). The classification error rate on these subsets are 7%, 7.2% and 8.7% respectively. </p>

</br>
   
   
   </ul>
  </div>

  
</div>

                                  
       """

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        pass
      
    
# Open the image
image = Image.open('images/VC1.png')

# Resize the image to desired dimensions (e.g., 300x300)
resized_image = image.resize((100, 100))

# Display the resized image
# st.image(resized_image)      

if __name__ == "__main__":
    main()