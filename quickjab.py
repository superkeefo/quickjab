import customtkinter as ctk
import os
import datetime
import glob
from PIL import Image


JOBLIST = os.path.join('joblist','joblist.txt')

class Jobtimer:
    def __init__(self):
        self.counting = False
        self.count_mode = "up" # default count mode
        
    def switchcount(self):
        if self.count_mode == "up":
            self.count_mode = "down"
            self.setcountbtns()
            countup_btn.configure(state="normal")
            countdown_btn.configure(state="disabled")
            print(f'now counting down')

        else:
            self.count_mode = "up"
            self.setcountbtns()
            countup_btn.configure(state="disabled")
            countdown_btn.configure(state="normal")
            print(f'now counting up')



    def setcountbtns(self):
        if self.count_mode == "up":
            countup_btn.configure(fg_color='#444444')
            countdown_btn.configure(fg_color='#333333')
        else:
            countdown_btn.configure(fg_color='#444444')
            countup_btn.configure(fg_color='#333333')


    def startcount(self):
        self.counting = True   
        if self.count_mode == "up":
            self.countup()
        else:
            self.countdown()   

    def stopcount(self):
        self.counting = False

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.timesup()
        else:
            hours = int(self.remaining / 3600)
            minutes = int(self.remaining / 60 ) % 60
            print(f"{hours:02}:{minutes:02}")
            self.remaining -= 1
            if self.counting:
                root.after(1000, self.countdown)

    def countup(self, startingat=None):
        if startingat is not None:
            self.starttime = startingat
        self.counting = True
      
        hours = int(self.starttime / 3600)
        minutes = int(self.starttime / 60 ) % 60
        print(f"{hours:02}:{minutes:02}")
        self.starttime += 1
        if self.counting:
            root.after(1000, self.countup)

    def timesup(self):
        print("Time's up!")

    def convertinput(self, hours, minutes):
        self.inputhours = hours*3600
        self.inputminutes = minutes*60
        self.inputtime = self.inputhours + self.inputminutes
        return self.inputtime

class Joblist:
    def __init__(self):
        self.jobs = []

    def listjobs(self):
        if not os.path.exists(JOBLIST):
            self.jobs = []
            return self.jobs
        with open(JOBLIST, "r") as file:
            self.jobs = [line.strip() for line in file if line.strip() != "Select job"]
        return self.jobs
        
    def addjob(self, jobname):
        if jobname == "Select job" or not jobname.strip():
            return  # Do nothing
        if jobname not in self.jobs:
            self.jobs.append(jobname)
            with open(JOBLIST, "w") as file:
                for item in self.jobs:
                    file.write(item + '\n')
        refresh_job_dropdown()

    def deletejob(self, jobtodelete):
        if jobtodelete == "Select job" or not jobtodelete.strip():
            return  # Do nothing
        if jobtodelete in self.jobs:
            self.jobs.remove(jobtodelete)
            with open(JOBLIST, "w") as file:
                for item in self.jobs:
                    file.write(item + '\n')
        refresh_job_dropdown()

class Timelog:
    def __init__(self):
        self.fulldate = datetime.date.today()
        self.cur_weeknum = self.fulldate.strftime("%V")
        self.cur_date = self.fulldate.strftime("%d-%m-%Y")
        self.log_dir = "logs"
        self.cur_log = self.find_latest_log()

    def find_latest_log(self):
        pattern = os.path.join(self.log_dir, f"WEEK{self.cur_weeknum}*")
        logs = glob.glob(pattern)
        if logs:
            return logs[0]
        else:
            new_log = os.path.join(self.log_dir, f"WEEK{self.cur_weeknum}_{self.cur_date}.txt")
            with open(new_log, "w") as file:
                pass
            return new_log
    
    def log_time(self, jobname, input):
        if jobname != "Select job" and input.strip():
            output = (f'{self.cur_date}   {jobname}   {input}')
            with open(self.cur_log, "a") as file:
                file.write(output + "\n")
            

root = ctk.CTk()
jobtimer = Jobtimer()
joblist = Joblist()
timelog = Timelog()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root.geometry("500x240")
root.title("Quick Jab")
root.iconbitmap(os.path.join('icons','punch.ico'))
root.resizable(False, False)

clock_bg = ctk.CTkLabel(master=root, text=None, width=325, height=100, fg_color='#000000', corner_radius=15)
clock_bg.place(x=20,y=20) 

clock_hours = ctk.CTkLabel(clock_bg, text="hr", font=("Roboto", 40), text_color='#333333')
clock_hours.place(x=85, y=32)
clock_minutes = ctk.CTkLabel(clock_bg, text="min", font=("Roboto", 40), text_color='#333333')
clock_minutes.place(x=220, y=32)

clock_hours_input = ctk.CTkEntry(clock_bg, width=70, height=100, font=("Roboto", 50), justify="right", fg_color='#000000', border_width=0)
clock_hours_input.place(x=10,y=3)
clock_minutes_input = ctk.CTkEntry(clock_bg, width=70, height=100, font=("Roboto", 50), justify="right", fg_color='#000000', border_width=0)
clock_minutes_input.place(x=145,y=3)

### PLAY PAUSE BTN
play_image = ctk.CTkImage(Image.open(os.path.join('icons','play_b.png')), size=(25,25))

count_btn = ctk.CTkButton(master=root, width=125, height=40, text=None, hover_color='#99CC99', corner_radius=7, image=play_image)
count_btn.place(x=355,y=28)

countup_image = ctk.CTkImage(Image.open(os.path.join('icons','up.png')), size=(20,20))
countdown_image = ctk.CTkImage(Image.open(os.path.join('icons','down.png')), size=(20,20))


countup_btn = ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, state="disabled", fg_color='#333333', hover_color='#666666', image = countup_image, command=jobtimer.switchcount )
countup_btn.place(x=355,y=78)
countdown_btn = ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, fg_color='#333333', hover_color='#666666', image = countdown_image,  command=jobtimer.switchcount )
countdown_btn.place(x=421,y=78)

jobtimer.setcountbtns()

dropdownlist = joblist.listjobs()
dropdownlist.insert(0, "Select job")
job_dropdown = ctk.CTkComboBox(root, values=dropdownlist, width = 325, height=35, corner_radius=7, border_width=0, font=("Roboto", 12))
job_dropdown.place (x=20, y=140)

def refresh_job_dropdown():
    dropdownlist = joblist.listjobs()
    dropdownlist.insert(0, "Select job")
    job_dropdown.configure(values=dropdownlist)
    job_dropdown.set("Select job")


### ADD JOB
addjob_image = ctk.CTkImage(Image.open(os.path.join('icons','add2.png')), size=(20,20))
deljob_image = ctk.CTkImage(Image.open(os.path.join('icons','delete.png')), size=(20,20))

time_input = ctk.CTkEntry(root, width=325, height=35, corner_radius=7)
time_input.place(x=20 , y=185)

addjob_btn =ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, fg_color='#333333', image=addjob_image, command=lambda: joblist.addjob(job_dropdown.get()) )
addjob_btn.place(x=355,y=140)
deljob_btn =ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, fg_color='#333333', hover_color='#990000', image=deljob_image, command=lambda: joblist.deletejob(job_dropdown.get()) )
deljob_btn.place(x=421,y=140)

### ADD LOG
addjob_image = ctk.CTkImage(Image.open(os.path.join('icons','add_b.png')), size=(20,20))

addtime_btn =ctk.CTkButton(master=root, width=125, height=35, text=None, text_color='#000000', hover_color='#99CC99', corner_radius=7, font=("Roboto Bold", 15), image=addjob_image, command= lambda: timelog.log_time(job_dropdown.get(),time_input.get()))
addtime_btn.place(x=355,y=185)

if __name__ == "__main__":
    root.mainloop()