import streamlit as st
from api_communication import upload, save_transcript
import os

# Define directories
UPLOAD_FOLDER = 'uploads'
TRANSCRIPTS_FOLDER = 'transcripts'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)

def main():
    st.title("Speech Recognition App")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "m4a"])
    
    if uploaded_file is not None:
        # Save the file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Upload file and get audio URL
        audio_url = upload(file_path)
        
        # Save transcript
        transcript_path = os.path.join(TRANSCRIPTS_FOLDER, uploaded_file.name)
        save_transcript(audio_url, transcript_path)

        # Read and display transcript
        transcript_file_path = transcript_path + '.txt'
        if os.path.exists(transcript_file_path):
            with open(transcript_file_path, 'r') as f:
                transcript_text = f.read()
            st.subheader("Transcription Result")
            st.text(transcript_text)
            
            # Download link for the transcript
            st.download_button(
                label="Download Transcript",
                data=open(transcript_file_path, "rb").read(),
                file_name=uploaded_file.name + '.txt',
                mime="text/plain"
            )
        else:
            st.error("Error in generating transcript")

if __name__ == "__main__":
    main()
