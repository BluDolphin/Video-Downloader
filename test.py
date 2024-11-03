from mutagen.mp4 import MP4

def customize_metadata(file_path, title=None, artist=None, album=None, genre=None):
    audio = MP4(file_path)
    
    if title:
        audio['\xa9nam'] = title
    if artist:
        audio['\xa9ART'] = artist
    if album:
        audio['\xa9alb'] = album
    if genre:
        audio['\xa9gen'] = genre
    
    audio.save()

# Example usage
file_path = '/home/bludolphin/Documents/GitHub/Video-Downloader/downloads/Let_s_cook_butter_chicken_together.m4a'
customize_metadata(file_path, title='New Title', artist='New Artist', album='my Album', genre='New Genre')