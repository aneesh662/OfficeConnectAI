import streamlit as st
from fpdf import FPDF
import tempfile
import google.generativeai as genai
import pandas as pd

# Configure Google Generative AI
genai.configure(api_key="AIzaSyCjsLMO-GZy5295jRe7-33MkEDkcuopnFU")
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
    #"""Load the predefined backend CSV file."""

    csv_path = "backend_data.csv"  # Path  CSV file
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        st.error("Backend CSV file not found.")
        return None
    except Exception as e:
        st.error(f"Error loading backend CSV file: {e}")
        return None

def main():
    st.set_page_config(page_title="OfficeConnect AI", page_icon="📄")
    st.title("OfficeConnect AI")
    st.markdown("Developed by : **Aneesh Mohanan**")
   # st.markdown("Predefined Data file as backend with AI chatbot integration.")
    st.markdown("---")

    # Load backend CSV
    st.info("Loading Data ...")
    csv_data = load_backend_csv()

    if csv_data is not None:
        st.success("Backend Data loaded successfully!")

        st.subheader("Data Preview:")
        st.dataframe(csv_data.head())  # Show the first few rows of the CSV

        # Provide an option to download the backend CSV
       # csv_download_link = csv_data.to_csv(index=False).encode("utf-8")
       # st.download_button(
       #     label="Download Backend CSV",
       #     data=csv_download_link,
       #     file_name="backend_data.csv",
       #     mime="text/csv"
       # )

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
    st.markdown("**Note:** This is an interactive AI chatbot integrated with a predefined backend CSV file.")

if __name__ == "__main__":
    main()
