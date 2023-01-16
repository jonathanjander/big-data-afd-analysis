import pymongo
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    view_db = client["TestView"]
    view_collection = view_db["View"]
    date_x_axis = []
    #["Flüchtling", "Weidel", "Wagenknecht", "Ukraine", "AfD", "Putin"]
    refugee = []
    afd = []
    weidel = []
    wagenknecht = []
    ukraine = []
    putin = []
    count_titles = []
    count_tweets = []
    positiv = []
    negative = []
    neutral = []
    positiv_avg = []
    negative_avg =[]
    neutral_avg = []
    for view in view_collection.find():
        #print(view)
        date_x_axis.append(view["Date"][:2])
        refugee.append(view.get("Flüchtling", 0))
        weidel.append(view.get("Weidel", 0))
        afd.append(view.get("AfD", 0))
        wagenknecht.append(view.get("Wagenknecht", 0))
        ukraine.append(view.get("Ukraine", 0))
        putin.append(view.get("Putin", 0))
        count_titles.append(view.get("Titel", 0))
        count_tweets.append(view.get("Tweet_count", 0))
        positiv.append(view.get("Absolut_positive", 0))
        negative.append(view.get("Absolut_negative", 0))
        neutral.append(view.get("Absolut_neutral", 0))
        positiv_avg.append(view.get("Avg_positive", 0))
        negative_avg.append(view.get("Avg_negative", 0))
        neutral_avg.append(view.get("Avg_neutral", 0))


    # Create a tkinter window
    root = tk.Tk()
    notebook = ttk.Notebook(root)

    #Tab with frame
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text='Schlagzeilen')
    frame1 = tk.Frame(tab1)
    frame1.pack()
    #Plot 1
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.plot(date_x_axis, putin, label="Putin")
    ax1.plot(date_x_axis, ukraine, label="Ukraine")
    ax1.plot(date_x_axis, wagenknecht, label="Wagenknecht")
    ax1.plot(date_x_axis, afd, label="AfD")
    ax1.plot(date_x_axis, weidel, label="Weidel")
    ax1.plot(date_x_axis, refugee, label="Flüchtling")
    fig1.legend(loc="upper left")
    #draw plot
    canvas1 = FigureCanvasTkAgg(fig1, tab1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Plot 2
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.plot(date_x_axis, count_titles, label="Titel")
    ax2.plot(date_x_axis, count_tweets, label="Tweets")
    fig2.legend(loc="upper left")
    # Tab with frame
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text='Tab 2')
    canvas2 = FigureCanvasTkAgg(fig2, tab2)
    canvas2.draw()
    frame2 = tk.Frame(tab2)
    frame2.pack()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(1, 1, 1)
    ax3.plot(date_x_axis, positiv, label="Positiv")
    ax3.plot(date_x_axis, negative, label="Negativ")
    ax3.plot(date_x_axis, neutral, label="Neutral")
    fig3.legend(loc="upper left")
    #Tab with frame 3
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text='Tab 3')
    canvas3 = FigureCanvasTkAgg(fig3, tab3)
    canvas3.draw()
    frame3 = tk.Frame(tab3)
    frame3.pack()
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    fig4 = plt.figure()
    ax4 = fig4.add_subplot(1, 1, 1)
    ax4.plot(date_x_axis, positiv_avg, label="Positiv")
    ax4.plot(date_x_axis, negative_avg, label="Negativ")
    ax4.plot(date_x_axis, neutral_avg, label="Neutral")
    fig4.legend(loc="upper left")
    # Tab with frame 4
    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text='Tab 4')
    canvas4 = FigureCanvasTkAgg(fig4, tab4)
    canvas4.draw()
    frame4 = tk.Frame(tab4)
    frame4.pack()
    canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    # Add the notebook to the window and display it
    notebook.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
