import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from report_logic import generate_report_pdf, ensure_image_resized
from io import BytesIO
import time
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

def save_uploaded_file(fileobj, subfolder=None):
    if not fileobj or fileobj.filename == '':
        return None
    if not allowed_file(fileobj.filename, ALLOWED_IMAGE_EXTS):
        return None
    
    filename = secure_filename(fileobj.filename)
    ts = int(time.time() * 1000)
    name = f"{ts}_{filename}"
    dest_dir = app.config['UPLOAD_FOLDER'] if not subfolder else os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, name)
    fileobj.save(path)
    return path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data = {}

            # General Information
            data['general_info'] = {
                'Activity Type': request.form.get('activityType', ''),
                'Sub Category': request.form.get('subCategory', '') or request.form.get('otherSubCategory', ''),
                'Start Date': request.form.get('startDate', ''),
                'End Date': request.form.get('endDate', ''),
                'Start Time': request.form.get('startTime', ''),
                'End Time': request.form.get('endTime', ''),
                'Venue': request.form.get('venue', ''),
                'Collaboration/Sponsor': request.form.get('collaboration', '')
            }
            # Remove empty values
            data['general_info'] = {k: v for k, v in data['general_info'].items() if v}

            # Extract multiple speakers
            speakers = []
            speaker_index = 0
            while True:
                name_key = f'speaker-name-{speaker_index}'
                if name_key not in request.form:
                    break
                
                speaker_name = request.form.get(name_key, '').strip()
                if speaker_name:
                    speaker = {
                        'name': speaker_name,
                        'title': request.form.get(f'speaker-title-{speaker_index}', '').strip(),
                        'organization': request.form.get(f'speaker-org-{speaker_index}', '').strip(),
                        'contact': request.form.get(f'speaker-contact-{speaker_index}', '').strip(),
                        'presentation_title': request.form.get(f'speaker-presentation-{speaker_index}', '').strip()
                    }
                    speakers.append(speaker)
                speaker_index += 1
            
            data['speakers'] = speakers

            # Extract multiple participants
            participants = []
            participant_index = 0
            while True:
                type_key = f'participant-type-{participant_index}'
                if type_key not in request.form:
                    break
                
                participant_type = request.form.get(type_key, '').strip()
                if participant_type:
                    count = request.form.get(f'participant-count-{participant_index}', '0').strip()
                    participant = {
                        'type': participant_type,
                        'count': count
                    }
                    participants.append(participant)
                participant_index += 1
            
            data['participants'] = participants

            # Synopsis
            data['synopsis'] = {
                'highlights': request.form.get('highlights', '').strip(),
                'key_takeaways': request.form.get('keyTakeaways', '').strip(),
                'summary': request.form.get('summary', '').strip(),
                'follow_up': request.form.get('followUp', '').strip()
            }

            # Extract multiple preparers
            preparers = []
            preparer_index = 0
            while True:
                name_key = f'preparer-name-{preparer_index}'
                if name_key not in request.form:
                    break
                
                preparer_name = request.form.get(name_key, '').strip()
                if preparer_name:
                    preparer = {
                        'name': preparer_name,
                        'designation': request.form.get(f'preparer-designation-{preparer_index}', '').strip(),
                        'signature_path': None
                    }
                    
                    # Handle signature upload
                    sig_file = request.files.get(f'preparer-signature-{preparer_index}')
                    if sig_file and sig_file.filename:
                        sig_path = save_uploaded_file(sig_file, subfolder='signatures')
                        if sig_path:
                            preparer['signature_path'] = ensure_image_resized(sig_path)
                    
                    preparers.append(preparer)
                preparer_index += 1
            
            data['preparers'] = preparers

            # Speaker Profile
            speaker_profile = {}
            
            # Speaker image
            speaker_file = request.files.get('speakerImage')
            if speaker_file and speaker_file.filename:
                speaker_path = save_uploaded_file(speaker_file, subfolder='speaker')
                if speaker_path:
                    speaker_profile['image_path'] = ensure_image_resized(speaker_path)
            
            speaker_bio = request.form.get('speakerBio', '').strip()
            if speaker_bio:
                speaker_profile['bio'] = speaker_bio
            
            data['speaker_profile'] = speaker_profile

            # Activity Photos (at least 2 required)
            photos = []
            photo_index = 1
            while True:
                photo_key = f'photo{photo_index}'
                if photo_key not in request.files:
                    break
                
                photo_file = request.files.get(photo_key)
                if photo_file and photo_file.filename:
                    photo_path = save_uploaded_file(photo_file, subfolder='photos')
                    if photo_path:
                        photos.append(ensure_image_resized(photo_path))
                photo_index += 1
            
            data['photos'] = photos

            # Validate required fields
            errors = []
            
            if not data['general_info'].get('Activity Type'):
                errors.append("Activity Type is required")
            if not data['general_info'].get('Venue'):
                errors.append("Venue is required")
            if not speakers:
                errors.append("At least one speaker is required")
            if not participants:
                errors.append("At least one participant type is required")
            if not preparers:
                errors.append("At least one report preparer is required")
            if len(photos) < 2:
                errors.append("At least 2 activity photos are required")
            
            if errors:
                error_msg = "; ".join(errors)
                return render_template('index.html', error=error_msg)

            # Generate PDF
            pdf_bytes = generate_report_pdf(data)

            activity_title = data['general_info'].get('Activity Type', 'Activity')
            filename = f"{activity_title}_Report_{int(time.time())}.pdf"

            return send_file(
                BytesIO(pdf_bytes),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )

        except Exception as exc:
            print("Exception in POST:", exc)
            import traceback
            traceback.print_exc()
            return render_template('index.html', error=f"Error generating report: {str(exc)}")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
