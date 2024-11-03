# DOCUMENTATION - WORK IN PROGRESS

## Pages
| Page Name| Description | route |
| -------- | ----------- | ---- |
| main | Used to manage the page switching | N/A |
| mainPage | The initial startup page with input for the url | / |
| downloadSettings | Prompts user for settings for the download | /settings |
| download | The page thats shown during the download process | /download |


### Global Variables
| Variable  | Type | Description | 
| --------- | ---- | ----------- | 
| pathLis  | list | Hold the paths which the program uses | 
| videoURL | str | The video url for the download | 
| thumbnailURL | str | The thumbnail url for the video | 
| videoTitle | str | The title of the video | 
| thumbnailPath | str | The path to the saved thumbnail | 
| downloadConfigData | dict | Stores settings for the download | 

## Page - Pseudocode




Gloal variables modified - videoURL, thumbnailURL, videoTitle, thumbnailPath

| Variable  | Type | Description | 
| --------- | ---- | ----------- | 
| response | html | Used to check if the entered URL is valid and has a page attached |
| soup | html | Parses the html code to find the video title |
| img | image | The variable which is used to display the thumbnail |
| mainText | flet text | Text field for the page |
| URLInput | flet text field | Input field for the desired URL to download |
| submitButton | flet button | The submit button |


### Page - downloadSettings
Global variables modified - downloadVariables

| Variable  | Type | Description | 
| --------- | ---- | ----------- | 
| isChecked | bool | Used to enable and disable the download button if an option has been picked or not | 
| videoTitleText | flet text | Text field to show the entered videos title and if it is a playlist | 
| videoSelect | flet checkbox | Checkbox to download video (w/audio), will enable resolution select if picked |
| audioSelect | flet checkbox | Checkbox to download only the audio |
| videoAudioRow | flet row | Used to put the video and audio checkboxes in line horizontally |
| resolutions | list | A list of posible resolutons (16:9) to be used for the video download |
| resolutionOptions | flet dropdown options | Adds all resolutions into a format that can be used by a flet dropdown |
| resolutionSelect | flet dropdown | Dropdown menu to select what video resolution to download (will defualt to highest if selected is not available) |
| buttonRow | flet row | Used to put the "main menu" and "download" button on the same row |
| downloadButton | flet Button | Button to confirm setting and begin download |


### Page - download 
Does not mofify any global variables 
| Variable  | Type | Description | 
| ----------| -----| ----------- | 
| cancelDownload | bool | Used by the cancel download button to stop the download |
| fileName | str | Used to store the name of the file being currently downloaded |
| fileExtention | str | Used to store the extention of the file being downloaded |
| totalBytes | int | Total number of bytes of the download, used to calculate download percentage |
| downloadedBytes | int | Total number of byted downloaded, used to calculate download percentage |
| conpletionDecimal | float | Completion percentage in a decimal format |
| altMode| bool | Used to switch to an alternative download method when ffmpeg is not installed |
| audio | audio file | Inputs the downloaded audio file into the program |
| video | video file | Inputs the downloaded video file into the program | 
| videoWithAudio | video file | Variable to store the merged audio and video file |
| filesDownloaded | list | Used to keep track of what files have been downlaoded when running altMode |
| downloadingText | flet text | General downloading information text |
| loadingBar | flet progress bar | Visual representation to show the download progress |
| loadingBarContainer | flet container | Holds the "loadingBar" so that its value can be modified |
| downloadInfo | flet column | Alligns the "downloadingText" and "loadingBarContainer" so that they are vertically in line with each other |
| completedText | flet text | Slightly larger text to show the downloaded file and the finished download text |
| cancelButton | flet button | Button to cancel the download and return to the main menu |
| finishedButton | flet button | Button that "unlocks" when the download is finished that returns to the main menu |
| buttonRow | flet row | Holds the cancel button and finished button so they are horizontally aligned |
| AorV | str | Stores the download configuration string for the download (yt_dlp) |
| resoluton | str | Temporaraly holds the resolution if downloading a video |
| ydl_opts | dict | Holds the download configuration settings for yt_dlp |
