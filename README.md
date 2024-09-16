# This project aims to improve my college's library

My library needs the student ID to grant access to books and laptops, but it’s really common for students to forget it since it's such a long number (like `123123213123`). To recover it, they have to ask the staff to print a paper with their ID on it.

So... What's the best way to improve a human process? Automatize it! That's exactly what we're doing here. The core project is to create a Face Recognition model to `recognize` (of course) all students by their _beautiful faces_ and avoid that boring and energy-wasting problem about memorizing that huge student ID number.

## Updates

- The first two weeks of this project were mainly spent looking for and reading documentation about how to create this `Face recognition model`. I started programming a sample with local images and an MVP code with a lot of room for improvement. (08/13 -> 08/28)
- At this moment, our group of researchers are interviewing our college's staff to understand the pain of this process and validate our project to actually help both students and labors. We've reached a decent amount of awnsers and a positive feedback to continue our project. (08/29 -> 09/13)
- Starting at 2nd week of September, I've started creating an API using `FastAPI` and a DataBase using `SQLite`, the respective archives are `api.py`, `schemas.py`, ` models.py` and `database.py`. Also, I've created a _React_ app aiming to livestream the Face Detection's output
