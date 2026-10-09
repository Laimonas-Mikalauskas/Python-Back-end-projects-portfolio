from flask import Flask, render_template, request
app = Flask(__name__)  # Correctly instantiate the Flask app

@app.route('/sitemap', methods=["GET"])
def sitemap():
    message = "Sitemap"
    sitemap_data = ["Home", "Blog", "Search", "About Us", "Services", "Sign Up", "Login", "Create Task", "Task Status", 
                    "View Tasks", "Edit Tasks", "Update Tasks", "Delete Tasks", "Task Priorities", 
                    "Task Categories", "Task Types", "Deadlines", "Updates", "Timeline", 
                    "Accomplishments", "Team Collaboration", "Collaboration Tools", 
                    "Project Tracking", "Analytics", "Reports", "Notifications", 
                    "Calendar", "Documents", "Notes", "Logout", "Gallery", "Videos", 
                    "Resources", "Contact Us", "Follow Us", "Feedback", 
                    "FAQ", "Terms and Conditions", "Privacy Policy"]
    return render_template("sitemap.html", message=message, sitemap=sitemap_data)


@app.route('/home', methods=["GET", "POST"])
def home():
    message = "Welcome to the Home Page!"
    if request.method == "POST":
        name = request.form.get("name")
        message = f"Hello, {name}! Welcome to the Home Page!"
    return render_template("home.html", message=message)

@app.route('/search', methods=["GET", "POST"])
def search():
    message = "Search"
    search_results = []
    if request.method == "POST":
        query = request.form.get("query")
        search_results = [f"Result 1 for '{query}'", f"Result 2 for '{query}'", f"Result 3 for '{query}'"]
        message = f"Search results for '{query}':"
    return render_template("search.html", message=message, search_results=search_results)

@app.route('/blog', methods=["GET"])
def blog():
    message = "Blog"
    return render_template("blog.html", message=message)

@app.route('/about-us', methods=["GET", "POST"])
def about():       
    message = "About Us"
    if request.method == "POST":
        name = request.form.get("name")
        message = f"Hello, {name}! Welcome to the About Us page!"
    return render_template("about.html", message=message)

@app.route('/services', methods=["GET"])
def services():
    message = "Our Services"
    services_data = ["Task Management", "Project Tracking", "Team Collaboration"]
    return render_template("services.html", message=message, services=services_data)


@app.route("/DevTasks", methods=["GET"])
def homepage():
    message = "Welcome to DevTasks!"
    return render_template("homepage.html", message=message)


@app.route('/create-task', methods=["GET", "POST"])
def create_task():
    message = "Create a new task!"
    if request.method == "POST":
        task_name = request.form.get("task_name")
        message = f"Task '{task_name}' has been created!"
    return render_template("create_task.html", message=message)

@app.route('/task-status', methods=["GET"])
def status():
    message = "Task Status"
    task_status = {"Task 1": "In Progress", "Task 2": "Completed", "Task 3": "Pending"}
    return render_template("task_status.html", message=message, task_status=task_status)


@app.route('/view-tasks', methods=["GET"])
def view_tasks():
    message = "Here are your tasks!"
    tasks = ["Task 1", "Task 2", "Task 3"]
    return render_template("view_tasks.html", message=message, tasks=tasks)


@app.route('/edit-tasks', methods=["GET", "POST"])
def edit_tasks():
    message = "Edit your tasks!"
    if request.method == "POST":
        task_id = request.form.get("task_id")
        new_task_name = request.form.get("new_task_name")
        message = f"Task '{task_id}' has been updated to '{new_task_name}'!"
    return render_template("edit_tasks.html", message=message)

@app.route('/update-tasks', methods=["GET", "POST"])
def update_tasks():
    message = "Update a task!"
    if request.method == "POST":
        task_id = request.form.get("task_id")
        new_status = request.form.get("new_status")
        message = f"Task '{task_id}' has been updated to status '{new_status}'!"
    return render_template("update_tasks.html", message=message)


@app.route('/delete-tasks', methods=["GET", "POST"])
def delete_tasks():
    message = "Delete a task!"
    if request.method == "POST":
        task_id = request.form.get("task_id")
        message = f"Task '{task_id}' has been deleted!"
    return render_template("delete_tasks.html", message=message)


@app.route('/task-priorities', methods=["GET"])
def priorities():
    message = "Task Priorities"
    task_priorities = {"Task 1": "High", "Task 2": "Medium", "Task 3": "Low"}
    return render_template("task_priorities.html", message=message, task_priorities=task_priorities)


@app.route('/task-categories', methods=["GET"])
def categories():
    message = "Task Categories"
    task_categories = {"Task 1": "Development", "Task 2": "Testing", "Task 3": "Documentation"}
    return render_template("task_categories.html", message=message, task_categories=task_categories)


@app.route('/task-types', methods=["GET"]) 
def task_types():
    message = "Task Types"
    task_types_data = {"Task 1": "Bug Fix", "Task 2": "Feature Development", "Task 3": "Documentation"}
    return render_template("task_types.html", message=message, task_types=task_types_data)

  
@app.route('/deadlines', methods=["GET"])
def deadlines():
    message = "Deadlines"
    deadlines_data = {"Task 1": "2023-12-31", "Task 2": "2023-11-30", "Task 3": "2023-10-31"}
    return render_template("deadlines.html", message=message, deadlines=deadlines_data)


@app.route('/updates', methods=["GET"])
def updates():
    message = "Updates"
    updates_data = ["Update 1: Task 1 is in progress", "Update 2: Task 2 has been completed", "Update 3: Task 3 is pending"]
    return render_template("updates.html", message=message, updates=updates_data)


@app.route('/timeline', methods=["GET"])
def timeline():
    message = "Timeline"
    timeline_data = ["2023-01-01: Project started", "2023-02-01: First milestone achieved", "2023-03-01: Second milestone achieved"]
    return render_template("timeline.html", message=message, timeline=timeline_data)


@app.route('/accomplishments', methods=["GET"])
def progress():
    message = "Accomplishments"
    accomplishments_data = ["Accomplishment 1: Task 1 completed", "Accomplishment 2: Task 2 completed", "Accomplishment 3: Task 3 completed"]
    return render_template("accomplishments.html", message=message, accomplishments=accomplishments_data)

@app.route('/dashboard', methods=["GET"])
def dashboard():
    message = "Dashboard"
    dashboard_data = {"Total Tasks": 100, "Completed Tasks": 70, "Pending Tasks": 30}
    return render_template("dashboard.html", message=message, dashboard=dashboard_data)

@app.route('/team-collaboration', methods=["GET"])
def collaboration():
    message = "Team Collaboration"
    team_collaboration_data = ["Collaboration 1: Task 1 assigned to Alice", "Collaboration 2: Task 2 assigned to Bob", "Collaboration 3: Task 3 assigned to Charlie"]
    return render_template("collaboration.html", message=message, team_collaboration=team_collaboration_data)

@app.route('/collaboration-tools', methods=["GET"])
def collaboration_tools():
    message = "Collaboration Tools"
    collaboration_tools_data = ["Tool 1: Slack", "Tool 2: Trello", "Tool 3: Asana"]
    return render_template("collaboration_tools.html", message=message, collaboration_tools=collaboration_tools_data)

@app.route('/project-tracking', methods=["GET"])
def tracking():
    message = "Project Tracking"
    project_tracking_data = ["Project 1: 50% complete", "Project 2: 75% complete", "Project 3: 25% complete"]
    return render_template("tracking.html", message=message, project_tracking=project_tracking_data)

@app.route('/analytics', methods=["GET"])
def analytics():
    message = "Analytics"
    analytics_data = {"Total Tasks": 100, "Completed Tasks": 70, "Pending Tasks": 30}
    return render_template("analytics.html", message=message, analytics=analytics_data)

@app.route('/reports', methods=["GET"])
def reports():
    message = "Reports"
    reports_data = ["Report 1: Weekly Summary", "Report 2: Monthly Summary", "Report 3: Yearly Summary"]
    return render_template("reports.html", message=message, reports=reports_data)

@app.route('/notifications', methods=["GET"])
def notifications():
    message = "Notifications"
    notifications_data = ["Notification 1: Task 1 is due tomorrow", "Notification 2: Task 2 has been completed", "Notification 3: Task 3 is pending"]
    return render_template("notifications.html", message=message, notifications=notifications_data)

@app.route('/calendar', methods=["GET"])
def calendar():
    message = "Calendar"
    calendar_data = {"2023-12-31": "Task 1 deadline", "2023-11-30": "Task 2 deadline", "2023-10-31": "Task 3 deadline"}
    return render_template("calendar.html", message=message, calendar=calendar_data)

@app.route('/documents', methods=["GET"])
def documents():
    message = "Documents"
    documents_data = ["Document 1: Project Plan", "Document 2: Design Specifications", "Document 3: User Manual"]
    return render_template("documents.html", message=message, documents=documents_data)

@app.route('/notes', methods=["GET"])
def notes():
    message = "Notes"
    notes_data = ["Note 1: Remember to review the project plan", "Note 2: Schedule a meeting with the team", "Note 3: Update the task status"]
    return render_template("notes.html", message=message, notes=notes_data)

@app.route('/logout', methods=["GET"])
def logout():
    message = "You have been logged out."
    return render_template("logout.html", message=message)  


@app.route('/gallery', methods=["GET"])
def gallery():
    message = "Gallery"
    gallery_images = ["image1.jpg", "image2.jpg", "image3.jpg"]
    return render_template("gallery.html", message=message, gallery_images=gallery_images)

@app.route('/videos', methods=["GET"])
def videos():
    message = "Videos"
    videos_data = ["video1.mp4", "video2.mp4", "video3.mp4"]
    return render_template("videos.html", message=message, videos=videos_data)

@app.route('/resources', methods=["GET"])
def resources():  
    message = "Resources"
    resources_data = ["Resource 1: DevTasks Documentation", "Resource 2: DevTasks API Reference", "Resource 3: DevTasks Support"]
    return render_template("resources.html", message=message, resources=resources_data)

@app.route('/contact-us', methods=["GET"])
def customer_support():
    message = "Contact Us"  
    contact_info = {"Email": "contact@devtasks.com", "Messenger": "DevTasks Messenger"}
    return render_template("contact_us.html", message=message, contact_info=contact_info)

@app.route('/follow-us', methods=["GET"])
def contacts():
    message = "Follow Us"
    social_media_links = {"Facebook": "https://www.facebook.com/devtasks", "Instagram": "https://www.instagram.com/devtasks"}
    return render_template("contacts.html", message=message, social_media_links=social_media_links)

@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    message = "Feedback"
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        message = f"Thank you for your feedback: '{feedback_text}'!"
    return render_template("feedback.html", message=message)

@app.route('/faq', methods=["GET"])
def faq():
    message = "Frequently Asked Questions"
    faq_data = {"Question 1": "How do I create a task?", "Answer 1": "Go to the Create Task page and fill out the form.", 
                "Question 2": "How do I update a task?", "Answer 2": "Go to the Update Tasks page and fill out the form.", 
                "Question 3": "How do I delete a task?", "Answer 3": "Go to the Delete Tasks page and fill out the form."}
    return render_template("faq.html", message=message, faq=faq_data)

@app.route('/terms', methods=["GET"])
def terms():
    message = "Terms and Conditions"
    terms_data = ["Term 1: Use of DevTasks is subject to our terms and conditions.", 
                  "Term 2: We are not responsible for any data loss or damage.", 
                  "Term 3: By using DevTasks, you agree to our privacy policy."]
    return render_template("terms.html", message=message, terms=terms_data)

@app.route('/privacy', methods=["GET"])
def privacy():
    message = "Privacy Policy"
    privacy_data = ["Privacy Policy 1: We collect user data to improve our services.", 
                    "Privacy Policy 2: We do not share user data with third parties.", 
                    "Privacy Policy 3: By using DevTasks, you consent to our privacy policy."]
    return render_template("privacy.html", message=message, privacy=privacy_data)


if __name__ == "__main__":
    app.run(debug=True)