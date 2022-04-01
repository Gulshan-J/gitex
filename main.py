import tkinter as tk
from tkinter import filedialog as fd
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.signal import find_peaks

class gui:  # creation of class for whole gui
    def __init__(self):
        self.root=tk.Tk()
        #photo = tk.PhotoImage(file="D:\OneDrive - LTTS\Desktop\images.png") # adding images to the gui
        #self.root.iconphoto(False,photo)
        self.root.title('ECG Peak detection')
        self.root.config(bg='burlywood2')
        self.root.geometry("400x400+700+200")
        self.b1=tk.Button(self.root,text='open',command=self.open,width=11,height=2,bg='black',fg='white',font=('Arabic Transparent',11,'bold','italic'))
        self.b1.pack(pady=40,padx=40)
        self.b2=tk.Button(self.root,text='Exit',command=self.exit,width=11,height=2,bg='black',fg='white',font=('Arabic Transparent',11,'bold','italic'))
        self.b2.pack(padx=50,pady=50)
        self.root.mainloop()
    def open(self):     #function to open the csv file
        self.ecg = []
        file = fd.askopenfile(mode='r', filetypes=[('Csv files', '*.csv')])
        myreader = csv.reader(file)
        next(myreader)
        for row in myreader:
            if row[7] != '':
                self.ecg.append(100 * float(row[7]))
        self.root.destroy()
        self.filter_gui()
    def filter_gui(self):   #fuction for filter gui
        self.filter = tk.Tk()
        self.filter.title('Filter')
        #photo = tk.PhotoImage(file="D:\OneDrive - LTTS\Desktop\images.png") # adding images to the gui
        #self.filter.iconphoto(False,photo)
        self.filter.geometry('400x400+700+200')
        self.filter.config(bg='burlywood2')
        self.b3 = tk.Button(self.filter, text='Filter Ecg', command=self.filterecg,width=11,height=2,bg='black',fg='white',font=('Arabic Transparent',10 ,'bold','italic'))
        self.b3.pack(pady=30, padx=30)
        self.b4=tk.Button(self.filter,text='Peak Detection',command=self.peaks,width=12,height=2,bg='black',fg='white',font=('Arabic Transparent',10,'bold','italic'))
        self.b4.pack(padx=40,pady=40)
        self.b5 = tk.Button(self.filter, command=self.back, text='Back', width=12, height=2, bg='black', fg='white',font=('Arabic Transparent', 10, 'bold', 'italic'))
        self.b5.pack(padx=50, pady=50)
        self.filter.mainloop()
    def filterecg(self):    #fuction for filtering the ecg signal using high pass and low pass filter
        f_sample = 400
        f_nyq = f_sample / 2
        Wn = 2 / f_nyq
        self.times = np.arange(len(self.ecg[:500])) / f_sample
        b, a = scipy.signal.butter(4, Wn, 'highpass', analog=False)# filtering through high pass filter
        filtered_ecg = scipy.signal.filtfilt(b, a, self.ecg)
        Wn = 30 / f_nyq
        b, a = scipy.signal.butter(4, Wn, 'low', analog=False)# filtering through low pass filter
        self.filtered_ecg_low = scipy.signal.filtfilt(b, a, filtered_ecg)
        plt.subplot(2,2,1)  #plotting the high and low pass filter
        plt.plot(self.times,self.ecg[:500])
        plt.title('Unfiltered')
        plt.grid()
        plt.subplot(2,2,2)
        plt.plot(self.times,filtered_ecg[:500])
        plt.title('Filtered-high pass')
        plt.grid()
        plt.subplot(2,2,3)
        plt.title('Filtered-Low Pass')
        plt.plot(self.times,self.filtered_ecg_low[:500])
        plt.grid()
        plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
        plt.show()
    def peaks(self):    #peak detection and plotting of peaks
        peaks, _ = find_peaks(self.filtered_ecg_low[:500],height=max(self.filtered_ecg_low) / 2)
        plt.plot(self.filtered_ecg_low[:500])
        plt.title("ECG Peaks")
        plt.plot(peaks,self.filtered_ecg_low[peaks],"+")
        plt.show()
    def exit(self):
        self.root.destroy()
    def back(self):
        self.filter.destroy()
        self.__init__()
if __name__ == "__main__":
    g1=gui()    #creation of object