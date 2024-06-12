from time import sleep
import flet as ft

def main(page: ft.Page):
    pb = ft.ProgressBar(width=400)

    # Define a placeholder to replace the progress bar later
    pb_placeholder = ft.Container(content=pb)

    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ft.Text("Doing something..."), pb_placeholder]),
    )
    
    for i in range(2):
        for i in range(0, 101):
            pb.value = i * 0.01
            sleep(0.1)
            page.update()

        # Replace the original progress bar with an indeterminate progress indicator
        pb_placeholder.content = ft.ProgressBar(width=400, color="blue")  # Using ProgressRing as an indeterminate indicator
        page.update()
        
        sleep(2)
        pb_placeholder.content = pb

ft.app(target=main)
