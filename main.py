# Proje Tarihi;
# 24.05.2021
#
# Modüller;

from tkinter import *
from tkinter import messagebox
from youtube_dl import YoutubeDL
import threading
import webbrowser
import os
import subprocess
import urllib.request
from io import BytesIO
from PIL import ImageTk, Image

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        F1 = Frame(self.master, bg="#6E7371")
        F1.pack(pady=30)
        
        # Butonlara koyacağımız resimleri ayarlıyoruz.
        photo = PhotoImage(file= r"img\plus.png")
        self.image1 = photo.subsample(9,9)
        photomp2 = PhotoImage(file = r"img\download.png")
        self.image2 = photomp2.subsample(9,9)

        # Widgetler
        F2 = Frame(F1, width="450")
        F2.grid(row=0,column=0, pady=20)
        pasteurl = Button(F1, text="Bağlantı Yapıştır", image=self.image1, compound=LEFT,bg="#6E7371",fg="white",cursor="hand2",command=self.bglnthrd) 
        pasteurl.grid(row=1,column=0,padx=20)
        
        self.percent_alt = Label(F1, bg="#6E7371", fg="white", font="Calibri 15")
        self.percent_alt.grid(row=2,column=0,pady=30,padx=50)

        self.url = Label(self.master,bg="#6E7371",fg="white")
        self.url.place(x=10,y=25)

        self.F3 = Frame(self.master,bg="#6E7371")

        self.file_path = Label(self.master, text="", font="bold", bg="#6E7371", fg="#30d5c8")
        self.file_path.pack(pady=55)

        # Pencerenin altında bulunan Developer kısmı.
        def callback(url):
            webbrowser.open_new(url)
        self.me = Label(self.master, text="Developer: yazilimfuryasi.com | @yazilimfuryasi",bg="#6E7371", fg="#30d5c8",cursor="hand2",font="Verdana 7 bold")
        self.me.place(x=120,y=190)
        self.me.bind("<Button-1>", lambda e: callback(webbrowser.open_new("https://www.instagram.com/yazilimfuryasi/")))


    def bglnthrd(self):
        # URL okunurken programın donmasını engellemek için kullanılır.
        # Yani, kodları iş parçacıklarına böler ve aynı anda birden fazla iş yapmasını sağlar.
        threading.Thread(target=self.bglnt).start()

    def bglnt(self):
        root.geometry("480x210")

        self.url["text"] = ""

        # Panoya kopyalanan öğeyi alır
        paste = root.clipboard_get()

        # Bu işleme gerek yoktur öylesine koydum :) 
        if len(paste) >= 200:
            messagebox.showerror("Çok Uzun", f"El İnsaf Be Adam Bu Nasıl Link?\n")

        # Bu koşulda URL kontrolü ediyoruz 
        if paste.count("youtube.com") != 0 or paste.count("youtu.be") != 0:
            self.url["text"] = paste
            self.url.config(cursor="hand2")
            self.url.bind("<Button-1>", lambda e: callback(root.clipboard_get()))
            self.icerik()

        else:
            messagebox.showerror("Hata", f"Doğru Bağlantı olduğuna emin olunuz.\n")
        
    def icerik(self):
        # Yapıştırılan bağlantı doğru ise bu kısıma geçiyor.
        # 
        self.percent_alt["text"] = "ALINIYOR..."
        if self.F3:
            self.F3.destroy()
            self.file_path["text"] = ""
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')

        # youtube-dl indirme ayarları
        ydl_opts = {
        'noplaylist':True,
        'outtmpl': desktop+'/MyApp/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'progress_hooks': [self.percent],

        # Eğer ffmpeg modülü kullanarak mp3 e dönüştürmek istiyorsanız
        # bu kısmı yorum satırından kaldırın (tavsiye etmem)

        # 'postprocessors': [{
        #     'key': 'FFmpegExtractAudio',
        #     'preferredcodec': 'mp3',
        #     'preferredquality': '192',   
        # }]
        }

        video = self.url["text"]
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video, False)
            
            self.F3 = Frame(self.master,bg="#6E7371")
            self.F3.place(x=15,y=210)

            def mp3indir():
                with YoutubeDL(ydl_opts) as ydl: 
                    # True ile indirmeyi aktif ederiz
                    ydl.extract_info(video, True)

                    eski = ".webm"
                    yeni = ".mp3"
                    isim = info_dict.get('title', None)
                    
                    file = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads'+'\MyApp')
                    
                    # Burada dosya uzantısını değiştiririz. (webm olarak iner. Burada mp3 olarak değişiyoruz.)
                    # Eğer yukarıda bahsettiğim ffmpeg ile indirme işlemini aktif ettiyseniz,
                    # bu kısmı silin veya yorum satırı haline getirin.
                    gdosya = os.path.join(file, isim+eski)
                    os.path.splitext(isim)
                    yeniAd = gdosya.replace(eski, yeni)

                    try:
                        os.rename(gdosya,yeniAd)
                    except WindowsError:
                        os.remove(yeniAd)
                        os.rename(gdosya, yeniAd)

                    # Dosya indikten sonra, inen klasöre gitmek için bu işlemi yaptık
                    self.file_path.bind("<Button-1>", lambda e: subprocess.Popen(r'explorer '+desktop+'\MyApp'))
                    self.file_path["text"] = (desktop+r"\MyApp   |   İndirilenlere Git")
                    self.file_path.config(cursor="hand2")
                    self.percent_alt["text"] = ("İndirildi.")
            
            def indirthrd():
                # indir butonuna basılınca bu işlem çalışır.
                # indirme işlemi yaparken programın donmasını engellemek için kullanılır.
                # Yani, kodları iş parçacıklarına böler ve aynı anda birden fazla iş yapmasını sağlar.
                threading.Thread(target=mp3indir).start()

            # Video başlığı
            video_title = info_dict.get('title', None)
            # Video süresi
            video_length = info_dict.get('duration')
            # Küçük resim
            video_thumb = info_dict.get("thumbnail")
            
            video_length = video_length % (24 * 3600)
            root.geometry("480x380")
            self.me.pack(side=BOTTOM)
            hour = video_length // 3600
            video_length %= 3600
            minutes = video_length // 60
            video_length %= 60
            seconds = video_length

            self.percent_alt["text"] = ""
            self.lbal = Label(self.F3, bg="#6E7371",fg="white",font="Vardana 9 bold")
            self.lbal.grid(row=0, column=1, sticky = NW)
                        
            lbal2 = Label(self.F3,text="",bg="#6E7371",fg="white")
            lbal2.grid(row=0, column=1, sticky = SW)
            lresim = Label(self.F3,image=self.ImgFromUrl(video_thumb))
            lresim.grid(row = 0, column = 0, sticky = E)

            self.lbal["text"] = video_title
            lbal2["text"] = (f"Süre: %d:%d:%d" % (hour, minutes, seconds))
            indirBtn = Button(root, bg="#6E7371",fg="white",text="İndir", image=self.image2, compound=LEFT, cursor="hand2", padx=15, command=indirthrd)
            indirBtn.place(x=190,y=235)

    # inerken % olarak ekrana yazdırıyoruz
    def percent(self, d):
        if d['status'] == 'finished':
            self.percent_alt["text"] = ("Dönüştürülüyor...")
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            self.percent_alt["text"] = (p+"%")

    # Burada, küçük resmin okunmasını ve yeniden boyutlandırılmasını sağlıyoruz 
    def ImgFromUrl(self,video_thumb):
        with urllib.request.urlopen(video_thumb) as connection:
            raw_data = connection.read()
        im = Image.open(BytesIO(raw_data))
        resized = im.resize((82,45), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        return self.image

root = Tk()

app = Window(root)
root.wm_title("Youtube Mp3 indir | 24.05.2021 | v1.0")

# Bu kısımda, programın programın başlama noktasını ayarlıyoruz
# Yani pencereyi ortalamasını sağlıyoruz
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2)
root.geometry(f"480x210+{positionRight}+{positionDown}")
root.resizable(width=False, height=False)
root.configure(bg='#6E7371')

root.mainloop()