from PIL import Image, ImageDraw
import ctypes
import os


def battery_percent() -> float:
    """returns current pattery percentage"""
    if os.name == "nt":
        os.system("powercfg /batteryreport")
        with open("battery-report.html", mode="r", encoding="utf-8") as f:
            close = False
            percentage = 0.0
            for line in f.readlines():
                if "Report generated" in line:
                    close = True
                if close:
                    if "percent" in line:
                        percentage = float(line.split(">")[-1][:-2]) / 100
                        break
        os.system("del *html")

    return percentage


def generate_wallpaper(battery):
    ## https://stackoverflow.com/a/15919897
    with Image.new(
        mode="RGB", size=(1920, 1080), color=(217, 125, 172)
    ) as background, Image.open("fg.png").convert("RGBA") as foreground:

        def draw(canvas_, side_, battery_, fill):
            diagonal = round(((2 * (side_ ** 2)) ** 0.5) * battery_)
            coordinate = round((2 * (diagonal ** 2)) ** 0.5)

            # bottom right, bottom left, top right
            canvas_.polygon(
                [
                    (side_, side_),
                    (side_ - coordinate, side_),
                    (side_, side_ - coordinate),
                ],
                fill=fill,
            )

        side = 365

        with Image.new(mode="RGBA", size=(side, side)) as shades:
            canvas = ImageDraw.Draw(shades)

            alpha = 170
            draw(canvas, side, battery, (213, 97, 158, alpha))
            draw(canvas, side, 0.9 * battery, (190, 51, 196, alpha))
            draw(canvas, side, 0.7 * battery, (98, 34, 180, alpha))
            draw(canvas, side, 0.5 * battery, (61, 16, 158, alpha))

        background.paste(shades, (1267, 358), shades)
        background.paste(foreground, (0, 0), foreground)
        # background.save("wallpaper.png")

    return background


if __name__ == "__main__":
    import time

    while True:
        generate_wallpaper(battery_percent()).save("wallpaper.png")
        ## https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
        ctypes.windll.user32.SystemParametersInfoW(
            0x0014, 0, os.path.abspath("wallpaper.png"), 0
        )
        time.sleep(300)

    # i = a = 0
    # while i <= 1:
    #     # print(i)
    #     generate_wallpaper(i).save(f"{a}.png")
    #     i += 0.001
    #     a += 1
    #     # time.sleep(0.5)
