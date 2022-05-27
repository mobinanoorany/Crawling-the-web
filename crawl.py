from tkinter import*
from bs4 import BeautifulSoup  # BeautifulSoup is in bs4 package
import requests
from urllib.parse import urljoin, urlparse
import os
from tqdm import tqdm
import csv


root = Tk()
root.geometry('800x800')
root.title("Crawling images")
#root.config(bg='blue')


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images():
    """
    Returns all image URLs on a single `url`
    """
    url = entry_1.get()
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all('img', {"class": "gallery-thumbs-img"}), "Extracting images"):

        img_url = img.attrs.get("srcset")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue

        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    print(urls)
    return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, str(x)+'.'+url.split(".")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(
        1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main():
    global x
    x = 0
    path = entry_2.get()
    # get all images
    imgs = get_all_images()
    for img in imgs:
        # for each image, download it
        download(img, path)
        x += 1
    Label(root, text=f'Download {x} images!',
          font=("bold", 10)).place(x=445, y=270)


def url_of_image():
    #i = 0
    #j = 0
    image_url = get_all_images()
    count = len(image_url)
    Label(root, text=f'Found {count} images!',
          font=("bold", 10)).place(x=200, y=270)
    #for img in image_url:
    # for each image, download it
    #Label(root, text=f'{img}').place(x=30, y=295+i)
    #i += 20
    #j += 1
    #label_2["text"] = f"{m} "

# Function to take data from GUI
# window and write to an excel file


def download_csv():
    image_url = get_all_images()
    path = entry_2.get()
    if not os.path.isdir(path):
        os.makedirs(path)
    filename = os.path.join(path, path+'.csv')
    for img in image_url:
        with open(filename, "a+", newline='') as my_csv:
            csvfile = csv.writer(my_csv, delimiter=',')
            csvfile.writerow([img])
        my_csv.close()
    Label(root, text=f'Download CSV!',
          font=("bold", 10)).place(x=320, y=270)


label_0 = Label(root, text="Crawling The Web", width=20, font=("bold", 20))
label_0.place(x=90, y=53)


label_1 = Label(root, text="Enter url", width=30, font=("bold", 10))
label_1.place(x=50, y=130)

entry_1 = Entry(root, width=70)
entry_1.place(x=220, y=130)

label_2 = Label(root, text="Path", width=30, font=("bold", 10))
label_2.place(x=50, y=180)

entry_2 = Entry(root, width=70)
entry_2.place(x=220, y=180)

Button(root, text='crawl', width=10, bg='brown',
       fg='white', command=url_of_image).place(x=210, y=230)

Button(root, text='Download csv', width=15, bg='brown',
       fg='white', command=download_csv).place(x=310, y=230)

Button(root, text='Download images', width=15, bg='brown',
       fg='white', command=main).place(x=445, y=230)

Button(root, text='Quit', width=10, bg='brown',
       fg='white', command=root.quit).place(x=580, y=230)


photo = PhotoImage(file='1.gif', format="gif -index 2")
label_3 = Label(root, image=photo, width=300, height=300)
label_3.place(x=250, y=330)


# it is use for display the registration form on the window
root.mainloop()
print("Well Done...")
