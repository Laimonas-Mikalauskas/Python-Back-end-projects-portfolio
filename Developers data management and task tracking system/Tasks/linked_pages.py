from flask import Flask, url_for, redirect
app = Flask(__name__)

# Route handlers
@app.route('/')
def index():
    about_url = url_for('about')
    services_url = url_for('services')
    gallery_url = url_for('gallery')
    videos_url = url_for('videos')
    contact_url = url_for('contact_us')
    follow_url = url_for('follow_us')
    admin_url = url_for('admin_page')
    return f"""<h1>Welcome to the Home Page</h1>
<p><a href="{about_url}">About Us</a></p>
<p><a href="{services_url}">Services</a></p>
<p><a href="{gallery_url}">Gallery</a></p>
<p><a href="{videos_url}">Video</a></p>
<p><a href="{contact_url}">Contact Us</a></p>
<p><a href="{follow_url}">Follow Us</a></p>
<p><a href="{admin_url}">Admin Page</a></p>
"""

@app.route('/linked_pages')
def linked_pages():
    return redirect(url_for('index'))

  
@app.route('/about')
def about():
    return "<h1>About Us</h1><p>This is the About page.</p>"

@app.route('/services')
def services():
    return "<h1>Services</h1><p>This is the Services page.</p>"

@app.route('/gallery')
def gallery():
    return "<h1>Gallery</h1><p>This is the Gallery page.</p>"

@app.route('/videos')
def videos():
    return "<h1>Video</h1><p>This is the Video page.</p>"

@app.route('/contact')
def contact_us():
    return "<h1>Contact Us</h1><p>This is the Contact Us page.</p>"

@app.route('/follow')
def follow_us():
    return "<h1>Follow Us</h1><p>This is the Follow Us page.</p>"


@app.route('/admin')
def admin_page():
    return "<h1>Admin Page</h1><p>Welcome, Admin!</p>"

@app.route('/invalid')
def invalid():
    return "<h1>Invalid Page</h1><p>This page does not exist.</p>", 404

# Error handlers - Standard HTTP status codes only
error_messages = {
    400: ("400 Bad Request", "Your request is invalid."),
    401: ("401 Unauthorized", "You need to log in to access this page."),
    403: ("403 Forbidden", "You do not have permission to access this page."),
    404: ("404 Not Found", "The page you are looking for does not exist."),
    405: ("405 Method Not Allowed", "The method is not allowed for the requested URL."),
    500: ("500 Internal Server Error", "Something went wrong on the server."),
    503: ("503 Service Unavailable", "The server is currently unavailable."),
    504: ("504 Gateway Timeout", "The server did not receive a timely response."),
}

# Register error handlers dynamically
for code, (title, message) in error_messages.items():
    def make_error_handler(title, message, code):
        def handler(e):
            return f"<h1>{title}</h1><p>{message}</p>", code
        return handler
    app.errorhandler(code)(make_error_handler(title, message, code))

if __name__ == '__main__':
    app.run(debug=True)