![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)
# [Ironhack](https://www.ironhack.com/pt-en) Data Analytics Bootcamp 2024 - Final Project
Welcome to my GitHub repository showcasing the final project I completed as part of the Data Analytics bootcamp at Ironhack, where I underwent six months of intensive training in data analytics, mastering foundational skills, programming proficiency, machine learning techniques, and project-based learning.

The culmination of this bootcamp is showcased in my final project, where I tackled a real-world problem using the skills and techniques acquired throughout the course.


# The Project 
<p align="center">
  <img width="300" height="auto" src="https://github.com/jantzla/Final-Project-Ironhack-2024/blob/main/Website/static/images/logo.png">
  </p>

## Introduction
In the ever-evolving landscape of scientific research, efficiency and accuracy are paramount. Researchers, students, and professionals in laboratories are constantly seeking innovative ways to streamline their workflows and enhance productivity without compromising the integrity of their work. Recognising this need, my project **NoteWhisperer** emerges as a transformative solution aimed at revolutionising the way experimental protocols and lab notes, particularly handwritten ones, are accessed and utilised during experiments.

Handwritten notes and protocols are an integral part of daily laboratory work. They often contain critical information and data recorded in real-time. However, referencing these handwritten notes during experiments poses a significant challenge, especially when maintaining a sterile lab environment is crucial. Physical handling of documents or electronic devices can lead to contamination risks, interrupting the workflow and potentially compromising experimental results.

**NoteWhisperer** is designed as a digital lab assistant that leverages the power of voice recognition to provide hands-free access to lab notes and protocols. This innovative tool is specifically developed to address the unique challenges of working with handwritten notes in the laboratory setting. By converting text-based and handwritten protocols into audible formats, NoteWhisperer enables researchers to voice-control the playback of their notes, ensuring they can remain focused on their experiments without the need to physically interact with their notes. This advancement offers a seamless, efficient, and safer way to access vital information, thereby enhancing the overall laboratory experience.

## Techniques and Tools Used in NoteWhisperer

### Google Cloud-Vision API
+ For the optical character recognition (OCR) process, NoteWhisperer utilizes Google Cloud Vision API.
+ This powerful tool extracts text from images and PDF files uploaded by the users.
+ The API's robust OCR capabilities ensure that even handwritten notes can be accurately transcribed into digital text.

### Google Cloud Text-to-Speech API
+  After the transcription process, NoteWhisperer leverages Google Cloud Text-to-Speech API to convert the digital text into natural-sounding speech.
+  This API supports various languages and voices, providing a customizable experience for the user.
+  The choice of voice gender and other attributes can be selected directly through the web interface, thanks to the flexibility offered by this API.

### Flask Framework
+ The backbone of NoteWhisperer is built using Flask, a lightweight WSGI web application framework in Python. Flask facilitated the creation of a web interface that allows users to interact with the application seamlessly.
+ By employing Flask, I was able to develop a user-friendly platform for uploading documents, viewing transcriptions, and listening to audio outputs.

### HTML/CSS/JavaScript
+ The client-side of NoteWhisperer is designed with HTML, CSS, and JavaScript, ensuring a responsive and intuitive user interface.
+ This [Bootstrap](https://bootswatch.com/quartz/) is used to enhance the UI design, making it accessible and aesthetically pleasing across different devices and screen sizes.

![image](https://github.com/jantzla/Final-Project-Ironhack-2024/assets/145261891/f8ad42d9-7d32-4692-bebe-2b62b8e1c2b4)


## Additional Notes
+ The web application allows the user only to uplaod image files (png, jpg) or pdf-files.
+ The user can easily upload several file at the same time (max 5) if the notes or protocols take up more than one page. For the this scenario it is important that the user specifies which audio files he wants to 'play'. For 'pausing' or 'stopping' the application will recognise which audio is currently running and will perform the action accordingly.
+ In order to assess the accuracy of the uploaded transcript, the 'Confidence Score' shows the user it's certainty about the correct transcription of the handwritten notes.

<p align="center">
  <img width="400" height="auto" src="https://github.com/jantzla/Final-Project-Ironhack-2024/blob/main/Website/static/images/dummy_logo.png">
  </p>
