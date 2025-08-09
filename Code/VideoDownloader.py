import flet as ft # GUI library
from bs4 import BeautifulSoup # Used to get thumbnail from video URL
from PIL import Image # Used to resize the thumbnail
from moviepy.editor import VideoFileClip, AudioFileClip # Used to merge video and audio (Using outdated version for no ffmpeg)
import yt_dlp, os, requests, shutil # Video downloader library, os library, requests library
from mutagen.mp4 import MP4 # Used to edit metadata


# Create necessary folders if they don't exist
pathLists = ["downloads/", "downloads/temp/"] # List of paths to create
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

# Global variables          
videoURL = "" # Variable to store video URL
thumbnailURL = "" # Variable to store thumbnail URL
videoTitle = "" # Variable to store video title
thumbnailPath = "" # Variable to store thumbnail path
downloadConfigData = {"format": "", "resolution": "", "metadata": False, 
                      "metaAlbum": "", "metaTrackNumber": False, "metaArtist": "", 
                      "metaComposer": "", "metaLyricists": "", "metaGenre": "", 
                      "metaYear": ""} # Dictionary to store download configuration data

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
        global videoURL, thumbnailURL, videoTitle, thumbnailPath
        videoURL = URLInput.value # gets value from text box and assigns to videoURL
        
        # Check if the URL is valid and get the thumbnail
        try:
            response = requests.get(videoURL) # Check if the URL is valid
            if response.status_code == 200: # If the URL is valid
                soup = BeautifulSoup(response.text, 'html.parser') # Get the thumbnail from the video URL
                thumbnailURL = soup.find('meta', property='og:image')['content'] # Get the thumbnail URL
                
                videoTitle = soup.find('meta', property='og:title')['content']
                            
                # Adds the temp path to a hash string of the video title to prevent duplicate file names
                thumbnailPath = f"{pathLists[1]}thumbnail-{str(hash(videoTitle))[1:]}.jpg"
                
                # Clear the previous thumbnail image if it already exists
                if os.path.exists(thumbnailPath):
                    os.remove(thumbnailPath)
                    

                with open(thumbnailPath, 'wb') as file:
                    file.write(requests.get(thumbnailURL).content)
                
                # Using pillow resize the image
                # Youtube thumbnail resolution is always 1280x720
                img = Image.open(thumbnailPath)
                img.thumbnail((img.width / 2, img.height / 2)) # Output resolution 640x360
                img.save(thumbnailPath)
                
                # Force the thumbnail to update
                page.update()

                page.route = "/settings"  # Change page to the settings page
                page.update()

            else: # If the URL is invalid
                errorBanner(f"URL is invalid. Status code: {response.status_code}")
        # invalid URL
        except requests.exceptions.MissingSchema: # If the URL is invalid
            errorBanner("Please enter a URL starting with 'http' or 'https'")
        except TypeError: # If the URL is invalid
            errorBanner("Please enter a valid URL.")
        except Exception as e:
            errorBanner(f"An error occurred: {e}")
                
    def errorBanner(message): # Function to display an error banner
        snackbar = ft.SnackBar( # Show a snackbar with the error message
            content=ft.Text(message, color=ft.Colors.WHITE, size=20),
            bgcolor=ft.Colors.RED
        )
        page.open(snackbar)
        
    page.controls.clear()  # Clear the previous controls
    
    mainText = ft.Text("Video Downloader", size=50, height=100) # Create a text widget with the title
    URLInput = ft.TextField(label="Enter the URL", hint_text="Enter the URL of the video or playlist") # Create a text field widget for the URL input
    
    submitButton = ft.ElevatedButton("Download", on_click=submitButtonClick) # Create a button widget to submit the URL
    page.add(mainText, URLInput, submitButton) # Add the widgets to the page


def downloadSettings(page: ft.Page):
    def backButtonClick(e): # Function for the back button
        page.route = "/"  
        page.update()
        
    def downloadButtonClick(e): # Function for the download button
        global downloadConfigData
        
        # Check the format and resolution and save to ddowloadConfigData
        downloadConfigData["format"] = videoAudioSelect.value
        downloadConfigData["resolution"] = resolutionSelect.value
        downloadConfigData["metadata"] = customMetadata.value
        downloadConfigData["metaAlbum"] = metaAlbumInput.value
        downloadConfigData["metaTrackNumber"] = metaTrackNumberInput.value
        downloadConfigData["metaArtist"] = metaArtistInput.value
        downloadConfigData["metaComposer"] = metaComposerInput.value
        downloadConfigData["metaLyricists"] = metaLyricistsInput.value 
        downloadConfigData["metaGenre"] = metaGenreInput.value
        downloadConfigData["metaYear"] = metaYearInput.value

        page.route = "/download"
        page.update()
    
    def formatSelectClick(e):
        videoAudio = videoAudioSelect.value # Get the selected value from the dropdown
        downloadButton.disabled = False # Enable the download button
        
        if videoAudio == "Video": # If the selected value is video
            resolutionSelect.disabled = False # Enable the resolution dropdown
        elif videoAudio == "Audio": # If the selected value is audio
            resolutionSelect.disabled = True # Disable the resolution dropdown
            
        page.update()
    
    def metadataButtonClick(e):
        metaAlbumInput.disabled = not metaAlbumInput.disabled # Enable or disable the album input field
        metaTrackNumberInput.disabled = not metaTrackNumberInput.disabled # Enable or disable the track number input field
        metaArtistInput.disabled = not metaArtistInput.disabled # Enable or disable the artist input field
        metaComposerInput.disabled = not metaComposerInput.disabled # Enable or disable the composer input field
        metaLyricistsInput.disabled = not metaLyricistsInput.disabled # Enable or disable the lyricists input field
        metaGenreInput.disabled = not metaGenreInput.disabled # Enable or disable the genre input field
        metaYearInput.disabled = not metaYearInput.disabled # Enable or disable the year input field
        
        page.update()
        
        
    page.controls.clear()  # Clear the previous controls
    
    # IMAGE AND TITLE
    thumbnailImage = ft.Image(src=thumbnailPath) # Create an image widget with the thumbnail
    if "&list=" in videoURL: # If the URL is a playlist
        videoTitleText = ft.Text(f"[PLAYLIST] == {videoTitle}", size=20)
    else: # If the URL is a video
        videoTitleText = ft.Text(videoTitle, size=20)
        
    # VIDEO AND AUDIO SELECTION
    videoAudioOptions = [ft.dropdown.Option(videoAudio) for videoAudio in ["Audio", "Video"]] # Video and Audio options
    videoAudioSelect = ft.Dropdown(
        width=200, 
        options=videoAudioOptions, 
        label="Select Format", 
        disabled=False,
        on_change=formatSelectClick)  # Create the dropdown widget

    # VIDEO RESOLUTION
    resolutions = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"] # Video resolutions
    resolutionOptions = [ft.dropdown.Option(resolution) for resolution in resolutions] # Create options for the dropdown
    resolutionSelect = ft.Dropdown( # Create the dropdown widget
        width=200, 
        options=resolutionOptions, 
        value="1080p", 
        disabled=True) # Create the dropdown widget
    
    # CUSTOM METADATA
    customMetadata = ft.Checkbox(label="Custom Metadata", width=20, on_change=metadataButtonClick) # Toggle to enable or disable metadata
    metaAlbumInput = ft.TextField(label="Album Name", width=200, disabled=True) # Create a text field widget for the album name
    metaTrackNumberInput = ft.Checkbox(label="Track Numbers", width=200, disabled=True) # Create a checkbox widget for the track number
    metaArtistInput = ft.TextField(label="Artist Name", width=200, disabled=True) # Create a text field widget for the artist name
    metaComposerInput = ft.TextField(label="Composer Name", width=200, disabled=True) # Create a text field widget for the composer name
    metaLyricistsInput = ft.TextField(label="Lyricists Name", width=200, disabled=True) # Create a text field widget for the lyricists name
    metaGenreInput = ft.TextField(label="Genre", width=200, disabled=True) # Create a text field widget for the genre
    metaYearInput = ft.TextField(label="Year", width=200, disabled=True) # Create a text field widget for the year

    # Uses a nested columns in a row to align the settings
    formatResolutionRow = ft.Row(
        [ft.Column([videoAudioSelect, resolutionSelect]),
         ft.Column([customMetadata, metaAlbumInput]), 
         ft.Column([metaTrackNumberInput, metaArtistInput]),
         ft.Column([metaComposerInput, metaLyricistsInput]),
         ft.Column([metaGenreInput, metaYearInput])], 
         alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER) # Adjust alignment properties as needed
    
    
    # CREATE BUTTONS
    # Create a Row widget to contain the buttons horizontally
    buttonRow = ft.Row([
        ft.ElevatedButton(text="Back to Main Menu", on_click=backButtonClick),
        (downloadButton := ft.ElevatedButton(text="Download", on_click=downloadButtonClick, disabled=True)) 
    ], alignment='center')


    page.add(thumbnailImage, videoTitleText)
    page.add(formatResolutionRow)
    page.add(buttonRow)
  
    
def download(page: ft.Page):
    cancelDownload = False
    def cancelButtonClick(e): 
        nonlocal cancelDownload
        cancelDownload = True
        
        page.route = "/"  # Set the route back to the main page
        page.update()
        
    def errorBanner(message): # Function to display an error banner
        snackbar = ft.SnackBar( # Show a snackbar with the error message
            content=ft.Text(message, color=ft.Colors.WHITE, size=20),
            bgcolor=ft.Colors.RED
        )
        page.open(snackbar)
    
    def finishedDownload():
        # Change the download status to finished
        downloadingText.value = "Download Finished"
        downloadingText.size = 30
          
        loadingBarContainer.content = loadingBar # Change the color of the progress bar
        loadingBar.color = ft.Colors.GREEN
        loadingBar.value = 1 # Set the progress bar to 100% (used for when downloads are skipped)
        
        # Enable the finished button and disable the cancel button
        finishedButton.disabled = False
        cancelButton.disabled = True
        downloadingText.value = "Download Finished"
        downloadingText.size = 30
          
        loadingBarContainer.content = loadingBar # Change the color of the progress bar
        loadingBar.color = ft.Colors.GREEN
        loadingBar.value = 1 # Set the progress bar to 100% (used for when downloads are skipped)
        
        # Enable the finished button and disable the cancel button
        finishedButton.disabled = False
        cancelButton.disabled = True
        
        
    fileName = "" # Variable to store the file name
    audioFile = "" # Variable to store the audio file
    downloadIndex = 0 # Variable to store the download index
    
    def my_hook(d):
        nonlocal cancelDownload 
        nonlocal fileName
        nonlocal audioFile
        nonlocal filesDownloaded
        nonlocal downloadIndex
        
        if cancelDownload == True: # If the cancel button was pressed
            raise Exception("Download Cancelled") # Raise an exception to stop the download
        
        if "filename" in d: #Get filename
            fileName = os.path.basename(d['filename']).split(".") # Split the file name by "."
            fileExtention = fileName[len(fileName)-1] # Get the file extension
            fileName = ".".join(fileName[:-1]) # rejoin the file name without the extension
        
        # During Download
        if d['status'] == 'downloading':
            totalBytes = d.get('total_bytes_estimate') # Get total size of the download
            downloadedBytes = d.get('downloaded_bytes', 0) # Get amount currently downloaded
            
            if totalBytes and downloadedBytes: # If the total size and amount downloaded are available
                completionDecimal = downloadedBytes / totalBytes # Calculate the completion percentage as decimal
                print(f" - download progress: {completionDecimal:.2f}")  # Display with 2 decimal places for precision
                loadingBar.value = completionDecimal # Update the progress bar with the completion percentage
                downloadingText.value = f"Downloading...   {completionDecimal:.2%}\n{fileName}.{fileExtention}" # Add a text widget to the page
        
        # The download will always download video then audio
        # If its downloading video it will attempt to merge the audio with it before the next download
        # When Download is Finished                
        elif d['status'] == 'finished': # If the download is finished
            if fileExtention == "mp4":
                if altMode == True: # If the download is in alt mode
                    completedText.value = f"Downloaded (1/2) - {fileName}" # Display the partial completion message
                else: # Display the completion message
                    completedText.value = f"Downloaded - {fileName}" # Display the completion message
            elif fileExtention == "m4a":
                completedText.value = f"Downloaded - {fileName}" # Display the completion message
                page.update() # Update the page
                downloadIndex += 1 # Increment the download index
                
                if altMode == True:           
                    downloadingText.value = "Merging Audio and Video\nPlease wait..." # Change the download status to merging audio and video
                    loadingBarContainer.content = ft.ProgressBar(width=1000, height=10, color=ft.Colors.BLUE) # Change the color of the progress bar
                    page.update() # Update the page
                    
                    # Load video and audio
                    audio = AudioFileClip((audioFile := f"{pathLists[0]}{fileName}.m4a"))
                    video = VideoFileClip((videoFile := f"{pathLists[0]}{fileName}.mp4"))
                    
                    videoWithAudio = video.set_audio(audio) # Merge video and audio
                    videoWithAudio.write_videofile(videoFile, codec='libx264', audio_codec='aac') # Write the video file

                    loadingBarContainer.content = loadingBar
                
                # If metadata is enabled
                if downloadConfigData["metadata"] == True:
                    temp = f"{pathLists[0]}{fileName}.{fileExtention}"
                    downloadedFile = MP4(temp) # Open the downloaded file
                    downloadedFile['\xa9alb'] = downloadConfigData["metaAlbum"] # Set the album metadata
                    downloadedFile['\xa9ART'] = downloadConfigData["metaArtist"] # Set the artist metadata
                    downloadedFile['\xa9wrt'] = downloadConfigData["metaComposer"] # Set the composer metadata
                    downloadedFile['\xa9lyr'] = downloadConfigData["metaLyricists"] # Set the lyricists metadata
                    downloadedFile['\xa9gen'] = downloadConfigData["metaGenre"] # Set the genre metadata
                    downloadedFile['\xa9day'] = downloadConfigData["metaYear"] # Set the year metadata
                    
                    if downloadConfigData["metaTrackNumber"] == True: # If the track number metadata is enabled
                        downloadedFile['trkn'] = [(int(downloadIndex), 0)] # Set the track number metadata
                    downloadedFile.save() # Save the metadata
                          
        page.update() # Update the page

    page.controls.clear()  # Clear the previous controls  
    
    
    downloadingText = ft.Text((value := "Starting Download..."), size=20) # Create a text widget to display the download status
    loadingBar = ft.ProgressBar(width=1000, height=10) # Create a progress bar widget
    loadingBarContainer = ft.Container(content=loadingBar) # Create a container widget to hold the progress bar
    downloadInfo = ft.Column([downloadingText, loadingBarContainer])
    
    completedText = ft.Text((value2 := ""), size=20) # Create a text widget to display the download status
    
    cancelButton = ft.ElevatedButton("Cancel", on_click=cancelButtonClick, disabled=False) # Create a button widget to cancel the download
    finishedButton = ft.ElevatedButton("Finish", on_click=cancelButtonClick, disabled=True) # Create a button widget to cancel the download
    buttonRow = ft.Row([cancelButton, finishedButton], alignment='center') # Create a Row widget to contain the buttons horizontally
    
    page.add(downloadInfo, completedText, buttonRow) # Add the button to the page
    
    
    if downloadConfigData["format"] == "Audio":
        AorV = "bestaudio[ext=m4a]/bestaudio"
    else:
        resolution = downloadConfigData["resolution"][:-1]
        AorV = f"bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best"

    
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

    
    # Delete playliststart and playlistend from ydl_opts
    # This is used to reset the pointer for the playlist when run multiple times
    if 'playliststart' in ydl_opts:
        del ydl_opts['playliststart']
        del ydl_opts['playlistend']

    altMode = False # Variable to store if the download is in alt mode
    try: # Attempt to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([videoURL])
        finishedDownload()
    
    except yt_dlp.utils.DownloadError as e: # If ffmpeg not installed 
        filesDownloaded = [] # List to store the files downloaded
        altMode = True
        errorBanner("ffmpeg not installed - running in alt mode, speed will be reduced")
        
        ydl_opts['playliststart'] = 1 # Reset pointer 
        ydl_opts['playlistend'] = 1 # Reset pointer
        
        # While true the program will attempt to download the video and audio seperatly at the pointer position
        # After download is complete merge will run and metadata will be added (same function in the hook as normal)
        # After merge iterate both pointers by 1
        while True:
            try:
                for format in AorV: # For each format in the format list
                    ydl_opts['format'] = format # Set download format
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: # Download the video
                        ydl.download([videoURL])
                
                shutil.move(audioFile, os.getcwd() + "/" + pathLists[1]) # Move audio file to temp
                
                if fileName in filesDownloaded: # If the file has already been downloaded
                    break # Exit loop

                filesDownloaded.append(fileName) # Add the video file to the list of files downloaded
                ydl_opts['playliststart'] = ydl_opts['playliststart'] + 1 # Increment the playlist start
                ydl_opts['playlistend'] = ydl_opts['playlistend'] + 1 # Increment the playlist end
                
            except Exception as e: # If playlist is finished
                raise Exception # Exit loop
        
        finishedDownload() # Call the finished download function
        
    except Exception as e:
        downloadingText.value = f"An error occurred: {e}" # Display the error message
        loadingBarContainer.content = loadingBar
        loadingBar.color = ft.Colors.RED
        loadingBar.value = 1
    page.update() 
    
     
ft.app(main) 