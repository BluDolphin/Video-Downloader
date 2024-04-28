import yt_dlp
import ffmpeg
import os 

def checkExtention(filename, intendedFormat): #Function for checking file extention and converting if needed
    _, extension = os.path.splitext(filename) #Get the file extension from the downloaded file
    
    if extension == ".mp4": #if the file is mp4 (no need to convert)
        #Because yt_dlp downlaods video then audio files separatlly
        #The file extention is flagged as m4a (audio) since its always downloaded last
        #this cuases a bug as after the hook is run its then combined 
        return
    
    if extension != intendedFormat: #If the file is not in the intended format
        print("Converting file to intended format...\n") 
        output_file = f"{os.path.splitext(filename)[0]}{intendedFormat}" #Set the output file to the intended format
        ffmpeg.input(filename).output(output_file).run(capture_stderr=True) #Convert the file to the intended format
        
        try:
            os.remove(filename) #Deleting the file with the wrong extention
        except OSError as e:
            print(f"Error: {filename} : {e.strerror}") #Print error message if file cannot be deleted
        
            
def Download():
    print("\n========= Youtube Downloader ========="
          "\nPlaylists need to be set to public or unlisted to be downloaded."
          "\nInput the URL of the playlist or single to download:")
    usrInput = input("\nURL: ").strip()
    
    AorV, intendedFormat = audioOrVideo()
    print("\nStarting download...")
    
    ydl_opts = {
    'noplaylist': False,  # Download just the video, if the URL refers to a video and a playlist.
    'quiet': True,  # Do not print messages to stdout.
    'format': AorV,  # Choice of quality.
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Name the file the ID of the video
    'restrictfilenames': True,  # Restrict filenames to only ASCII characters, and avoid "&" and spaces in filenames
    'no_warnings': True,  # Suppress all warning messages
    'nooverwrites': True,  # Prevent overwriting files.
    'continuedl': True,  # Force resume of partially downloaded files.
    'progress_hooks': [lambda d: my_hook(d, intendedFormat)],  # Hook function that gets called before the download starts
    }
                
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: 
            ydl.download([usrInput])
    except:
        print("\nError: Invalid URL")
        Download()
    
    print("\nDownload Complete")
    input("Press Enter to Exit...")

def audioOrVideo(): #Function for specifying audio or video download
    print("\nWhich do you want to download:"
          "\n1) Audio (m4a)"
          "\n2) Video (mp4)"
          "\n3) Custom (Format and quality, needs ffmpeg installed)")
    
    if (temp:=input("Input: ")) == "1": #If audio
        return "bestaudio[ext=m4a]/bestaudio", ".m4a" #Return parameters for audio - mp3 and best quality
    elif temp == "2": #If video
        return "bestvideo[ext=mp4]+bestaudio[ext=mp4]/best", ".mp4" #Return parameters for video - mp4 and best quality
    elif temp == "3": #If custom format
        return customFormat() #Return custom format
    else:
        print("Invalid Input")
        audioOrVideo()
    
        
def customFormat(): #Function for setting custom format
    print("\nDo you want to download"
          "\n1) Audio"
          "\n2) Video")
    
    #Player picks audio or video
    if (usrInput:=input("Input: ").strip()) == "1": #If audio
        while True: 
            audioFormats = ["mp3", "m4a", "mp4", "wav", "aac", "flac", "ogg", "wma", "webm", "mkv", "mka"] #List of supported audio formats
            print("\nWhich format do you want to download:" 
                "\nSupported Formats are: ", audioFormats,
                "\nLeave Blank for defualt(m4a)"
                "\nNote: formats other thatn m4a and webm will take extra time and require ffmpeg to be installed.")
            
            if (temp:=input("Input: ").strip()) == "": #If blank
                fileFormat = "m4a"
                break
            elif temp in audioFormats: #If format is supported
                fileFormat = temp #Set format
                break
            else:
                print("Invalid Input")
                
        custQuality = customQuality(usrInput) #Return custom quality
        return f"{custQuality}audio[ext={fileFormat}]/bestaudio", f".{fileFormat}" #Return custom quality and format parameter
    
    elif usrInput == "2": #If video
        while True: 
            videoFormats = ["mp4", "mkv", "avi", "mov"] #List of supported video formats
            print("\nWhich format do you want to download:"
                  "\nSupported Formats are: ", videoFormats,
                  "\nLeave Blank for defualt(mp4)"
                  "\nNote: formats other thatn mp4 and webm will take extra time to convert and require ffmpeg to be installed.")
            
            temp=input("Input: ").strip() #Player picks format
            if temp == "": #If blank
                fileFormat = "mp4" #Set format
                break
            elif temp in videoFormats: #If format is supported
                fileFormat = temp #Set format
                break
            else:
                print("Invalid Input")
        
        custQuality, custResolution = customQuality(usrInput) #Return custom quality
        return f"{custQuality}video{custResolution}[ext={fileFormat}]+bestaudio[ext=m4a]/best", f".{fileFormat}"#Return custom quality and format parameter
    
    else:
        print("Invalid Input")
        customFormat()


def customQuality(type): #Function for setting custom quality - Passed type of download (audio or video)
    while True: 
            print("\nWhich quality do you want to download:"
                "\n1) Best"
                "\n2) Worst")
            if (temp:=input("Input: ")) == "1": #If best quality
                quality = "best" #Set quality
                break
            elif temp == "2": #If worst quality
                quality = "worst" #Set quality
                break
            else:
                print("Invalid Input")
                   
    if type == "1": #If audio
        return quality #Return quality (resolution isnt needed for audio)
     
                    
    validResolutions = ["144", "240", "360", "480", "720", "1080", "1440", "2160", "4320"] #List of valid resolutions
    while True:
        temp = input("\nInput Resolution (e.g. 720, 1080)"
                     "\nInput Blank for Best: ")
        
        if temp in validResolutions: #If resolution is valid
            resolution = f"[height<={temp}]" #Set resolution
            break
        elif temp == "": #If blank
            resolution = "" #Set resolution to blank (defualt - best)
            break
        else:
            print("Invalid Input")
                   
    return quality, resolution #Return quality and resolution


def my_hook(d, intendedFormat):
    if d['status'] == 'finished':
        print("\nFinished downloading: ", d['filename'])
        filename = d['filename']
        checkExtention(filename, intendedFormat)


Download()