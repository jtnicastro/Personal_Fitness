# Personal Fitness
PersonalFit is a comprehensive Django-based web application designed to enhance the connection between personal trainers and clients. This platform provides an all-in-one solution for managing workouts, tracking nutrition plans, communicating in real-time, and monitoring physical metrics.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demonstrations](#demonstrations)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Overview

The PersonalFit application allows trainers to manage their clients’ workout routines, nutrition plans, and physical metrics. With real-time communication and interactive features, this application is ideal for trainers and clients looking for a streamlined, interactive fitness management experience.

## Features
### User Management
+ **User Authentication:** Secure login and logout functionality, with distinct roles for clients and trainers.
+ **Separate User Experiences:** Different data is displayed depending on the type of user (client or trainer) for a customized experience.
+ **Profile Management:** Both clients and trainers can update their profiles with relevant information.

### Workout Tracking
+ **Customizable Workout Plans:** Trainers can create personalized workout routines for each client, logging workouts with details like sets, reps, and weights.
+ **Weekly Scheduling:** Trainers can assign specific workouts for each day, allowing clients to follow structured plans.
+ **Exercise Database Integration:** The app integrates with an external exercise API to fetch and display exercise information, enhancing workout variety.

### Nutrition Management
+ **Meal Plans:** Trainers can create and assign meal plans to clients, including dietary recommendations tailored to client needs.
+ **Downloadable Plans:** Nutrition and workout plans can be converted into PDFs and downloaded for offline use.

### Physical Metrics Monitoring
+ **Client Metrics:** Track metrics such as weight, height, and other physical attributes to monitor client progress over time.

### Real-Time Communication
+ **In-App Messaging:** Real-time chat functionality between trainers and clients, facilitating instant feedback and guidance.

### Additional Features
+ **Pagination and Search:** Easily navigate through data with paginated lists and search functionality to quickly find workouts, nutrition plans, or messages.
+ **Image Upload:** Allows clients and trainers to upload images, providing visual progress tracking or additional details to support training.
+ **PDF Generation:** Generate and download personalized nutrition and workout plans as PDFs.


## Installation


1. **Clone the Repository:**
    ```bash
    git clone https://github.com/jtnicastro/lifting-log.git
    cd lifting-log
    ```

2. **Install the Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

* **Trainers:** Manage clients, assign workouts and nutrition plans, track progress, and provide real-time support through messaging.
* **Clients:** View assigned workouts and meal plans, log physical metrics, download PDF plans, and communicate directly with their trainer.


## Demonstraction
![add_workout](https://github.com/jtnicastro/lifting_log/blob/master/screenshots/add_workout.JPG)
![entries](https://github.com/jtnicastro/lifting_log/blob/master/screenshots/entries.JPG)
![analyze](https://github.com/jtnicastro/lifting_log/blob/master/screenshots/analyze.JPG) 

## Project Structure
```bash
    # PersonalFit_project Structure

PersonalFit_project/
├── __init__.py              # Initialization file for the Django project
├── asgi.py                  # ASGI configuration for async support
├── settings.py              # Project-wide settings and configuration
├── urls.py                  # URL routing for the project
├── wsgi.py                  # WSGI configuration for deployment
├── templates/               # Project-wide HTML templates
│
├── nutritionApp/            # App for managing nutrition plans
│   ├── __init__.py
│   ├── admin.py             # Admin configuration for nutrition models
│   ├── apps.py              # App configuration file
│   ├── forms.py             # Forms for nutrition data input
│   ├── models.py            # Database models for nutrition
│   ├── tests.py             # Unit tests for the nutrition app
│   ├── urls.py              # URL routing for nutrition views
│   ├── views.py             # View logic for handling nutrition pages
│   ├── migrations/          # Database migrations for the nutrition app
│   └── templates/           # Nutrition-related templates
│       └── nutritionApp/
│           ├── addMeal.html
│           ├── editMeal.html
│           ├── index.html
│           ├── meal_plan.html
│           └── nutritionPage.html
│
├── updateApp/               # App for managing client updates like weight and height
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   └── templates/           # Update-related templates
│       └── updateApp/
│           ├── index.html
│           └── updatePage.html
│
├── users/                   # App for user registration, authentication, and profile management
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── static/              # Static files for the users app
│   │   └── users/
│   │       ├── style.css
│   │       ├── styles.css
│   │       ├── tw.css
│   │       └── images/
│   │           └── fitness_logo.png
│   └── templates/           # User-related templates
│       └── users/
│           ├── base.html
│           ├── edit.html
│           ├── index.html
│           ├── login.html
│           ├── logout.html
│           ├── password_change_done.html
│           ├── password_change_form.html
│           ├── password_reset_complete.html
│           ├── password_reset_confirm.html
│           ├── password_reset_done.html
│           ├── password_reset_form.html
│           ├── register.html
│           └── register_done.html
│
├── workoutApp/              # App for workout planning and tracking
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── static/              # Static files for the workout app
│   │   └── workoutApp/
│   │       ├── style.css
│   │       └── images/
│   │           ├── add_icon.png
│   │           └── trash_icon.png
│   └── templates/           # Workout-related templates
│       └── workoutApp/
│           ├── addWorkout.html
│           ├── editSchedule.html
│           ├── editWorkout.html
│           ├── exerciseDetails.html
│           ├── exerciseList.html
│           ├── exerciseList_bodypart.html
│           ├── index.html
│           ├── workoutPage.html
│           └── workoutPlan.html
│
├── uploads/                 # Directory for storing uploaded files, such as progress images
│   ├── BodyPic1.png
│   ├── BodyPic2.png
│   ├── BodyPic3.png
│   ├── progressPic1.png
│   ├── progressPic2.png
│   └── Updates1.png
└── README.md                # Project README file

```
## Technologies Used
+ **Python:** Backend logic using Flask.
+ **Backend:** Django, Django Channels
+ **Frontend:** HTML, CSS, JavaScript
+ **Database:** SQLite (default, configurable to PostgreSQL or MySQL)
* **Libraries:** 
    * Matplotlib for data visualization
    * Pdfkit for report generation
## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.tldrlegal.com/license/mit-license) file for details.


