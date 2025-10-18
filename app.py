import streamlit as st
import numpy as np
import cv2

st.set_page_config(page_title="VisionFX",page_icon="🤩")

st.title("VisionFX: A Streamlit Filter Engine")
st.subheader("Filter Your Image")

def GreyScaleImage(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img

def SmoothImage(img,intensity):
    for i in range(intensity):
        img = cv2.bilateralFilter(img,d=9,sigmaColor=75,sigmaSpace=75)
    return img

def Sketchimage(img,sketch_intensity,sketch_brightness):
    sketch_intensity = 11 + 4*(sketch_intensity)
    blur = cv2.GaussianBlur(img,(sketch_intensity,sketch_intensity),0)
    div = cv2.divide(img,blur,scale= 150 + 10*(sketch_brightness))
    sketch = cv2.cvtColor(div,cv2.COLOR_BGR2GRAY)
    return sketch

def FilterImage1(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img

def cartoonify(img,intensity,sharp_intensity,blocksize,Sketch_intensity):

        for i in range(intensity):
            img = cv2.bilateralFilter(img,d=9,sigmaColor=75,sigmaSpace=75)

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,sharp_intensity)
        edges =  cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,blockSize=blocksize,C=Sketch_intensity)
        edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

        cartoon = cv2.bitwise_and(img,edges)
        return cartoon

def VisionFx(file_upload):
    filebytes = np.frombuffer(file_upload.read(),dtype="uint8")
    image = cv2.imdecode(filebytes,1)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    Filter_img = image.copy()

    ch = st.radio("Apply Filters : ",["Original","GreyScale","Smooth","Pencil Sketch","Cartoonify","Filter1"],horizontal=True)
    if ch == "GreyScale":
        Filter_img = GreyScaleImage(Filter_img)
    elif ch == "Smooth":
        smooth_intensity = st.sidebar.slider("Smooth Intensity",min_value=1,max_value=10,value=3)
        Filter_img = SmoothImage(Filter_img,smooth_intensity)
    elif ch == "Pencil Sketch":
        brightness = st.sidebar.slider("Select Brightness :",min_value=1,max_value=10,value=8)
        sketch_intensity = st.sidebar.slider("Select Sketch Intensity :",min_value= 1 , max_value= 10,value=10)
        Filter_img = Sketchimage(Filter_img,sketch_brightness=brightness,sketch_intensity=sketch_intensity)
    elif ch == "Cartoonify":
        intensity = st.sidebar.slider("Choose Intensity of Image",min_value=1,max_value=15,value=1)
        sharp_intensity = st.sidebar.slider("Select Sharpening Intensity",min_value=1,max_value=11,value=1,step=2)
        blocksize = st.sidebar.slider("Select Blocksize",min_value=5,max_value=17,value= 17,step=2)
        Skech_intensity = st.sidebar.slider("Select Sketch Intensity",min_value=1,max_value=15,value=6)
        Filter_img = cartoonify(Filter_img,intensity,sharp_intensity,blocksize,Skech_intensity)

    elif ch == "Filter1":
        Filter_img = FilterImage1(Filter_img)

    elif ch == "Original":
        Filter_img = image.copy()

    if st.button("Detect Color") :
        txt = st.write("🖱️ Click anywhere on filtered image")
    

    col1,col2 = st.columns(2)
    with col1:
        st.write("## Original Image :")
        with st.container(border=True):
            st.image(image)  
    with col2:
        st.write("## Filtered Image :")  
        with st.container(border=True):
            st.image(Filter_img)
        
    Filter_img = cv2.cvtColor(Filter_img,cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".jpg", Filter_img)
    st.download_button("Download Filtered Image",data=buffer.tobytes(),file_name="Image.jpg",mime="image/jpeg")

ch = st.radio("Enter Your Choice : ",["Upload an Image","Take Photo"])

if ch == "Upload an Image":
    file = st.file_uploader("Upload Your Image",["jpg","png","jpeg","webp"])
    if file:
        VisionFx(file)
elif ch == "Take Photo":
    enable = st.checkbox("Enable Camera")
    file = st.camera_input("Take Your Photo",disabled=not enable)
    if file:
        VisionFx(file)