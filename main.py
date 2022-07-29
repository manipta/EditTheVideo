import streamlit as st
import cv2
import glob
st.markdown("<h1 style='text-align:center; color:rgb(153,242,196)'>Video Editor</h1>",unsafe_allow_html=True)
st.markdown("<p style='text-align:center'><b>Upload a mp4 file</b></p>",unsafe_allow_html=True)
u_video=st.file_uploader("",type=["mp4"])
def bw(vid,name,c,fp,speed):
    success = True
    count = 1
    f=-1
    while success:
        success,frame = vid.read()
        nam = str(count)+'.jpg'
        if success == True:
            cv2.imwrite(nam,frame)
            # print('Frame No. {} Extracted Successfully'.format(count))
            count = count+1
            f=0
        else:
            break
    if f==-1:
        st.markdown('**Some Error :|**')
        return -1
    cv_img = []
    for img in glob.glob("*.jpg"):
        if c==True:
            n= cv2.imread(img,0)
        else:
            n= cv2.imread(img)
        cv_img.append(n)
        # img=str(img)
        # cv2.imwrite(img.split("/")[-1],n)
    for img in cv_img:
        height = img.shape[0]
        width = img.shape[1]
    size = (width,height)
    if speed=='1x':
        newname="BW"+name
    elif c==1:
        newname="BW"+speed+name
    else:
        newname=speed+name
    if(c==True):
        out = cv2.VideoWriter(newname,cv2.VideoWriter_fourcc(*'MP4V'), fp, size,False)
    else:
        out = cv2.VideoWriter(newname,cv2.VideoWriter_fourcc(*'MP4V'), fp, size)
    for i in range(len(cv_img)):
        out.write(cv_img[i])
    out.release()
    st.markdown('**Converted File is:** '+newname)
    with open(newname,mode='rb') as f:
        st.download_button('Download Video', f,file_name=newname)
    return vid
    # print('Total {} Frame Extracted Successfully'.format(count-1))
    
if u_video is not None:
    name=u_video.name
    st.markdown(
                ' **Uploaded Original File** '+ ":arrow_down:"
                )
    st.markdown('**Name:** '+name)
    vid=cv2.VideoCapture(name)
    fps = vid.get(cv2.CAP_PROP_FPS)
    st.markdown('**FPS:** '+str(fps))
    st.video(u_video)
    c=st.checkbox(label="B/W")
    options=['0.25x','0.5x','1.5x','2x']
    speed=st.radio('What Speed of Video you want?',('0.25x','0.5x','1x','1.5x','2x'),2)
    with open(name,mode='wb') as f:
        f.write(u_video.read())
    if(c==True or speed in options):
        if(st.button('Save')):
            if speed==options[0]:
                fp=int((3*fps)/4)
            elif speed==options[1]:
                fp=int(fps/2)
            elif speed==options[2]:
                fp=int((3*fps)/2)
            elif speed==options[3]:
                fp=int(2*fps)
            else:
                fp=fps
            vidb=bw(vid,name,c,fp,speed)
            
    