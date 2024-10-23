from flask import Flask, render_template, request, redirect, url_for, flash
import os
#from transformer_bert_model.transformer_bert_model_eval import get_prediction
import pandas as pd
import base64
from database.Text_Add_Retrieve import add_text_info, add_text_file
from database.Audio_Add_Retrieve import add_audio_info



app = Flask(__name__)
app.secret_key = "supersecretkey"  # for flash messages
#app.config['UPLOAD_FOLDER_TEXT'] = './User_Panel/text_file_uploads'
app.config['UPLOAD_FOLDER_AUDIO'] = './User_Panel/audio_file_uploads'


if not os.path.exists(app.config['UPLOAD_FOLDER_AUDIO']):
    os.makedirs(app.config['UPLOAD_FOLDER_AUDIO'])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image_page/<image_id>')
def image_page(image_id):
    # Render the template and pass the image ID to be used in the new page
    return render_template('image_page.html', image_id=image_id)


@app.route('/submit_review', methods=['POST'])
def submit_review():
    review_type = request.form.get('review_type')
    pid_text = request.form.get('pid-text')  # For the text review
    pid_audio = request.form.get('pid-audio')  # For the audio review
    pid_video = request.form.get('pid-video')  # For the video review
    
    # !------------------------------- Handling Text reviews
    if review_type == 'text':
        text_review = request.form.get('single-text')
        text_file = request.files.get('text-upload')
        test_file_path = None
        
        # saving single review into the database
        if text_review:
            # Handle text review here
            print(f'Pid text in app.py: {pid_text}')
            add_text_info(pid_text, text_review)
            flash('Text review submitted successfully!', 'success')
        
        
        # Saving the uploaded file into the database
        elif text_file and text_file.filename.endswith('csv'):
            test_file_path = os.path.join('Text_file_uploads', text_file.filename)
            text_file.save(test_file_path)
            
            # Loading saved dataframe
            df = pd.read_csv(test_file_path)
            
            # List column names
            columns = df.columns.tolist()
                        
            # Try to find the column with reviews (checking common names)
            possible_review_columns = ['review', 'reviews', 'text', 'comment', 'comments']
        
            # Find the first matching column (or default)
            review_column = None
            for col in possible_review_columns:
                if col in columns:
                    review_column = col
                    break
                
            # Process the reviews
            reviews = df[review_column].tolist()    
            for i in range(len(reviews)):
                add_text_info(pid_text, reviews[i])
            
            flash('Text file uploaded successfully!', 'success')
            
        
        
        
    # !------------------------------------ Handling Audio reviews    
    elif review_type == 'audio':
        audio_file = request.files.get('audio-upload')
        recorded_audio = request.form.get('recorded-audio')
        audio_file_path = None
        recorded_audio_file_path = None
        
        # Handle uploaded audio file
        if audio_file:
            audio_file_path = os.path.join(app.config['UPLOAD_FOLDER_AUDIO'], audio_file.filename)
            audio_file.save(audio_file_path)
            flash('Audio file uploaded successfully!', 'success')
        
        if recorded_audio:
            # Decode Base64 audio and save it as a file
            try:
                audio_data = recorded_audio.split(',')[1]  # Extract base64 part after "data:audio/wav;base64,"
                audio_bytes = base64.b64decode(audio_data)
                recorded_audio_file_path = os.path.join(app.config['UPLOAD_FOLDER_AUDIO'], f'recorded_audio.wav')
                
                with open(recorded_audio_file_path, 'wb') as f:
                    f.write(audio_bytes)
                
                flash('Recorded audio saved successfully!', 'success')
            except Exception as e:
                print(f"Error saving recorded audio: {e}")
                flash('Failed to save recorded audio.', 'error')
    
        # Save the uploaded audio file path into the database
        if audio_file_path:
            add_audio_info(pid_audio, audio_file_path)

        # Save the recorded audio file path into the database
        if recorded_audio_file_path:
            add_audio_info(pid_audio, recorded_audio_file_path)
        
        
        
    # Handling Video reviews    
    elif review_type == 'video':
        video_file = request.files.get('video-upload')
        if video_file:
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename))
            flash('Video file uploaded successfully!', 'success')
        
        # Video recording logic will go here
    
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
