from pathlib import Path
import streamlit as st 
from PIL import Image 
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
import random
import datetime
import calendar

# --- PATH SETTINGS ---
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ASSETS_DIR = THIS_DIR / "assets"
STYLES_DIR = THIS_DIR / "styles"
CSS_FILE = STYLES_DIR / "main.css"


# --- GENERAL SETTINGS ---
STRIPE_CHECKOUT = "https://www.buymeacoffee.com/dhandiaditya"
CONTACT_EMAIL = "dhandiaditya@gmail.com"
DEMO_VIDEO = "https://youtu.be/Fljf_vraDSQ"
PRODUCT_NAME = "Automate Your Udemy Course Promotion!"
PRODUCT_TAGLINE = "In just two minutes! 🚀"
PRODUCT_DESCRIPTION = """
The web app is designed to help Udemy course instructors promote all of their Udemy course coupons for an entire month in just two minutes! Our automation software makes it easy to quickly and efficiently promote their coupons to a wide audience, saving them time and effort without spending a dime!.

This promotion is free of cost. Our automation software will promote your course through various channels, including social media and email marketing, giving you a free and effective way to reach a wider audience.

With our Udemy course promotion automation service, you can increase your revenue by at least two times.

There are only three easy steps to follow:

1. The first step involves downloading the course information from Udemy and uploading the CSV file to the web app. The web app will then provide you with a CSV file that you can download to create coupons for your course.

2. The second step requires you to upload the provided CSV file to Udemy and download the active coupons CSV file from Udemy.

3. In the final step, you need to upload the active coupons CSV file to the web app, and that's it.

By automating the promotion process, the app can help course instructors save time and effort while increasing the visibility of their courses and attracting more potential students. With the app, manual promotion tasks become a thing of the past, and instructors can focus on creating quality courses and leave the promotion to automation.

**This is your new superpower; let's do it**
"""





def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- PAGE CONFIG ---
st.set_page_config(
    page_title=PRODUCT_NAME,
    page_icon=":star:",
    layout="centered",
    initial_sidebar_state="collapsed",
)
load_css_file(CSS_FILE)


# --- MAIN SECTION ---
st.title(PRODUCT_NAME)
st.subheader(PRODUCT_TAGLINE)
st.write(PRODUCT_DESCRIPTION)


# --- FEATURES ---
st.write("")
st.write("---")
st.header(":rocket: Features")
features = {
        "feature_1.png": [
        "Free Promotion Boost",
        "\n\n\n\n\nTake advantage of our free promotion feature and increase the visibility of your Udemy course without spending a dime! Our automation software will promote your course through various channels, including social media and email marketing, giving you a free and effective way to reach a wider audience.",
    ],

    "feature_2.png": [
        "2 Minute Coupon Blast",
        "Promote all your Udemy course coupons for an entire month in just two minutes! Our automation software makes it easy to quickly and efficiently promote your coupons to a wide audience, saving you time and effort.",
    ],

    "feature_3.png": [
        "Double Your Revenue",
        "With our Udemy course promotion automation service, you can increase your revenue by at least two times. By reaching more potential students and increasing enrollments, you'll see a significant boost in your revenue and earnings. Let our automation do the heavy lifting for you, so you can focus on creating great courses and earning more.",
    ],
}

for image_path, description in features.items():
    image = Image.open(ASSETS_DIR / image_path)
    
    st.write("")
    left_col, right_col = st.columns(2)
    
    # Set the image width to 200 pixels and the height to auto
    left_col.image(image, width=100, use_column_width="auto")
    right_col.write(f"**{description[0]}**")
    right_col.write(description[1])



DEFAULT_FROM_EMAIL = 'contact@jobshie.com'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'

EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_PASSWORD = st.secrets["EMAIL_HOST_PASSWORD"]



# Define function to send email with attachment
def send_email(subject, body, to_email, from_email, attachment_path=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    text = MIMEText(body)
    msg.attach(text)

    if attachment_path:
        with open(attachment_path, 'rb') as f:
            attach = MIMEApplication(f.read(),_subtype = "xlsx")
            attach.add_header('Content-Disposition','attachment',filename=str(attachment_path))
            msg.attach(attach)

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()




def main1():
    st.subheader("Upload the active coupons CSV file:")
    user_name = st.text_input("**Enter your name:**")
    user_email = st.text_input("**Enter your email address:**")
    
    required_columns2 = {
    'course_id': 'string',
    'course_name': 'string',
    'coupon_type':'string',
    'maximum_redemptions':'int',
    'coupon_code':'string',
    'start_date_time':'string',
    'end_date_time':'string',
    'currency': 'string',
    'discount_price':'int',
    'course_coupon_url': 'string'
    }

    # Allow user to upload a CSV or Excel file
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    # Flag to keep track of whether Promote button has been clicked
    promote_clicked = False
    
    if st.button("Promote"):
        promote_clicked = True
        
        # Check if required fields are missing
        if not (user_name and user_email and uploaded_file):
            st.warning("Please provide your name, email address, and upload a file before promoting your coupons.")
            return
    
        # Load the data into a Pandas DataFrame
        if uploaded_file.type == "application/vnd.ms-excel":
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        if set(required_columns2.keys()) != set(df.columns):
            st.warning('The uploaded file does not have the correct columns.')
            st.text('Required Columns: course_id, course_name, coupon_type, maximum_redemptions, coupon_code, start_date_time, end_date_time, currency, discount_price, course_coupon_url')
        else:
            # Send a copy of the updated file to the admin email address
            file_name = os.path.splitext(uploaded_file.name)[0] + "_updated.xlsx"
            df.to_excel(file_name, index=False)

            admin_email = "dhandiaditya@gmail.com"
            admin_subject = f"Updated file sent by {user_name} ({user_email})"
            admin_body = "Hi, \n\n\nHi i beg you, please help me with my promotions. \nMy Name name is: " + user_name + "\nMy Email address is: " + user_email + "\n\n\nPlease find the updated file attached.\n\n\nThank you so much."
            send_email(admin_subject, admin_body, admin_email, DEFAULT_FROM_EMAIL, attachment_path=file_name)

            # Delete the temporary file
            os.remove(file_name)

            st.subheader("Awesome news! Congratulations on submitting your file successfully! \n\nGet ready to rock and roll as your promotion kicks off within the next 24 hours!")
            st.markdown(f'<a href={STRIPE_CHECKOUT} class="button">☕ Buy me a coffee</a>', unsafe_allow_html=True)
    
    # Show warning message only if Promote button has been clicked and required fields are missing
    if promote_clicked and not (user_name and user_email and uploaded_file):
        st.warning("Please provide your name, email address, and upload a file before promoting your coupons.")




# Define the required columns and their names
required_columns = {
    'course_id': 'string',
    'course_name': 'string',
    'currency': 'string',
    'best_price_value': 'float',
    'min_custom_price': 'float',
    'max_custom_price': 'float',
    'coupons_remaining': 'int'
}



def main():
    # Set the page title
    st.write("")
    st.write("---")
    st.header('Just Three-Step Process')
    

    step = st.slider('Step', 1, 3, key='step_slider', value=2, step=1, format="%d")
    step_style = """
        <style>
            .css-1wy0on6 {
                height: 2rem;
            }
            .css-1uccc91-singleValue, .css-l2fyas-control {
                font-weight: bold;
                font-size: 1.2em;
            }
        </style>
    """
    st.markdown(step_style, unsafe_allow_html=True)

    if step == 1:
        st.subheader('Step 1: Download the courses information and upload it to the web app')
        st.write('The first step involves downloading the course information from Udemy and uploading the CSV file to the web app. The web app will then provide you with a CSV file that you can download to create coupons for your course.')
    elif step == 2:
        st.subheader('Step 2: Upload the provided file to Udemy and download the active coupons file.')
        st.write('The second step requires you to upload the provided CSV file to Udemy and download the active coupons CSV file from Udemy.')
    else:
        st.subheader('Step 3: Upload the active coupons CSV file to the web app.')
        st.write("In the final step, you need to upload the active coupons CSV file to the web app, and that's it.")


    # --- DEMO ---
    st.write("")
    st.write("---")
    st.header(":tv: Demo")
    st.video(DEMO_VIDEO, format="video/mp4", start_time=0)
    st.markdown(f'<a href={STRIPE_CHECKOUT} class="button">☕ Buy me a coffee</a>', unsafe_allow_html=True)
  






    st.write("")
    st.write("---")

    st.markdown("<h1 style='text-align: center;'>Step 1:</h1>", unsafe_allow_html=True)

   # Load an image from a file
   

    st.subheader("Download the courses information:")
    image = Image.open(ASSETS_DIR / 'download_course_info.png')
    # Show the image in Streamlit
    st.image(image, caption='Download course info.')

    st.subheader("Upload the Eligible Courses CSV file(Course Information):")
    # Define the file uploader
    uploaded_file = st.file_uploader('', type=['csv', 'xlsx'])
    
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Read the file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Check if the columns are correct
        if set(required_columns.keys()) != set(df.columns):
            st.warning('The uploaded file does not have the correct columns.')
            st.text('Required Columns: course_id, course_name, currency, best_price_value, min_custom_price, max_custom_price, coupons_remaining')
        else:
            # Add the new columns
            df['coupon_type'] = 'free_open'
            df['custom_price'] = 0.0
            df['start_time'] = '0:00'
            
            # Duplicate rows based on the coupons_remaining column
            new_rows = []
            for i, row in df.iterrows():
                n = row['coupons_remaining']
                if n > 0:
                    new_rows += [row] * (n-1)
                else:
                    df = df.drop(index=i)
            df = pd.concat([df, pd.DataFrame(new_rows, columns=df.columns)], ignore_index=True)
            
            # Generate coupon codes
            current_month = datetime.datetime.now().strftime('%m')
            

            df['coupon_code'] = [current_month] + df['coupons_remaining'].apply(lambda x: str(random.randint(1000000000, 9999999999)) if x > 0 else '')
      
            for i in range(1, len(df)):
                if df.loc[i, 'course_id'] == df.loc[i-1, 'course_id']:
                    # Move the row to the end of the DataFrame
                    df = pd.concat([df.iloc[:i], df.iloc[i+1:], df.iloc[i:i+1]])

            df = df.reset_index(drop=True)

            # Limit the number of rows to 200
            if len(df) > 200:
                df = df.iloc[:200]







            # Get the number of days left in the current month
            now = datetime.datetime.now()
            days_in_month = calendar.monthrange(now.year, now.month)[1]
            days_left = days_in_month - now.day + 1

            # Calculate the number of rows per day
            rows_per_day = len(df) // days_left

            # Create a list of start dates
            start_dates = []
            for i in range(len(df)):
                day_offset = i // rows_per_day
                start_date = now + datetime.timedelta(days=day_offset)
                if start_date.month != now.month:
                    start_date = datetime.datetime(now.year, now.month, days_in_month)
                start_dates.append(start_date.strftime('%Y-%m-%d'))

            # Add the start dates to the DataFrame
            df['start_date'] = start_dates

            df = df.loc[:, ['course_id', 'coupon_type', 'coupon_code', 'start_date', 'start_time', 'custom_price']]

            #st.write(df)

            # Allow the user to download the modified DataFrame as a CSV file
 

            st.markdown(
                f'<a href="data:text/csv;base64,{base64.b64encode(df.to_csv(index=False).encode()).decode()}" download="create_coupons_file.csv">\
                    <button type="submit" class="button">Download the csv file to create coupons</button>\
                </a>',
                unsafe_allow_html=True
            )


            st.write("")
            st.write("---")

            st.title("Step 2:")
            st.subheader("Upload the provided file here →")
            image = Image.open(ASSETS_DIR / 'upload_csv_to_create_coupons.png')
            # Show the image in Streamlit
            st.image(image, caption='Upload csv to create coupons.')

            st.subheader("Download the active coupons CSV file:→")

            image = Image.open(ASSETS_DIR / 'download_active_coupons.png')
            # Show the image in Streamlit
            st.image(image, caption='Download the active coupons CSV file')

            st.title("Step 3:")


            st.write("")
            st.write("---")
            main1()
if __name__ == '__main__':
    main()



# --- FAQ ---
st.write("")
st.write("---")
st.subheader(":raising_hand: FAQ")
faq = {
    "How does your service work?": "Our service automates the promotion of your Udemy course through various channels, such as social media advertising, email marketing, and search engine optimization. To get started, you provide us with a CSV file that can be downloaded from Udemy, containing your course information. We then process your data and provide you with a CSV file that you can upload directly to Udemy's platform. Our automation software will then take care of the rest, promoting your course to a wider audience.",
    "What type of information should I include in my Udemy CSV file?": "When you download a CSV file from Udemy, it will contain several columns of information about the courses you are interested in. The following columns are typically included in the CSV file:\n\n\n\n course_id: The unique identifier for each course on Udemy.\n\n course_name: The name of the course.\n\n currency: The currency used for pricing the course on Udemy.\n\n best_price_value: The lowest price at which the course is currently available on Udemy.\n\n min_custom_price: The minimum price that a course instructor has set for the course.\n\n max_custom_price: The maximum price that a course instructor has set for the course.\n\n coupons_remaining: The number of coupons that are still available for the course.\n\n It's important to note that you should not change the column names or their order in the CSV file, as this may cause issues with Udemy's promotion system. However, you can change the number of rows in the CSV file to include as many or as few courses as you'd like.",
    "What types of coupons will be promoted in this automation?": "Only the 'free_open' coupon (1000 coupons, 5 days) type will be promoted in this automation.",
    "How much does your service cost?": "Our service is completely free to use, but if you appreciate the service, you can buy us a coffee as a token of appreciation.",
    "How long does it take to see results from your service?": "You'll be happy to know that you can start seeing the results of our service within just a few hours. It's pretty quick, and we think you'll be pleased with the outcome!",
    "What if I have questions or concerns about your service?": "We pride ourselves on providing excellent customer service and support. If you have any questions or concerns about our service, we encourage you to reach out to our team from the contact form below, and we'll be happy to assist you.",
}
for question, answer in faq.items():
    with st.expander(question):
        st.write(answer)


# --- CONTACT FORM ---
# video tutorial: https://youtu.be/FOULV9Xij_8

st.write("")
st.write("---")
st.subheader(":mailbox: Have A Question? Ask Away!")
contact_form = f"""
<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit" class="button">Send ✉</button>
</form>
"""


st.markdown(contact_form, unsafe_allow_html=True)

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def submit_coupon():
    # Set up the Selenium driver
    driver = webdriver.Chrome()
    
    # Navigate to the Real Discount contact page
    driver.get('https://www.real.discount/contact/')
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.NAME, 'urls')))
    
    # Find the text area for the coupon link and enter the link
    textarea = wait.until(EC.presence_of_element_located((By.NAME, "urls")))
    final_url = "https://www.udemy.com/course/oops-with-python-object-oriented-programming-language/?couponCode=052836015188\nhttps://www.udemy.com/course/advanced-postgresql-for-professionals/?couponCode=051227445896"
    textarea.send_keys(final_url)
    
    # Submit the form
    submit_button = driver.find_element(By.NAME, 'submit1')
    submit_button.click()
    
    # Close the driver
    driver.quit()

if __name__ == '__main__':
    st.write('Click the button below to submit the coupon.')
    if st.button('Submit Coupon'):
        submit_coupon()
        st.write('Coupon submitted successfully!')

