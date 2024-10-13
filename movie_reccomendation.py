import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk 
from tkinter import messagebox
import webbrowser
import mysql.connector
db = mysql.connector.connect(host="localhost",user="root",password="Navee@03",db="projects")
cursor = db.cursor()
root=tk.Tk()
root.title("movie search")
root.geometry("1920x1080")
# Load an image using PIL and convert it to a PhotoImage object
image_path = r"C:\Users\dell\Downloads\3.jpg"
pil_image = Image.open(image_path)
photo = ImageTk.PhotoImage( pil_image)

# Create a Label widget and set its image option
label = tk.Label(root, image=photo)
# Keep a reference to the image object to prevent it from being garbage collected
label.image = photo
# Pack the Label widget into the window
label.place(relheight=1,relwidth=1)
txt=tk.Label(root,text="Movie Recommendation System ",font=('georgia',80),bg="#CC313D",fg="#F7C5CC")
txt.pack()
l1 = tk.Label(root, text="Enter a Movie Please : ", width=25,height=2, font=('arial' ,30,'bold'),bg='#F98866',fg='#FFF2D7')
l1.place(x=600, y=130)

t1 = tk.Text(root, height=2, width=27, bg='light blue')
t1.place(x=600, y=230)
t1.get('1.0',tk.END)
movie_title=tk.StringVar()
movie_title_entry = tk.Entry(root, width=27, textvariable=movie_title,font=('arial', 30,'bold'))
movie_title_entry.place(x=600, y=230)

# Create a listbox to display search suggestions
search_listbox = tk.Listbox(root, width=27, height=5, font=('arial', 20, 'bold'))
search_listbox.place(x=600, y=280)
search_listbox.delete(0, tk.END)

# Create a scrollbar for the listbox
#scrollbar = tk.Scrollbar(root, orient="vertical", command=search_listbox.yview)
#scrollbar.place(x=930, y=280, height=120)
#search_listbox.config(yscrollcommand=scrollbar.set)

movie_title_entry.focus()
root.bind("<Return>", lambda event: details(movie_title.get()))
root.bind("<Delete>" ,lambda event:(clear_input(),close_treeview()) )

b1 = tk.Button(root, text='showdetails', width=18,height=2, bg='#EB5B00', command=lambda: details(movie_title.get()),font=("arial", 12, "bold"))
b1.place(x=600, y=680)
b2 = tk.Button(root, text='Clear', width=18,height=2, bg='red', command=lambda: [clear_input(),close_treeview()],font=("arial", 12, "bold"))
b2.place(x=800, y=680)
# mystr=tk.StringVar()
# mystr.set('output here')

def clear_input():
    movie_title_entry.delete(0, 'end')  # clear the text box
    movie_title_entry.focus_set()  # set the focus back to the entry widget
    movie_title.set('')
    mystr.set('output here ')
    if tree:
        tree.destroy()
    if main_frame:
        main_frame.destroy()
    if close_button:
        close_button.destroy()

    if close_button:
        close_button.destroy()
    search_listbox.place_forget()
    search_listbox.delete(0, tk.END)
    movie_title.delete(0, tk.END)
    



tree = None
main_frame = None
close_button = None

def search_suggestions(event):
    search_query = movie_title.get()
    if search_query:  # If the entry field is not empty
        cursor.execute("SELECT movie_title FROM kushalmovies WHERE movie_title LIKE %s", (f"%{search_query}%",))
        search_results = [row[0] for row in cursor.fetchall()]
        search_listbox.delete(0, tk.END)
        for result in search_results:
            search_listbox.insert(tk.END, result)
        search_listbox.place(x=600, y=280)  # Show the listbox
    else:
        search_listbox.place_forget()  # Hide the listbox

root.bind("<KeyRelease>", search_suggestions)

def select_movie(event):
    selected_movie = search_listbox.get(search_listbox.curselection())
    details(selected_movie)

root.bind("<<ListboxSelect>>", select_movie)


def details(movie_title):
    global tree, main_frame, close_button
    try:
        print(f"Query: select movie_title, movie_imdb_link, title_year,language,genres,duration,imdb_score from kushalmovies where movie_title={movie_title}")
        cursor.execute('select  movie_title, movie_imdb_link, title_year,language,genres,duration,imdb_score from kushalmovies where movie_title=%s',(movie_title,))
        kushalmovies = cursor.fetchall()

        if not kushalmovies:
            raise Exception(f"No records found for movie title '{movie_title}'")

        # Create a main frame to hold the Treeview widget
        if main_frame:
            main_frame.destroy()
        main_frame = Frame(root, bg="light grey")
        main_frame.pack(fill="both", expand=True, pady=200)  # Add some padding to the top and bottom

        # Clear the previous Treeview widget
        if tree:
            tree.destroy()

        # Create a new Treeview widget
        
        
        tree = ttk.Treeview(main_frame, columns=('Movie Title', 'IMDB Link', 'Year','language','genres','duration','imdb_score'), show='headings')
        tree.pack(fill="both", expand=True)

        tree.heading('Movie Title', text='Movie Title')
        tree.column('Movie Title', width=200)
        tree.heading('IMDB Link', text='IMDB Link')
        tree.column('IMDB Link', width=200)
        tree.heading('Year', text='Year')
        tree.column('Year', width=200)
        tree.heading('language', text='language')
        tree.column('language', width= 200)
        tree.heading('genres', text='genres')
        tree.column('genres', width=200)
        tree.heading('duration', text='duration')
        tree.column('duration', width=200)
        tree.heading('imdb_score', text='imdb_score')
        tree.column('imdb_score', width=200)

        #row height
       
        

        # Populate the Treeview with data
        for index, movie in enumerate(kushalmovies):
            tree.insert('', 'end', values=(movie[0], movie[1], movie[2],movie[3],movie[4],movie[5],movie[6]))

        # Select the first item in the Treeview
        tree.focus_set()
        tree.selection_set(tree.get_children()[0])

        # Destroy the Treeview widget and its parent frame
        def close_treeview():
            if tree:
                tree.destroy()
            if main_frame:
                main_frame.destroy()
            if close_button:
                close_button.destroy()

        if close_button:
            close_button.destroy()
        close_button = Button(root,width=20 , height = 2, text="Close Treeview",bg="blue" ,fg="pink",  command=close_treeview,font=("arial", 10, "bold"))
        close_button.pack(pady=20)

        # Define a function to open the URL link
        def open_url(event):
            item = tree.item(tree.focus())
            url = item['values'][1]  # Assuming the URL is in the second column
            webbrowser.open(url)

        # Bind the double-click event to the open_url function
        tree.bind("<Double-Button-1>", open_url)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mystr.set('Database Error')
    except Exception as e:
        print(f"Error: {e}")
        mystr.set(f"No records found for movie title '{movie_title}'")
        # Display an error message in the Treeview
        if main_frame:
            main_frame.destroy()
        main_frame = Frame(root, bg="light grey")
        main_frame.pack(fill="both", expand=True, pady=180)
        tree = ttk.Treeview(main_frame, columns=('Error'), show='headings')
        tree.pack(fill="both", expand=True)
        tree.heading('Error', text='Error')
        tree.column('Error', width=500)
        tree.insert('', 'end', values=(str(e),))
    else:
        print(f"Result: {kushalmovies}")


mystr = tk.StringVar()
mystr.set('outputhere ')
 

def display_message():
    messagebox.showinfo("About", """Welcome to our project dedicated to enhancing your movie-watching"
    experience through intelligent recommendations. Our team has developed
    "a robust movie recommendation system using advanced Python programming techniques
    and this project is done by the team of Mr Kushal, Mr Deelip ,Mr kishor and This structure effectively communicates the purpose, 
                     benefits, and goals of your movie recommendation system project in an engaging and informative manner, suitable for 
                     an "About Us" section. Adjust the details to fit your specific project and audience preferences for clarity and impact
                     n today's digital age, where streaming platforms offer a vast array of movies, a recommendation system becomes invaluable. A movie recommendation system suggests movies to users based on their preferences and behavior, enhancing user experience and engagement.
                      This project aims to develop a movie recommendation system using Python.""")

button = tk.Button(root, text="AboutUs",width=10 , height = 2, bg="#219C90", command=display_message,font=("arial", 10, "bold"))
button.place(x=500,y=680)

def help():
    messagebox.showinfo("How to run the project ","""step1:open terminal
                        step2:type file name with extension like datavisualization.py
                        step3:later the window visible and 
                        step4: start searcing the movie  name 
                        and enjoy itttt """)
button1 = tk.Button(root, text="Help..?",width=10 ,height = 2, bg="#219C90", command=help,font=("arial", 10, "bold"))
button1.place(x=345,y=680)

# def create_new_window():
#     root.title("Feedback System")
#     root.geometry('200x300')
#     feedback_label = tk.Label(root, text="Enter your feedback:")
#     feedback_label.pack()
#     feedback_entry = tk.Text(root, width=40, height=10)
#     feedback_entry.pack()
#     submit_button = tk.Button(root, text="Submit", command=lambda:store(feedback_entry))
#     submit_button.pack()

# def store(feedback_entry):
#     feedback = feedback_entry.get("1.0", "end-1c")
#     if feedback:
#         cursor.execute("INSERT INTO feedback (feedback) VALUES (%s)", (feedback,))
#         db.commit()
#         messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
#     else:
#         messagebox.showerror("Error", "Please enter your feedback")
def create_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Feedback System")
    new_window.geometry('300x300')
    feedback_label = tk.Label(new_window, text="Enter your feedback:")
    feedback_label.pack()
    feedback_entry = tk.Text(new_window, width=40, height=10)
    feedback_entry.pack()
    submit_button = tk.Button(new_window, text="Submit",bg='red',command=lambda:store(feedback_entry),font=('arial' ,10 ))
    submit_button.pack()
button3=tk.Button(root,text="feedback",width=10, height = 2, bg='#219C90',command=create_new_window,font=("arial", 10, "bold"))
button3.place(x=420,y=680) 
def store(feedback_entry):
    feedback = feedback_entry.get("1.0", "end-1c")
    if feedback:
        cursor.execute("INSERT INTO feedback (feedback) VALUES (%s)", (feedback,))
        db.commit()
        messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
        feedback_entry.master.destroy()  # Close the new window
    else:

        
        messagebox.showinfo("Error", "Please enter your feedback")

def display_items():
    window=tk.Toplevel(root)
    window.title("MySQL Database Viewer")
    window.geometry('500x600')
    # Create a label and text box to display the list of items
    labe5= tk.Label(window, text="Movies:")
    labe5.pack()
    text_box = tk.Text(window, width=120, height=20, font=("Helvetica", 12, "bold"))
    text_box.pack()
    # Retrieve the list of items from the database
    cursor.execute("SELECT movie_title FROM kushalmovies")
    items = cursor.fetchall()

    # Display the list of items in the text box
    text_box.delete(1.0, tk.END)
    for item in items:
        text_box.insert(tk.END, str(item[0]) + "\n", "movie_title")

    # Configure the font style for the text box
    text_box.tag_config("movie_title", font=("Helvetica", 12, "bold"))
button5 = tk.Button(root, text="Sugesstion Movies",bg='pink',height=2,width=18,command=display_items,font=("arial", 12, "bold"))
button5.place(x=1000,y=680)
   
root.mainloop()


