import streamlit as st

# Allow user to upload video
video = st.file_uploader(label="upload video", type="mp4", key="video_upload_file")

if(video is not None):
    st.text("video has been uploaded")
    st.write('''
    <video loop autoplay>
        <source src={video} />
    </video>
     ''')


