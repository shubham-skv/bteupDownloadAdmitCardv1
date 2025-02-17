import requests
from bs4 import BeautifulSoup
import streamlit as st
from fpdf import FPDF
import os

# Function to fetch admit card and modify HTML
def fetch_admit_card(enroll_no):
    url = f"https://bteup.ac.in/ESeva/Student/AdmitCard.aspx?Enrollnumber={enroll_no}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Construct correct image URLs for photo, signature, barcode, and logo
        photo_url = f"https://bteup.ac.in/PDFFILES/STUDENTIMAGES/P{enroll_no}.jpg"
        sign_url = f"https://bteup.ac.in/PDFFILES/STUDENTSIGNATURE/S{enroll_no}.jpg"
        barcode_url = f"https://bteup.ac.in/ESeva/Student/BarCode.aspx?appno={enroll_no}"
        logo_url = "https://bteup.ac.in/ESeva/Student/logo.jpg"

        # Find and modify img tags
        img_photo = soup.find("img", {"id": "imgphoto"})
        img_sign = soup.find("img", {"id": "imgsign"})
        img_barcode = soup.find("img", {"id": "imgBarcode"})

        if img_photo:
            img_photo["src"] = photo_url
            img_photo["style"] = "border-color:Black;border-width:1px;border-style:Solid;height:3.5cm;width:2.5cm;"

        if img_sign:
            img_sign["src"] = sign_url
            img_sign["style"] = "border-color:Black;border-width:1px;border-style:Solid;height:1cm;width:2.5cm;"

        if img_barcode:
            img_barcode["src"] = barcode_url
            img_barcode["style"] = "height:1cm;width:4cm;"

        # Modify the logo
        img_logo = soup.find("img", {"id": "imgLogo"})
        if img_logo:
            img_logo["src"] = logo_url
            img_logo["style"] = "height:2cm;width:3cm;"

        return str(soup)  # Return modified HTML as string
    else:
        return None  # Return None if request fails


# Function to generate a PDF from HTML content
def generate_pdf(html_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, html_content)
    
    # Make a directory to save the PDF if it doesn't exist
    if not os.path.exists('generated_files'):
        os.makedirs('generated_files')
    
    pdf_output = os.path.join("generated_files", "admit_card.pdf")
    pdf.output(pdf_output)
    return pdf_output


# Streamlit App Configuration
st.set_page_config(page_title="Admit Card Viewer", layout="centered")
st.title("🎓 Admit Card Viewer")

# Input field for Enrollment Number
enroll_no = st.text_input("Enter Enrollment Number:", "")

# Submit Button
if st.button("Submit") and enroll_no:
    modified_html = fetch_admit_card(enroll_no)

    if modified_html:
        st.subheader("Admit Card Preview:")
        
        # Display the full modified HTML in Streamlit
        st.components.v1.html(modified_html, height=600, scrolling=True)

        # Option to download as PDF
        if st.button("Download as PDF"):
            # Use the print button code (simulating the same functionality)
            pdf_file = generate_pdf(modified_html)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name="admit_card.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("❌ Admit Card Not Found! Please check the enrollment number.")
