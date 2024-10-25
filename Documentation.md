# DOCUMENTATION

## Pages
| Page Name| Description | route |
| -------- | ----------- | ---- |
| main | Used to manage the page switching | N/A |
| mainPage | The initial startup page with input for the url | / |
| downloadSettings | Prompts user for settings for the download | /settings |
| download | The page thats shown during the download process | /download |



## Variables
List of all variables sorted by where they're decalred 

### Global
| Variable  | Type | Description | 
| ----------| -----| ----------- | 
| pathLis  | list | Hold the paths which the program uses | 
| videoURL | str | The video url for the download | 
| thumbnailURL | str | The thumbnail url for the video | 
| videoTitle | str | The title of the video | 
| thumbnailPath | str | The path to the saved thumbnail | 
| downloadVariables | dict | Stores settings for the download | 

### mainPage 
Gloal variables refrenced - videoURL, thumbnailURL, videoTitle, thumbnailPath

| Variable  | Type | Description | 
| ----------| -----| ----------- | 
| response | html | Used to check if the entered URL is valid and has a page attached |
| soup | html | Parses the html code to find the video title |
| img | image | The variable which is used to display the thumbnail |
| mainText | flet text | Text field for the page |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |



### downloadSettings
| Variable  | Type | Description | 
| ----------| -----| ----------- | 
|  |  |

### download 
| Variable  | Type | Description | 
| ----------| -----| ----------- | 


