import flet as ft # GUI library
import yt_dlp
import requests # used to check if url is valid
from bs4 import BeautifulSoup # used to get thumbnail from video URL
import os
from PIL import Image
import re

pathLists = ["downloads", "downloads/temp"]
for i in pathLists:
    if not os.path.exists(i):
        os.makedirs(i)
    else:
        try:
            # for each file in temp folder, delete it
            for file in os.listdir(pathLists[1]):
                os.remove(os.path.join(pathLists[1], file))
        except:
            # delete the folder and recreate it
            os.rmdir(i)
            os.makedirs(i)
            
            
tempPath = pathLists[1] + "/thumbnail-"
videoURL = "" # Variable to store video URL
thumbnailURL = "" # Variable to store thumbnail URL
videoTitle = "" # Variable to store video title
downloadVariables = {"audio": False, "video": False, "resolution": ""}

def main(page: ft.Page): # Main function
    # Initialize the page settings
    page.title = "Video Downloader" # Set the page title
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    # Set the routes for the different pages
    def route_change(route):
        if page.route == "/": # main page
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.padding = 100 # Set the padding of the page
            mainPage(page)
            
        elif page.route == "/settings": # settings page
            page.vertical_alignment = ft.MainAxisAlignment.START
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.padding = 50 # Set the padding of the page
            downloadSettings(page)
            
        elif page.route == "/download": # download page
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.padding = 100 # Set the padding of the page
            download(page)
        page.update()
    
    page.on_route_change = route_change # Set the route change function
    page.go(page.route or "/") # Go to the main page
    
    
def mainPage(page: ft.Page):
    def submitButtonClick(e): # Function for button press
        # Get video URL from the input field
        global videoURL, thumbnailURL, tempPath, videoTitle
        videoURL = URLInput.value
        
        # Check if the URL is valid and get the thumbnail
        try:
            response = requests.get(videoURL) # Check if the URL is valid
            if response.status_code == 200: # If the URL is valid
                soup = BeautifulSoup(response.text, 'html.parser') # Get the thumbnail from the video URL
                thumbnailURL = soup.find('meta', property='og:image')['content'] # Get the thumbnail URL
                
                videoTitle = soup.find('meta', property='og:title')['content']
                            
                # Adds the temp path to a hash string of the video title to prevent duplicate file names
                tempPath = tempPath[:25] + str(hash(videoTitle))[1:] + ".jpg" 
                
                # Clear the previous thumbnail image
                if os.path.exists(tempPath):
                    os.remove(tempPath)
                    

                with open(tempPath, 'wb') as file:
                    file.write(requests.get(thumbnailURL).content)
                
                # Using pillow resize the image
                # Youtube thumbnail resolution is always 1280x720
                img = Image.open(tempPath)
                img.thumbnail((img.width / 2, img.height / 2)) # Output resolution 640x360
                img.save(tempPath)
                
                # Force the thumbnail to update
                page.update()

                page.route = "/settings"  # Change page to the settings page
                page.update()

            else: # If the URL is invalid
                errorBanner(f"URL is invalid. Status code: {response.status_code}")
        except requests.RequestException as e: # If an error occurred
            errorBanner(f"An error occurred: {e}")
                
    def errorBanner(message): # Function to display an error banner
        snackbar = ft.SnackBar( # Show a snackbar with the error message
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.show_snack_bar(snackbar)
        
    page.controls.clear()  # Clear the previous controls
    
    MainText = ft.Text("Video Downloader", size=50, height=100) # Create a text widget with the title
    URLInput = ft.TextField(label="Enter the URL", hint_text="Enter the URL of the video or playlist") # Create a text field widget for the URL input
    
    button = ft.ElevatedButton("Download", on_click=submitButtonClick) # Create a button widget to submit the URL
    page.add(MainText, URLInput, button) # Add the widgets to the page


def downloadSettings(page: ft.Page):
    def backButtonClick(e): # Function for the back button
        page.route = "/"  
        page.update()
        
    def downloadButtonClick(e): # Function for the download button
        global downloadVariables
        downloadVariables["audio"] = audioSelect.value
        downloadVariables["video"] = videoSelect.value
        downloadVariables["resolution"] = resolutionSelect.value
        
        page.route = "/download"
        page.update()
        
    def videoSelected(e): # Video quality selection
        isChecked = videoSelect.value  # Get the value of the master checkbox
        
        resolutionSelect.disabled = not isChecked  # Enable or disable the resolution dropdown based on the master checkbox
        audioSelect.value = False  # Enable or disable the audio checkbox based on the master checkbox
        downloadButton.disabled = not isChecked  # Enable or disable the download button based on the master checkbox
        page.update()
        
    def audioSelected(e):
        isChecked = audioSelect.value
        
        resolutionSelect.disabled = True
        videoSelect.value = False
        downloadButton.disabled = not isChecked
        
        page.update()
        
    page.controls.clear()  # Clear the previous controls
    
    # IMAGE AND TITLE
    thumbnailImage = ft.Image(src=tempPath) # Create an image widget with the thumbnail
    if "&list=" in videoURL: # If the URL is a playlist
        videoTitleText = ft.Text(f"[PLAYLIST] == {videoTitle}", size=20)
    else:
        videoTitleText = ft.Text(videoTitle, size=20)
        
    # VIDEO AND AUDIO SELECTION
    videoSelect = ft.Checkbox(label="Download Video", on_change=videoSelected)
    audioSelect = ft.Checkbox(label="Download Audio", on_change=audioSelected) # Select audio
    
    videoAudioRow = ft.Row([
        videoSelect,audioSelect
    ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)  # Adjust alignment properties as needed
    
    # VIDEO RESOLUTION
    resolutions = ["4k", "2k", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"] # Video resolutions
    options = [ft.dropdown.Option(resolution) for resolution in resolutions] # Create options for the dropdown
    resolutionSelect = ft.Dropdown( # Create the dropdown widget
        width=200, 
        options=options, 
        value="1080p", 
        disabled=True) # Create the dropdown widget
    
    # CREATE BUTTONS
    # Create a Row widget to contain the buttons horizontally
    buttonRow = ft.Row([
        ft.ElevatedButton(text="Go to Main Page", on_click=backButtonClick),
        (downloadButton := ft.ElevatedButton(text="Download", on_click=downloadButtonClick, disabled=True)) 
    ], alignment='center')


    page.add(thumbnailImage, videoTitleText)
    page.add(videoAudioRow, resolutionSelect)
    page.add(buttonRow)
  
    
def download(page: ft.Page):
    cancelDownload = False
    def cancelButtonClick(e): 
        nonlocal cancelDownload
        cancelDownload = True
        
        page.route = "/"  # Set the route back to the main page
        page.update()
    
    def my_hook(d):
        nonlocal cancelDownload
        
        if "filename" in d: #Get filename
            filename = d['filename'].split("\\")[-1].split(".") # Delete file path and split the filename by "." 
            filename = filename[0] + "." + filename[2] # Concatenate the filename and extension chunks
        
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') # Get total size of the download
            downloaded_bytes = d.get('downloaded_bytes', 0) # Get amount currently downloaded
            
            if total_bytes and downloaded_bytes: # If the total size and amount downloaded are available
                completionDecimal = downloaded_bytes / total_bytes # Calculate the completion percentage as decimal
                print(f" - download progress: {completionDecimal:.2f}")  # Display with 4 decimal places for precision
                loadingBar.value = completionDecimal # Update the progress bar with the completion percentage
                downloadingText.value = f"{filename} - {completionDecimal:.2%}" # Add a text widget to the page
                page.update() # Update the progress bar with the completion percentage             
                        
        elif d['status'] == 'finished': # If the download is finished
            if filename.split(".")[1] == "mp4":
                completedText.value = f"Successfully downloaded video - {filename.split(".")[0]}" 
            else:
                completedText.value = f"Successfully downloaded audio - {filename.split(".")[0]}"
        
        if cancelDownload == True:
            raise Exception("Download Cancelled")
        
        
    page.controls.clear()  # Clear the previous controls
    value = "Starting Download..."
    value2 = ""
    
    downloadingText = ft.Text(value, size=20) # Create a text widget to display the download status
    loadingBar = ft.ProgressBar(width=800, height=10) # Create a progress bar widget
    completedText = ft.Text(value2, size=20) # Create a text widget to display the download status
    cancelButton = ft.ElevatedButton("Cancel", on_click=cancelButtonClick) # Create a button widget to cancel the download
    
    
    page.add(ft.Column([downloadingText, loadingBar]))
    page.add(completedText, cancelButton) # Add the button to the page
    
    
    if downloadVariables["audio"] == True:
        AorV = "bestaudio[ext=m4a]/bestaudio"
    else:
        AorV = f"bestvideo[height<={downloadVariables['resolution']}][ext=mp4]+bestaudio[ext=m4a]/best"

    ydl_opts = {
        'no_warnings': True,  # Suppress all warning messages
        'noplaylist': False,  # Download just the video, if the URL refers to a video and a playlist.
        'quiet': True,  # Do not print messages to stdout.
        'format': AorV,  # Choice of quality.
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Name the file the ID of the video
        'restrictfilenames': True,  # Restrict filenames to only ASCII characters, and avoid "&" and spaces in filenames
        'nooverwrites': True,  # Prevent overwriting files.
        'continuedl': True,  # Force resume of partially downloaded files.
        'progress_hooks': [my_hook],  # Directly pass the function without lambda
    }
                
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
        try:
            ydl.download([videoURL])
        except Exception as e:
            print(e)
             

# BUG
# When a file with the same name is going to be downloaded it doesnt download and is marked as complete even though it didnt download
# If the last download is has the same name as a file already downloaded it will be marked as complete by yt_dlp yet theres no GUI prompt for it
# Can check yt_dlp callouts with CLI version

# Temp playlist - https://www.youtube.com/watch?v=_YfqYB-m1AM&list=PL4b6-i5pR3IKwG4X9svp4F8Kf9PuUmM3p
ft.app(main)