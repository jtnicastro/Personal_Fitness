# Personal Fitness
PersonalFit is a comprehensive Django-based web application designed to enhance the connection between personal trainers and clients. This platform provides an all-in-one solution for managing workouts, tracking nutrition plans, communicating in real-time, and monitoring physical metrics.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
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
+ **Pagination and Search:**Easily navigate through data with paginated lists and search functionality to quickly find workouts, nutrition plans, or messages.
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
    lifting-log/
    │
    ├── app.py            # Main application file
    ├── forms.py          # Form classes for Flask-WTF
    ├── models.py         # Database models
    ├── views.py          # View functions
    ├── templates/        # HTML templates
    │   ├── base.html
    │   ├── alt_base.html
    │   ├── home.html
    │   ├── addExercise.html
    │   ├── entries.html
    │   ├── analyze.html
    │   └── register.html
    ├── static/           # Static files (CSS, JS, Images)
    │   └── theme.css
    ├── requirements.txt  # Requirements file
    └── README.md         # This README file 
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


