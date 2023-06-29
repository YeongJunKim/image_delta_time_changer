"""Image Delta Time Changer"
"""

from datetime import datetime, timedelta
import argparse
import glob
import sys
import piexif

def delta_changer(target_file: str, d_h: int, d_m: int, d_s: int):
    """Delta time changer

    Args:
        f (str): File name
        h (int): Delta hour
        m (int): Delta minute
        s (int): Delta second
    """
    exif_dict = piexif.load(target_file)
    current_time_b = exif_dict['0th'][piexif.ImageIFD.DateTime]
    current_time_str = current_time_b.decode('utf-8')

    new_time = datetime.strptime(current_time_str, "%Y:%m:%d %H:%M:%S")
    new_time = new_time + timedelta(hours=d_h,minutes=d_m,seconds=d_s)
    new_time_str = new_time.strftime("%Y:%m:%d %H:%M:%S")

    print(f"file: {target_file},\ncurrent: {current_time_str},\nnew: {new_time_str}")

    exif_dict['0th'][piexif.ImageIFD.DateTime] = new_time_str
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_time_str
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_time_str

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, target_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate delta time and set; JPG image format")

    parser.add_argument("-H", "--hour", help="Delta time of hour", default=0)
    parser.add_argument("-M", "--minute", help="Delta time of minute", default=0)
    parser.add_argument("-S", "--second", help="Delta time of second", default=0)
    parser.add_argument("-f", "--file", help="File to chage time")
    parser.add_argument("-d", "--dir", help="Directory to chage time")

    args = parser.parse_args()

    if args.file is None:
        if args.dir is None:
            print("File or Dir is not imported")
            sys.exit()

    d_hour = int(args.hour)
    d_minute = int(args.minute)
    d_second = int(args.second)


    if args.file is not None:
        file = args.file
        delta_changer(file, d_hour, d_minute, d_second)
        sys.exit()

    if args.dir is not None:
        extensions = [".JPG", ".jpg", ".jpeg", ".JPEG"]
        files = []
        for extension in extensions:
            rule = args.dir+"/*"+extension
            g = glob.glob(rule)
            files = files + g

        files.sort(reverse=False)
        for file in files:
            delta_changer(file, d_hour, d_minute, d_second)
        sys.exit()
