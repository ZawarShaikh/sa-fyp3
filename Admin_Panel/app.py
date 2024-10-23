from flask import Flask, render_template, jsonify, request
import sqlite3  # Assuming you are using SQLite
import matplotlib.pyplot as plt
import io
import base64
from transformer_bert_model.transformer_bert_model_eval import get_prediction
import pandas as pd
import csv


app = Flask(__name__)



# !--------------------------- Retrieving Data from the database ------------------------!
# Function to retrieve text data from the database
def get_text_reveiws_data(product):
    # connecting to database
    conn = sqlite3.connect(r'C:\Users\pc\Data Science\FYP_Project_Codes\MSA_Flask_Application\MSA_Prod_Rev_db.db')
    #conn = sqlite3.connect('MSA_Prod_Rev_database.db')
    cursor = conn.cursor()
    
    # Getting pid and review from database
    cursor.execute("SELECT pid, review FROM text_reviews WHERE pid=?", (product, ))  # Adjust to your table/column names
    single_text_data = cursor.fetchall()

    # Getting pid and text file loc from database
    #cursor.execute("SELECT pid, text_file_loc FROM text_file_location WHERE pid=?", (product, ))  # Adjust to your table/column names
    #text_file_data = cursor.fetchall()
    
    conn.close()
    return single_text_data

# Function to retrieve audio data from the database
def get_audio_reveiws_data(product):
    # connecting to database
    conn = sqlite3.connect(r'C:\Users\pc\Data Science\FYP_Project_Codes\MSA_Flask_Application\MSA_Prod_Rev_db.db')
    #conn = sqlite3.connect('MSA_Prod_Rev_database.db')
    cursor = conn.cursor()
    
    # Getting pid and review from database
    cursor.execute("SELECT pid, audio_file_loc FROM audio_file_location WHERE pid=?", (product, ))  # Adjust to your table/column names
    audio_file_data = cursor.fetchall()

    # Getting pid and text file loc from database
    cursor.execute("SELECT pid, audio_folder_loc FROM audio_folder_location WHERE pid=?", (product, ))  # Adjust to your table/column names
    audio_folder_data = cursor.fetchall()
    
    conn.close()
    return audio_file_data, audio_folder_data




# !----------------------- Admin panel route to view data and visualizations --------------------!
@app.route('/admin')
def admin_panel():
    # List of products
    product_list = [
        "Air Cooler",
        "Curtains",
        "Dry Iron",
        "Mens Cargo",
        "T-shirts",
        "Google Smart Home Speaker",
        "Cushions",
        "DSLR Camera",
        "Dinner Set Plates",
        "Electric Kettle",
        "Lekme Iconic Kajal"
    ]
    
    # Taking data from the database
    """
    data = [("Cushions", "Product review 1"), ("Dry Iron", "Product review 2"), ("Curtains", "Product review 3"), 
            ("Mens cargo", "Product review 4"), ("Lekme Iconinc Kajal", "Product review 5"), 
            ("Air Cooler", "Product review 6"), ("Dinner Set Plates", "Product review 7"), 
            ("T-shirts", "Product review 8"), ("Electric Kettle", "Product review 9"), 
            ("DSLR Camera", "Product review 10"), ("Google Assistant Smart Speaker", "Product review 11")]
    """
    text_sentiment_count = {"positive": 3, "negative": 1, "neutral": 1}
    audio_sentiment_count = {"positive": 2, "negative": 5, "neutral": 4}
    video_sentiment_count = {"positive": 8, "negative": 6, "neutral": 2}
    
    return render_template('admin.html', 
                           product_list = product_list,
                           text_sentiment_count=text_sentiment_count, 
                           audio_sentiment_count=audio_sentiment_count, 
                           video_sentiment_count=video_sentiment_count
                           )



# Route to handle product selection and data fetching
@app.route('/select_product', methods=['POST'])
def select_product():
    # List of products
    product_list = [
        "Air Cooler",
        "Curtains",
        "Dry Iron",
        "Mens Cargo",
        "T-shirts",
        "Google Smart Home Speaker",
        "Cushions",
        "DSLR Camera",
        "Dinner Set Plates",
        "Electric Kettle",
        "Lekme Iconic Kajal"
    ]
    
    # !-------------- Get the selected product from the form submission
    selected_product = request.form.get('product')
    
    # !-------------- Get the data from the database
    text_reviews = get_text_reveiws_data(selected_product)
    audio_file_data, audio_folder_data = get_audio_reveiws_data(selected_product)
    
    
    # !-------------- Doing sentiment analysis on text by using get_prediction function
    single_text_df = pd.DataFrame(columns=['Product', 'Reviews'], data=text_reviews)
    single_text_predictions = []
    
    for review in single_text_df['Reviews']:
        prediction = get_prediction(str(review))  # Get prediction for each individual review
        single_text_predictions.append(prediction)
    
    # Add predictions to DataFrame
    single_text_df['Prediction'] = single_text_predictions
    
    
    # !-------------- Saving Sentiment Count of each modaity
    text_sentiment_count = {"positive": len(single_text_df[single_text_df['Prediction'] == 0]), 
                            "negative": len(single_text_df[single_text_df['Prediction'] == 1]), 
                            "neutral": len(single_text_df[single_text_df['Prediction'] == 2])
                            }
    audio_sentiment_count = {"positive": 2, "negative": 5, "neutral": 4}
    video_sentiment_count = {"positive": 8, "negative": 6, "neutral": 2}

    # Render the template with the selected reviews and product list
    return render_template('admin.html', 
                           product_list=product_list, 
                           text_reviews = text_reviews, 
                           audio_file_data = audio_file_data, 
                           audio_folder_data = audio_folder_data, 
                           text_sentiment_count=text_sentiment_count, 
                           audio_sentiment_count=audio_sentiment_count, 
                           video_sentiment_count=video_sentiment_count,
                           )



if __name__ == '__main__':
    #single_text_rev, file_text_rev = get_text_reveiws_data('Air_Cooler')
    
    app.run(debug=True, port=5001)
