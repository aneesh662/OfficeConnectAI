import streamlit as st
from fpdf import FPDF
import tempfile
import google.generativeai as genai
import pandas as pd

# Configure Google Generative AI
genai.configure(api_key="AIzaSyC_t0wvmafmoDMQMBRWXN0fpdUIrdi2NXI")
model = genai.GenerativeModel("gemini-1.5-flash")

def sanitize_text(text):
    """Sanitize text to remove non-latin characters."""
    return text.encode("latin-1", "replace").decode("latin-1")

def export_to_pdf(response_text):
    """Export AI response to a PDF with proper encoding."""
    sanitized_text = sanitize_text(response_text)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="ADI AI", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=sanitized_text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        return tmpfile.name

def load_backend_csv():
    """Load the predefined backend CSV file."""
    csv_path = "backend_data.csv"  # Path to the CSV file
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        st.error("Backend CSV file not found.")
        return None
    except Exception as e:
        st.error(f"Error loading backend CSV file: {e}")
        return None

# Hide all Streamlit branding and default elements
#hide_st_style = """
   # <style>
    #MainMenu {visibility: hidden !important;} /* Hides the hamburger menu */
   # header {visibility: hidden !important;}    /* Hides the header */
   # footer {visibility: hidden !important;}    /* Hides the footer */
   # .stApp {margin-top: -50px;}                /* Adjusts spacing after hiding the header */
   # [data-testid="stDecoration"] {visibility: hidden !important;} /* Hides Streamlit branding */
   # .viewerBadge_container__1QSob {display: none !important;}    /* Hides footer badge */
   # .stFooter {visibility: hidden !important;} /* Hides the footer section */
   # .css-14xtw13 {visibility: hidden !important;} /* Additional footer class */
   # </style>
#"""
#st.markdown(hide_st_style, unsafe_allow_html=True)



# Set up page configuration at the start
st.set_page_config(page_title="OfficeConnect AI", page_icon="📄")

#st.markdown(hide_st_style, unsafe_allow_html=True)

def main():
    st.title("OfficeConnect AI")
    st.markdown("Developed by : **Aneesh Mohanan**")
    st.markdown("---")

    # Load backend CSV
    st.info("Loading Data ...")
    csv_data = load_backend_csv()

    if csv_data is not None:
        st.success("Backend Data loaded successfully!")

        st.subheader("Data Preview:")
        st.dataframe(csv_data.head(2))  # Show the first few rows of the CSV

        # Input for user question
        user_question = st.text_input("Ask a question about the CSV content:")

        if user_question:
            with st.spinner("Generating AI response..."):
                csv_preview_text = csv_data.to_string(index=False, max_rows=10)  # Include a preview of the CSV
                combined_content = f"CSV Data Preview:\n{csv_preview_text}\n\nUser Question: {user_question}"
                response = model.generate_content(contents=combined_content)

            st.subheader("Response:")
            st.write(response.text)

            # Export response to PDF
            if st.button("Export Response to PDF"):
                pdf_path = export_to_pdf(response.text)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Response as PDF",
                        data=pdf_file,
                        file_name="response.pdf",
                        mime="application/pdf"
                    )
    else:
        st.error("Failed to load backend CSV. Please check the file path or format.")

    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()
