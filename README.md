# Segregation-and-analysis-of-multimedia (Cyber Forensic Tool)
This is a cyber forensic tool build by me and my team during the internship at CID gov of Karnataka we are keeping this open to use and dev 


This project is a web-based cyber forensic tool designed to analyze and categorize images extracted from forensic dumps. The tool can process standard forensic dump formats like E01, RAW, and DD, utilizing Scalpel and Foremost for image carving.

## Features

- **Forensic Dump Support**: Process forensic dumps in E01, RAW, and DD formats.
- **Image Carving**: Extract images and photos from forensic dumps using Scalpel and Foremost.
- **Image Categorization**: Classify images into user-defined categories (e.g., narcotics, weapons) using machine learning models.
- **Search Faces by Image**: You can get all the similar faces from the database that look alike by dragging and dropping a sample photo of the person who you want to look up
- **Time Line view**: The app is capable of separating images that have metadata and the once that don't have metadata and based on the meta data it divides the images into 3 categories as shown in the fig
  
<img src="images/Timeline.jpg" alt="Time Line" width="400"/>

## Project Structure

The project consists of two main folders:

- **`frontend`**: Contains the React application for the user interface. Refer to the `README.md` in the `frontend` folder for setup and usage instructions.
- **`backend`**: Contains the backend code, which is designed to run on Windows with WSL installed. Refer to the `README.md` in the `backend` folder for setup and usage instructions.

## Requirements

### Backend

- Windows OS with WSL installed
- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Frontend

- Node.js (version x.x.x)
- npm (version x.x.x)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
