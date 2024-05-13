import streamlit as st
import speech_recognition as sr
import pyperclip

def main():
    st.title("Voice to Text Converter")

    # Function to start recording
    def start_recording():
        st.session_state.start_recording = True

    # Function to stop recording
    def stop_recording():
        st.session_state.start_recording = False

    # Reset session state
    if 'start_recording' not in st.session_state:
        st.session_state.start_recording = False

    # Record of last three statements
    if 'last_records' not in st.session_state:
        st.session_state.last_records = []

    # Display start recording button if recording hasn't started
    if not st.session_state.start_recording:
        start_button_clicked = st.button("START")
        if start_button_clicked:
            start_recording()

    # Display stop recording button if recording has started
    else:
        stop_button_clicked = st.button("STOP")
        if stop_button_clicked:
            stop_recording()

    # Recording voice and converting it to text
    if st.session_state.start_recording:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Recording...")
            audio = r.listen(source)

        # Convert audio to text
        try:
            text = r.recognize_google(audio)
            st.write("Converted Text:")
            st.text_area("Text", value=text, height=100, key="text_area")

            st.write("Recording stopped. Click 'STOP' to record again.")
            # Update the last recorded statements list
            st.session_state.last_records.append(text)
            # Maintain only the last three statements in the record
            if len(st.session_state.last_records) > 3:
                st.session_state.last_records.pop(0)

        except sr.UnknownValueError:
            st.write("Could not understand audio")
        except sr.RequestError as e:
            st.write("Could not request results; {0}".format(e))

    # Display the last three recorded statements in a table
    if st.session_state.last_records:
        st.write("Last Three Recorded Statements:")
        records_table = [[record] for record in st.session_state.last_records]
        st.table(records_table)

if __name__ == "__main__":
    main()
