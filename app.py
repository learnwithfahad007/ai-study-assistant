import streamlit as st
from utils import summarize_text, generate_mcqs, make_flashcards
from PyPDF2 import PdfReader


st.title('AI Study Assistant — Summarize, MCQs, Flashcards')


uploaded = st.file_uploader('Upload PDF (optional)', type=['pdf'])
text_input = st.text_area('Or paste text here')


text = ''
if uploaded is not None:
    try:
        reader = PdfReader(uploaded)
        pages = [p.extract_text() or '' for p in reader.pages]
        text = '\n'.join(pages)
    except Exception as e:
        st.error('Could not read PDF: ' + str(e))


if not text:
    text = text_input


if st.button('Generate'):
    if not text or len(text.strip()) < 30:
        st.warning('Please provide longer text (PDF or paste).')
    else:
        st.subheader('Summary')
        st.write(summarize_text(text, num_sentences=4))

        st.subheader('MCQs')
        for i, mcq in enumerate(generate_mcqs(text, num_q=5)):
            st.write(f"**Q{i+1}.** {mcq['question']}")
            for j, opt in enumerate(mcq['options']):
                st.write(f"- {chr(65+j)}. {opt}")
            with st.expander('Show answer'):
                st.write(mcq['answer'])

        st.subheader('Flashcards')
        for f in make_flashcards(text, num=8):
            with st.expander(f['q']):
                st.write(f['a'])

st.write('You can now view your Streamlit app in your browser.')
st.write('  Local URL: http://localhost:8501')
