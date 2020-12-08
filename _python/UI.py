from tkinter import Frame,Button,Label,Toplevel,Canvas,Tk,Entry
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import cv2
from helper import check_if_face,detect_faces



class VideoFrame:
    
    def closeCamera(self):
        running = False
        if self.vid.isOpened():
            self.vid.release()
            self.root.destroy()
        
    def __init__(self,root,video_source = 0):
        
        global running,frame
        
        self.root = root
        self.root.protocol('WM_DELETE_WINDOW',self.closeCamera)
        self.root.title('Image Capture')
        self.label = Label(self.root)
        self.label.pack()
        
        self.captureImage = Button(self.root,text = 'Capture Image', command = lambda:self.show_frame())
        self.captureImage.pack()
        
        self.vid = cv2.VideoCapture(video_source)
        
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
            
        running= True
        self.show_video()
        self.root.mainloop()       
        
        
    def show_frame(self):
        if running:
            print('inside show_frame')
            _ ,frame = self.vid.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.closeCamera()
            #obj = App()
            #obj.display(frame)
            App.display(frame)
            
        
        
    def show_video(self):
        if running:
            #print('inside show_video')
            _, imgFrame = self.vid.read()
            imgFrame = cv2.flip(imgFrame, 1)
            imgFrame = cv2.cvtColor(imgFrame, cv2.COLOR_BGR2RGB)
            imgFrame = ImageTk.PhotoImage(image = Image.fromarray(imgFrame))
            self.label.imgFrame = imgFrame
            self.label.configure(image = imgFrame)
            self.label.after(10,self.show_video)

class App():
    
    global imageCanvas
    
    def importImageFile():
        print('Import Image')
        imageCanvas.delete('all')
        path = askopenfilename(initialdir = 'D:/Photos',filetypes = [('All Images',['*.jpeg','*.jpg','*.png'])])
        if path:
            img = Image.open(path)
            img = img.resize((600,400),Image.ANTIALIAS) 
            imageCanvas.image = ImageTk.PhotoImage(img)
            imageCanvas.create_image(400,200,anchor = 'center',image=imageCanvas.image)
        
    def video():
        print('in Video()')
        imageCanvas.delete('all')
        vidFrame = Toplevel()
        vid = VideoFrame(vidFrame,0)
        
        
    
    def display(frame):
        global img1
        img1 = frame
        imageCanvas.image = ImageTk.PhotoImage(image = Image.fromarray(frame))
        imageCanvas.create_image(400,200,anchor = 'center',image = imageCanvas.image)
    
    def sendImageServer():
        path = 'D:/AndroidProjects/Attendance/Smart_Attendance_Management_App/_python/image.jpeg'
        Image.fromarray(img1).save(path, 'jpeg')
        print('image written')
        result = check_if_face(path)
        print(result)
        if result:
            detect_faces('CN',path)
        
   
    root = Tk()
    root.title('Attendance Management')
    
    # Canvas Frame
    mainFrame = Frame(root)
    mainFrame.pack()
    imageCanvas = Canvas(mainFrame,width = 800,height = 400,highlightthickness=1,highlightbackground="black")
    imageCanvas.pack(pady = 5)
    
     # Text Frame
    textFrame = Frame(root)
    textFrame.pack(pady = 5)
    
    #Button Frame
    buttonFrame = Frame(root)
    buttonFrame.pack(pady = 10)
    
    
    # Import Button
    importImageButton = Button(mainFrame,text = 'Import Image',command=importImageFile)
    importImageButton.pack(pady = 5)
    
    textLabel = Label(textFrame,text = 'Enter Lecture: ')
    textLabel.grid(row = 0,column = 1,padx = 5)
    
    textField = Entry(textFrame)
    textField.grid(row = 0, column = 2,padx = 5)
    textField.focus_set()
    
    # Start Camera
    startCamera = Button(buttonFrame,text = 'Start Camera',command=video)
    startCamera.grid(row = 0, column = 1, pady = 5)
    
    submit = Button(buttonFrame,text = 'Submit',command = sendImageServer)
    submit.grid(row = 0, column = 2,padx = 5, pady = 5)
    
    
    root.mainloop()
    
        
if __name__=='__main__':
    App()