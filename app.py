# app.py
import streamlit as st
import subprocess

st.title("Google Play Review Scraper")
st.write("Enter the Google Play app URL to start scraping reviews.")

# Input field for the Google Play app URL
app_url = st.text_input("Google Play App URL", "")

# Button to run the Selenium producer script
if st.button("Start Scraping"):
    if app_url:
        try:
            # Run the Selenium producer script with the entered URL
            result = subprocess.run(
                ["python", "scripts/selenium_producer.py", app_url],
                capture_output=True,
                text=True
            )
            st.write("Scraping started successfully.")
            st.write("Output:", result.stdout)
        except Exception as e:
            st.write("Error:", str(e))
    else:
        st.write("Please enter a valid Google Play app URL.")
