import customtkinter as ctk
import os
import datetime
import glob
from PIL import Image

os.makedirs('joblist', exist_ok=True)
os.makedirs('logs', exist_ok=True)

JOBLIST = os.path.join('joblist','joblist.txt')

class Jobtimer:
    def __init__(self):
        self.counting = False
        self.count_mode = "up" # default count mode
        self.clock_hours_input = None
        self.clock_minutes_input = None
        self._timer_after_id = None  

    def set_default_inputs(self):
        if self.clock_hours_input:
            self.clock_hours_input.delete(0, "end")
            self.clock_hours_input.insert(0, "0")
        if self.clock_minutes_input:
            self.clock_minutes_input.delete(0, "end")
            self.clock_minutes_input.insert(0, "00")
        
    def switchcount(self):
        if self.count_mode == "up":
            self.count_mode = "down"
            self.setcountbtns()
            countup_btn.configure(state="normal")
            countdown_btn.configure(state="disabled")
            

        else:
            self.count_mode = "up"
            self.setcountbtns()
            countup_btn.configure(state="disabled")
            countdown_btn.configure(state="normal")
            

    def setcountbtns(self):
        if self.count_mode == "up":
            countup_btn.configure(fg_color='#444444')
            countdown_btn.configure(fg_color='#333333')
        else:
            countdown_btn.configure(fg_color='#444444')
            countup_btn.configure(fg_color='#333333')

    def playpause(self):
        if not self.counting:
            try:
                hours = int(self.clock_hours_input.get())
            except Exception:
                hours = 0
            try:
                minutes = int(self.clock_minutes_input.get())
            except Exception:
                minutes = 0
            self.startcount(hours, minutes)
        else:
            self.stopcount()

    def startcount(self, hours=0, minutes=0):
        if self.count_mode == "down" and hours == 0 and minutes == 0:
            time_input.delete(0, "end")
            time_input.insert(0, "no time to countdown")
            return
        
        self.counting = True
        countup_btn.configure(state="disabled")
        countdown_btn.configure(state="disabled")
        self.count_btn.configure(fg_color="#990000", image=self.pause_image, hover_color="#AA0000")
        if self.count_mode == "up":
            self.starttime = hours * 3600 + minutes * 60
            self.countup(self.starttime)
        else:
            self.remaining = hours * 3600 + minutes * 60
            self.countdown(self.remaining)
        

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.counting:
            if self.clock_hours_input:
                self.clock_hours_input.configure(state="disabled")
            if self.clock_minutes_input:
                self.clock_minutes_input.configure(state="disabled")

        if self.remaining <= 0:
            self.timesup()
            
            if self.clock_hours_input:
                self.clock_hours_input.configure(state="normal")
            if self.clock_minutes_input:
                self.clock_minutes_input.configure(state="normal")
        else:
            hours = int(self.remaining / 3600)
            minutes = int(self.remaining / 60 ) % 60
            if self.clock_hours_input:
                self.clock_hours_input.configure(state="normal")
                self.clock_hours_input.delete(0, "end")
                self.clock_hours_input.insert(0, f"{hours}")
                self.clock_hours_input.configure(state="disabled")
            if self.clock_minutes_input:
                self.clock_minutes_input.configure(state="normal")
                self.clock_minutes_input.delete(0, "end")
                self.clock_minutes_input.insert(0, f"{minutes:02}")
                self.clock_minutes_input.configure(state="disabled")
            self.remaining -= 1
            if self.counting:
                self._timer_after_id = root.after(1000, self.countdown)
            else:
                self._timer_after_id = None

    def countup(self, startingat=None):
        if startingat is not None:
            self.starttime = startingat
        self.counting = True

        if self.clock_hours_input:
            self.clock_hours_input.configure(state="disabled")
        if self.clock_minutes_input:
            self.clock_minutes_input.configure(state="disabled")

        hours = int(self.starttime / 3600)
        minutes = int(self.starttime / 60 ) % 60
        if self.clock_hours_input:
            self.clock_hours_input.configure(state="normal")
            self.clock_hours_input.delete(0, "end")
            self.clock_hours_input.insert(0, f"{hours}")
            self.clock_hours_input.configure(state="disabled")
        if self.clock_minutes_input:
            self.clock_minutes_input.configure(state="normal")
            self.clock_minutes_input.delete(0, "end")
            self.clock_minutes_input.insert(0, f"{minutes:02}")
            self.clock_minutes_input.configure(state="disabled")
        self.starttime += 1
        if self.counting:
            self._timer_after_id = root.after(1000, self.countup)
        else:
            self._timer_after_id = None

    def stopcount(self):
        self.counting = False
        if self._timer_after_id is not None:
            root.after_cancel(self._timer_after_id)
            self._timer_after_id = None
        if self.clock_hours_input:
            self.clock_hours_input.configure(state="normal")
        if self.clock_minutes_input:
            self.clock_minutes_input.configure(state="normal")
        self.count_btn.configure(fg_color=["#2CC985", "#2FA572"], image=self.play_image, hover_color="#99cc99")
        if self.count_mode == "up":
            countdown_btn.configure(state="normal")
            try:
                hours = int(self.clock_hours_input.get())
            except Exception:
                hours = 0
            try:
                minutes = int(self.clock_minutes_input.get())
            except Exception:
                minutes = 0
            time_input.delete(0, "end")
            time_input.insert(0, f"{hours:01}hr {minutes:02}min")
        else:
            countup_btn.configure(state="normal")

    def timesup(self):
        self.counting = False
        countup_btn.configure(state="normal")
        stopped_at = datetime.datetime.now().strftime("Stopped at %H:%M")
        self.count_btn.configure(fg_color=["#2CC985", "#2FA572"], image=self.play_image, hover_color="#99cc99")
        time_input.delete(0, "end")
        time_input.insert(0, stopped_at)
        

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
            return  
        if jobname not in self.jobs:
            self.jobs.append(jobname)
            with open(JOBLIST, "w") as file:
                for item in self.jobs:
                    file.write(item + '\n')
        refresh_job_dropdown()

    def deletejob(self, jobtodelete):
        if jobtodelete == "Select job" or not jobtodelete.strip():
            return  
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
        self.fulldate = datetime.date.today() # needs to be initialised at time of log
        if jobname != "Select job" and input.strip():
            output = (f'{self.cur_date}   {jobname}   {input}')
            with open(self.cur_log, "a") as file:
                file.write(output + "\n")
            time_input.delete(0, "end")
            job_dropdown.set("Select job")
            

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

clock_hours_input = ctk.CTkEntry(clock_bg, width=70, height=100, font=("Roboto", 50), 
                                 justify="right", fg_color='#000000', border_width=0)
clock_hours_input.place(x=10,y=3)

clock_minutes_input = ctk.CTkEntry(clock_bg, width=70, height=100, font=("Roboto", 50), 
                                   justify="right", fg_color='#000000', border_width=0)
clock_minutes_input.place(x=145,y=3)

jobtimer.clock_hours_input = clock_hours_input
jobtimer.clock_minutes_input = clock_minutes_input
jobtimer.set_default_inputs()

### PLAY PAUSE BTN
play_image = ctk.CTkImage(Image.open(os.path.join('icons','play_b.png')), size=(25,25))
pause_image = ctk.CTkImage(Image.open(os.path.join('icons','pause.png')), size=(25,25))


count_btn = ctk.CTkButton(master=root, width=125, height=40, text=None, hover_color='#99CC99', 
                          corner_radius=7, image=play_image,
                          command=jobtimer.playpause)
count_btn.place(x=355,y=28)

jobtimer.count_btn = count_btn
jobtimer.play_image = play_image
jobtimer.pause_image = pause_image

countup_image = ctk.CTkImage(Image.open(os.path.join('icons','up.png')), size=(20,20))
countdown_image = ctk.CTkImage(Image.open(os.path.join('icons','down.png')), size=(20,20))


countup_btn = ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, 
                            state="disabled", fg_color='#333333', hover_color='#666666', image = countup_image, 
                            command=jobtimer.switchcount )
countup_btn.place(x=355,y=78)

countdown_btn = ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, 
                              fg_color='#333333', hover_color='#666666', image = countdown_image,  
                              command=jobtimer.switchcount )
countdown_btn.place(x=421,y=78)

jobtimer.setcountbtns()

dropdownlist = joblist.listjobs()
dropdownlist.insert(0, "Select job")
job_dropdown = ctk.CTkComboBox(root, values=dropdownlist, width = 325, height=35, 
                               corner_radius=7, border_width=0, font=("Roboto", 12))
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

addjob_btn =ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, 
                          fg_color='#333333', image=addjob_image, 
                          command=lambda: joblist.addjob(job_dropdown.get()) )
addjob_btn.place(x=355,y=140)


deljob_btn =ctk.CTkButton(master=root, width=58, height=35, text=None, corner_radius=7, 
                          fg_color='#333333', hover_color='#990000', image=deljob_image, 
                          command=lambda: joblist.deletejob(job_dropdown.get()) )
deljob_btn.place(x=421,y=140)

### ADD LOG
addjob_image = ctk.CTkImage(Image.open(os.path.join('icons','add_b.png')), size=(20,20))
addtime_btn = ctk.CTkButton(master=root, width=125, height=35, text=None, 
                            text_color='#000000', hover_color='#99CC99', 
                            corner_radius=7, font=("Roboto Bold", 15), image=addjob_image, 
                            command= lambda: timelog.log_time(job_dropdown.get(),time_input.get()))
addtime_btn.place(x=355,y=185)

if __name__ == "__main__":
    root.mainloop()