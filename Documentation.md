# DOCUMENTATION

## Notes

When creating the download and temp folders, the program will auto purge temp if it already exists.

The thumbnail uses the hashed video title prevent duplicate file names.

The download settings nested within their columns inside a row to achieve the layout.
The metadata can be easily expanded just by adding a new input box and appropriate key to the downloadConfigData dictionary.

The download hook continuously checkes to see if the cancelDownload is true to terminate the download.
Download percentage is calculated with the 'total_bytes_estimate' and 'downloadedBytes' from the hook. Completion percentage is then calculated with downloadedBytes/totalBytes, and passed to the loading bar to be displayed

When attempting to download videos yt_dlp will attempt to use ffmpeg. If it is not installed, instead of crashing, the program will fall back to using moviepy at the cost of speed. Following the merge the video file with be overwritten and the audio file will be moved to the temp folder.

## Pages

| Page Name| Description | route |
| -------- | ----------- | ---- |
| main | Used to manage the page switching | N/A |
| mainPage | The initial startup page with input for the url | / |
| downloadSettings | Prompts user for settings for the download | /settings |
| download | The page thats shown during the download process | /download |

## Pseudocode

1. Import required packages
2. Create downloads and temp folders
3. Initialise global variables
4. Define main(page) for page routing
5. Define mainPage
    - Clear the page
    - Display URL input box
    - Display submit button
    - On submit button press
        - Download video thumbnail
        - Store video title
6. Define downloadSettings
    - Clear the page
    - Display video thumbnail
    - Display video/Playlist name
    - Display format dropdown (Audio, Video)
    - Display resolution dropdown
    - Display metadata checkbox
    - Display album name input
    - Display back and submit button
7. Define download page
    - Clear the page
    - Display download progress bar
    - Display download status text
    - Display cancel button
    - On download start
        - Update progress bar
        - Update status text
    - On download finish
        - Display completion text
        - Enable finish button
    - On cancel button press
        - Stop download
        - Return to main page

### Global Variables

| Variable  | Type | Description |
| --------- | ---- | ----------- |
| pathLists | list | Hold the paths which the program uses |
| videoURL | str | The video url for the download |
| thumbnailURL | str | The thumbnail url for the video |
| videoTitle | str | The title of the video |
| thumbnailPath | str | The path to the saved thumbnail |
| downloadConfigData | dict | Stores settings for the download (format, resolution, metadata, metaAlbum) |

### Page - mainPage

Global variables modified - videoURL, thumbnailURL, videoTitle, thumbnailPath

| Variable  | Type | Description |
| --------- | ---- | ----------- |
| response | html | Used to check if the entered URL is valid |
| soup | html | Parses the html code to find video metadata |
| img | image | Used to resize the thumbnail |
| mainText | flet text | Title text for the page |
| URLInput | flet text field | Input field for the URL |
| submitButton | flet button | Button to submit the URL |

### Page - downloadSettings

Global variables modified - downloadConfigData

| Variable  | Type | Description |
| --------- | ---- | ----------- |
| thumbnailImage | flet image | Displays the video thumbnail |
| videoTitleText | flet text | Shows video title and if it's a playlist |
| videoAudioOptions | list | List of format options (Audio/Video) |
| videoAudioSelect | flet dropdown | Dropdown for selecting format |
| resolutions | list | List of available video resolutions |
| resolutionOptions | flet dropdown options | Resolution options for dropdown |
| resolutionSelect | flet dropdown | Dropdown for selecting resolution |
| customMetadata | flet checkbox | Checkbox to enable custom metadata |
| metaAlbumInput | flet textfield | Input for album name metadata |
| formatResolutionRow | flet row | Contains format and resolution settings |
| buttonRow | flet row | Contains navigation buttons |
| downloadButton | flet button | Button to start download |

### Page - download

Does not modify global variables

| Variable  | Type | Description |
| ----------| -----| ----------- |
| cancelDownload | bool | Flag to stop the download |
| fileName | str | Name of file being downloaded |
| audioFile | str | Path to downloaded audio file |
| totalBytes | int | Total size of download |
| downloadedBytes | int | Current downloaded bytes |
| completionDecimal | float | Download progress as decimal |
| altMode | bool | Flag for alternative download mode (no ffmpeg) |
| filesDownloaded | list | Tracks downloaded files in altMode |
| downloadingText | flet text | Shows download status |
| loadingBar | flet progress bar | Visual download progress |
| loadingBarContainer | flet container | Contains progress bar |
| downloadInfo | flet column | Groups download status elements |
| completedText | flet text | Shows completion status |
| buttonRow | flet row | Contains control buttons |
| AorV | str/list | Download format configuration |
| ydl_opts | dict | Options for yt-dlp downloader |
