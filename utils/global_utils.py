import pathlib
import shutil

crimson = 0xDC143C


def flatten(d, inval, outval):
    for k, v in d.items():
        if isinstance(v, dict):
            flatten(d[k], inval, outval)
        else:
            if v == "":
                d[k] = None
    return d


def news_exists(s):
    path = pathlib.Path(s)
    if path.exists():
        return
        # print("File exist")
    else:
        source = "./assets/empty.json"
        try:
            shutil.copy(source, s)
            print("File copied successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")


def minutes(s):
    s = s * 60
    return s
