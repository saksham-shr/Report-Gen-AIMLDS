# Academic Activity Report Generator v2.0

## Overview

The **Academic Activity Report Generator v2.0** is a comprehensive web application designed for Christ University's Department of AI, ML & Data Science to create professional academic activity reports. The application provides an intuitive, multi-section form interface with dynamic fields, file uploads, and automatic PDF generation.

## Key Features

### 1. **Fixed Header Information**
- Displays Christ(Deemed to be University) information on all reports
- School of Engineering and Technology
- Department of AI, ML & Data Science

### 2. **Sidebar Navigation**
- Easy navigation between 8 main sections
- Visual indicators with emoji icons
- Active section highlighting
- Mobile-responsive design

### 3. **General Information Section**
- **Type of Activity** dropdown with 19 predefined options:
  - Seminar, Workshop, Conference, Technical Talk, Guest Talk
  - Industry Visit, Sports, Cultural Competition
  - Technical fest/Academic fests, CAADS
  - Research Clubs, Newsletter, Alumni
  - Faculty Development Program, Quality Improvement Program
  - Refresher Course, MoU, Outreach Activity, International Event
  
- **Sub Category** dropdown that dynamically updates based on activity type
- **Other** option with custom text input for unlisted subcategories
- **Date and Time** section with:
  - Start Date and End Date pickers
  - Start Time and End Time pickers
  - Automatic handling of multi-day events
- **Venue** field for event location
- **Collaboration/Sponsor** field for partnership details

### 4. **Speaker/Guest/Presenter Details**
- Add multiple speakers with "Add Another Speaker" button
- For each speaker:
  - Name (required)
  - Title/Position (required)
  - Organization (required)
  - Contact Info (optional)
  - Title of Presentation (required)
- Remove individual speakers with "Remove" button
- Minimum 1 speaker required

### 5. **Participants Profile**
- Add multiple participant types with "Add Participant Type" button
- For each participant type:
  - Type of Participants dropdown (Faculty, Student, Research Scholar)
  - Number of Participants (numeric input)
- Real-time total participant count display
- Remove individual participant types
- Minimum 1 participant type required

### 6. **Synopsis of the Activity**
- **Highlights of the Activity** - Key highlights (required)
- **Key Takeaways** - Main learning points (required)
- **Summary of the Activity** - Comprehensive summary (required)
- **Follow-up Plan** - Future actions or plans (required)

### 7. **Report Prepared By**
- Add multiple preparers with "Add Another Preparer" button
- For each preparer:
  - Name (required)
  - Designation (required)
  - Digital Signature upload (image file, JPG/PNG, max 2MB)
- Remove individual preparers
- Minimum 1 preparer required

### 8. **Speaker Profile**
- Optional speaker photo upload (JPG/PNG, max 2MB)
- Speaker biography text (max 1000 characters)
- Real-time character counter
- Displays in generated PDF with proper formatting

### 9. **Activity Photos**
- **Photo 1** - Mandatory
- **Photo 2** - Mandatory
- **Photo 3** - Optional
- Drag-and-drop or click-to-upload interface
- File preview with size display
- Automatic image resizing for PDF optimization

### 10. **PDF Generation**
- Professional PDF report with:
  - University header information
  - All form sections properly formatted
  - Tables for organized data display
  - Embedded images (speaker photos, activity photos, signatures)
  - Proper page breaks and spacing
  - Color-coded sections for readability

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone or Extract Project
```bash
cd /path/to/report-generator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python3 app.py
```

The application will start on `http://localhost:5000`

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### Basic Workflow

1. **Start with General Information**
   - Select the type of activity from the dropdown
   - Choose a sub-category (or select "Other" and enter custom text)
   - Set the event date and time
   - Enter the venue location
   - Add collaboration/sponsor details (if applicable)

2. **Add Speaker Details**
   - Click "Add Another Speaker" to add the first speaker
   - Fill in speaker information (name, title, organization, contact, presentation title)
   - Add multiple speakers if needed

3. **Add Participant Information**
   - Click "Add Participant Type"
   - Select participant type (Faculty, Student, or Research Scholar)
   - Enter the number of participants
   - Add multiple participant types as needed
   - View total participant count in real-time

4. **Complete Synopsis**
   - Enter highlights, key takeaways, summary, and follow-up plan
   - All fields are required

5. **Add Report Preparers**
   - Click "Add Another Preparer"
   - Enter preparer name and designation
   - Upload digital signature (image file)
   - Add multiple preparers if needed

6. **Add Speaker Profile** (Optional)
   - Upload speaker photo (optional)
   - Enter speaker biography (max 1000 characters)

7. **Upload Activity Photos** (Mandatory)
   - Upload at least 2 activity photos
   - Optional third photo can be added

8. **Generate Report**
   - Review all information
   - Click "Generate PDF Report"
   - PDF will be automatically downloaded

## Form Validation

The application validates the following before PDF generation:
- ✓ Activity Type is selected
- ✓ Venue is provided
- ✓ At least 1 speaker is added
- ✓ At least 1 participant type is added
- ✓ At least 1 report preparer is added
- ✓ At least 2 activity photos are uploaded

## File Structure

```
report-generator/
├── app.py                 # Flask application main file
├── report_logic.py        # PDF generation logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main form template
├── static/
│   └── (CSS and JS files)
└── uploads/              # Temporary upload directory
    ├── signatures/       # Digital signatures
    ├── speaker/          # Speaker photos
    └── photos/           # Activity photos
```

## Technical Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Generation**: ReportLab
- **Image Processing**: Pillow (PIL)
- **File Handling**: Werkzeug

## Configuration

### Upload Settings
- Maximum file size: 50MB
- Allowed image formats: JPG, PNG, GIF
- Image optimization: Automatic resizing to 1200px width

### PDF Settings
- Page size: A4
- Margins: 0.7 inches
- Font: Helvetica
- Colors: Professional color scheme with blue accents

## Troubleshooting

### Issue: Application won't start
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Images not appearing in PDF
**Solution**: Check that image files exist and are in supported formats (JPG, PNG)

### Issue: Form submission fails
**Solution**: Ensure all required fields are filled:
- Activity Type must be selected
- Venue must be provided
- At least 1 speaker must be added
- At least 1 participant type must be added
- At least 1 report preparer must be added
- At least 2 activity photos must be uploaded

### Issue: PDF download doesn't start
**Solution**: Check browser download settings and ensure pop-ups are not blocked

## Browser Compatibility

- Chrome/Chromium: ✓ Fully supported
- Firefox: ✓ Fully supported
- Safari: ✓ Fully supported
- Edge: ✓ Fully supported
- IE 11: ✗ Not supported

## Mobile Responsiveness

The application is responsive and works on:
- Desktop computers (1024px and above)
- Tablets (768px and above)
- Mobile devices (with optimized layout)

## Security Considerations

- File uploads are validated for type and size
- Filenames are sanitized to prevent path traversal
- Uploaded files are stored in a dedicated directory
- No sensitive data is stored permanently

## Performance

- Average form completion time: 5-10 minutes
- PDF generation time: 2-5 seconds
- Maximum recommended participants per report: 500

## Support & Maintenance

For issues or feature requests, please contact:
- Email: saksham.sharma@btech.christuniversity.in
- Department: AI, ML & Data Science

## Version History

### Version 2.0 (Current)
- Complete redesign with sidebar navigation
- Support for multiple speakers
- Support for multiple participant types
- Support for multiple report preparers
- Enhanced PDF formatting
- Improved user interface
- Mobile responsive design
- Dynamic subcategory selection
- Character counter for speaker bio
- Real-time participant count
- Professional styling with color scheme

### Version 1.0
- Basic form with single speaker support
- Simple PDF generation

## License

This application is developed for Christ University and is intended for internal use only.

## Credits

Developed by: OneStop Dev Pvt Ltd
Incubated in: Christ Incubation Center

---

**Last Updated**: November 2025
**Current Version**: 2.0
