import streamlit as st
from utils import generate_script

st.markdown("""
<style>
            div.stButton > button:first-child{
            background-color:#0099ff;
            color:#ffffff;
            }
            div.stButton > button:hover {
            background-color:#00ff00;
            color:#FFFFFF;
            }
            </style>            
""", unsafe_allow_html=True)

if 'API_key' not in st.session_state:
    st.session_state['API_key']=''


st.title(":video_camera: :spiral_note_pad: Youtube video script writing tool")

st.sidebar.title(":key: API Key")
st.session_state['API_key'] = st.sidebar.text_input("what is your API key", type="password")
st.sidebar.image('./streamlit-playground/youtube_script_generator/dm-high-resolution-logo.png', width=300, use_column_width=True)

# Capture user inputs
prompt = st.text_input("Please provide the topic of the video", key="prompt")
video_length = st.text_input("Expected video length in min", key="video_length")
creativity = st.slider("Words limit - (0 --> Low || 1 ---> High)", 0.0, 1.0, 0.2, step=0.1)


submit = st.button("Generate Script")

if submit:
    if st.session_state["API_key"]:
        search_result, title, script = generate_script(prompt, video_length, creativity, st.session_state["API_key"])
        st.success("Hope you like this script")

        st.subheader("Title:")
        st.write(title)

        st.subheader("Your video script :spiral_note_pad:: ")
        st.write(script)

        st.subheader("Check out - DuckDuckGo Search: ")
        with st.expander("show me"):
            st.info(search_result)
            
    else:
        st.error("Oops! please provide api key!")


