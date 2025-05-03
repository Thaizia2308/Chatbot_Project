import streamlit as st
import os
from generate_munit import generate_munit_test

st.title("XML to MUnit Chatbot")
st.write("Upload your MuleSoft flow XML file:")

uploaded_file = st.file_uploader("Choose a file", type="xml")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    
    # Save uploaded file temporarily
    input_path = os.path.join("output", "uploaded_flow.xml")
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    
    # Set output file path
    output_path = os.path.join("output", "generated_munit.xml")
    
    # Generate the MUnit file
    try:
        generate_munit_test(input_path, output_path)
        st.success("MUnit test generated successfully!")

        # Show the content of generated file
        with open(output_path, "r") as f:
            st.code(f.read(), language="xml")

        # Provide download button
        with open(output_path, "rb") as f:
            st.download_button("Download MUnit Test File", f, file_name="munit_test.xml", mime="application/xml")

    except Exception as e:
        st.error(f"Error during generation: {e}")