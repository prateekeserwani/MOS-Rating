import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk 
import glob 
import os
from tkinter import messagebox
import csv
import pandas as pd 
import random 
import numpy as np

all_labels = []
all_combo = []
path='./images/method1/'
counter=1
current=0

def read_filelist(path):
    # crawl file list 
    filelist = glob.glob(path+'*.png')
    return filelist

def initialize_dataframe(files):
    file_list=[]
    for file in files:
        file_list.append(file.split(os.sep)[-1])

    df = pd.DataFrame(columns = [ 'Method1', 'Method2','Method3','Method4','Method5'],
                      index = file_list) 

    return df 

def write_df(df, image_name, rating):
    global current 
    print(image_name)
    df.loc[image_name] = [rating[0], rating[1],rating[2],rating[3],rating[4]] 
    print(df)
    df.to_csv('rating.csv') 

def check_restart():
    global current 
    if os.path.exists('rating.csv'):
        current = np.load('counter.npy')
        current = current-1
        print('current', current)
        return True
    return False
    
def nextbuttonClick():
    global current
    global files 
    global df 
    # record the score 
    image_name = files[current-1].split(os.sep)[-1]
    response=[]
    flag=True
    for i in range(5):
        combo_value=all_combo[i].get()
        if combo_value=='' or combo_value=='0':
            flag=False
        response.append(combo_value)
    print('collected response', response)
    if flag:
        #write_csv(image_name,response)
        write_df(df, image_name, response)
        if current > len(files)-1: 
            messagebox.showerror("Forward move error", "No more images")
        else:
            for i in range(5):
                pilimage = Image.open(os.path.join('./images/method'+str(i+1),files[current].split(os.sep)[-1])).convert('RGB')
                #pilimage = pilimage.resize((256,256), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(pilimage)
                print(os.path.join('./images/method'+str(i+1),files[current].split(os.sep)[-1]))
                all_labels[i].configure(image=image)
                all_labels[i].photo = image
                all_combo[i].current(0)
            current = current +1
    else:
        messagebox.showerror("Error", "Please select all response") 
    np.save('counter.npy',current)
    

def previousbuttonClick():
    global current
    # show an "Open" dialog box.
    if current-2<0:
        messagebox.showerror("Backward move error", "No backward seek is possible. ")
    else:
        current = current-2
        for i in range(5):
            pilimage = Image.open(os.path.join('./images/method'+str(i+1),files[current].split(os.sep)[-1])).convert('RGB')
            pilimage = pilimage.resize((256,256), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(pilimage)
            print(os.path.join('./images/method'+str(i+1),files[current].split(os.sep)[-1]))
            all_labels[i].configure(image=image)
            all_labels[i].photo = image
        current = current +1



if check_restart():
    df = pd.read_csv('rating.csv', index_col=0)
    print(df.index.values)
    files=df.index.values#df['Unnamed: 0'].tolist()
    print(files)
else:
    files = read_filelist(path)
    df = initialize_dataframe(files)



root = tk.Tk()
container = ttk.Frame(root)

canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar_2 = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)


scrollable_frame = ttk.Frame(canvas)

main_frame = tk.Frame(scrollable_frame)
main_frame.pack(fill="both", expand=True)

for i in range(2):
    for j in range(3):
        if i==1 and j>=2:
           break	
        
        frame = tk.Frame(
            master=main_frame,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j)
        image = ImageTk.PhotoImage(Image.open(os.path.join('./images/method'+str(counter),files[current].split(os.sep)[-1])))

        label = tk.Label(master=main_frame,image=image)
        label.photo = image 
        label.grid(row=2*i, column=j)
        
        all_labels.append(label)  
        # Combobox creation 
        n = tk.StringVar() 
        monthchoosen = ttk.Combobox(main_frame, width = 5, textvariable = n) 
  
        # Adding combobox drop down list 
        monthchoosen['values'] = ('0',' 1', ' 2', '3', ' 4', ' 5') 
        monthchoosen.grid(row = 2*i+1, column = j) 
        monthchoosen.current(0)
        all_combo.append(monthchoosen)
        counter=counter+1

f1 = tk.Frame(main_frame)
current=current+1
btn2 = ttk.Button(f1, text = '< Previous', command=previousbuttonClick) 
btn1 = ttk.Button(f1, text = 'Next >',  command=nextbuttonClick) 

f1.grid(row=3, column=2)
btn2.pack(side="left")
btn1.pack(side="right")




scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.configure(xscrollcommand=scrollbar_2.set)


container.pack(fill="both", expand=True)#grid(row=0,column=0)
canvas.pack(side="top", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
scrollbar_2.pack(side="bottom", fill="x")

root.mainloop()

