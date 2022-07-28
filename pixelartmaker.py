# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tkinter as tk
from tkinter.ttk import Style, Button
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps


############## <summary> ###############
##                                   
##   画像をドット絵に変換するアプリ    
##   プレビュー機能つき 次 → 保存
##   それぞれの値を入れた状態で動作する
##   アルファ値:ドットサイズ
##   K値:減色処理,色数
##                                
############# </summary> ###############

class Application(tk.Frame):

    dotnum = 16
    alpha = 0.0
    K = 8
    tmp_file_name = "./tmpdot.png" #今のディレクトリに作る用

    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        self.master.geometry("1200x800")     # ウィンドウサイズ(幅x高さ)
        self.master.title("Pixel Art Maker")       # タイトル
        
        # メニューの作成
        self.create_menu()

        # Canvasの作成
        self.back_color = "lightgray" # 背景色
        self.canvas = tk.Canvas(self.master, bg = self.back_color, width=850, height=800) #Canvasオプション

        # Canvasを配置
        self.canvas.place(x=0, y=0)

        self.create_widgets() #ウィジェット作成

########################################################################################################################## <表示系>
    # メニュー作成
    def create_menu(self):
        # メニューバーの作成
        menubar = tk.Menu(self)

        # ファイルメニュー
        menu_file = tk.Menu(menubar, tearoff = False)
        menu_file.add_command(label = "画像ファイルを開く", command = self.menu_file_open_click, accelerator="Ctrl+O")
        menu_file.add_separator() # 仕切り線
        menu_file.add_command(label = "Exit", command = self.master.destroy)

        # ショートカットキーの関連付け
        menu_file.bind_all("<Control-o>", self.menu_file_open_click)

        # メニューバーに各メニューを追加
        menubar.add_cascade(label="ファイル", menu = menu_file)

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        self.master.config(menu = menubar)
    
    ######################################### <ウィジェット作成>
    def create_widgets(self):
        ############### ボタン
        btnref = tk.Button(self.master, text="参照",command = self.btnclick_ref) #command = ???
        btnref.place(x=1160, y=98)

        btnpre = tk.Button(self.master, text="プレビュー",width = "46",command = self.btn_preview)
        btnpre.place(x=860, y=270, width=330, height = 50)

        btnsave = tk.Button(self.master, text="保存", command = self.btn_savefile) #state="disable"
        btnsave.place(x=860, y=700, width=330, height = 50)

        #btnsave = tk.Button(self.master, text="保存",state = "disable",width = "40")

        ############### ラベル,表示テキスト
        lbl_filename = tk.Label(text="ファイル名")
        lbl_filename.place(x=870, y=100)
        lbl_dotnum = tk.Label(text="短辺のピクセル数(>0)")
        lbl_dotnum.place(x=870, y=150)
        lbl_K = tk.Label(text="色の数(K値>0)")
        lbl_K.place(x=870, y=200)

        ############### テキストボックス,入力テキスト
        self.txt_filename = tk.Entry()
        self.txt_filename.place(x=934, y=100, width= 220, height = 23)

        self.txt_dotnum = tk.Entry()
        self.txt_dotnum.insert(tk.END,"16") #初期値
        self.txt_dotnum.place(x=990, y=150, width= 163, height = 23)

        self.txt_K = tk.Entry()
        self.txt_K.insert(tk.END,"8") #初期値
        self.txt_K.place(x=990, y=200, width= 163, height = 23)

        self.txt_savefilename = tk.Entry()
        self.txt_savefilename.insert(tk.END,"8") #初期値
        self.txt_savefilename.place(x=990, y=200, width= 163, height = 23)

    ######################################### </ウィジェット作成>

########################################################################################################################## </表示系>


########################################################################################################################## <機能系>
    def menu_file_open_click(self, event=None):
        idir = "./" #自分自身のディレクトリ
        filetype = [("すべて","*"), ("png","*.png"), ("jpg","*.jpg")] #ファイルフィルタ ("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif")
        file_path = tk.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
        if(file_path != ""):
            self.txt_filename.delete(0,tk.END)
            self.txt_filename.insert(tk.END,file_path)
        self.disp_image(file_path) # 画像の表示

    def disp_image(self, filename):
        """画像をCanvasに表示する"""
        if not filename:
            return

        # PIL.Imageで開く
        pil_image = Image.open(filename)

        # キャンバスのサイズを取得
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height), color = self.back_color)

        #PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.create_image(
                canvas_width / 2,       # 画像表示位置(Canvasの中心)
                canvas_height / 2,                   
                image=self.photo_image,  # 表示画像データ
                tag="img"
                )

########################################################################## <クリックイベント>

    def btnclick_ref(self): #参照ボタン
        idir = "./" #自分自身のディレクトリ
        filetype = [("すべて","*"), ("png","*.png"), ("jpg","*.jpg")] #ファイルタイプ,追加可能
        file_path = tk.filedialog.askopenfilename(filetypes = filetype, initialdir = idir)
        if(file_path != ""):
            self.txt_filename.delete(0,tk.END)
            self.txt_filename.insert(tk.END,file_path)
        self.disp_image(file_path) # 画像の表示

    def btn_preview(self):
        self.canvas.delete("img")
    
        if(self.txt_filename.get() != "" and self.txt_dotnum.get() != "" and self.txt_K.get() != ""):
            dotnum = int(self.txt_dotnum.get())
            K = int(self.txt_K.get())
            if(dotnum > 0 and K > 0): #isinstance(dotnum,int) and isinstance(K,int)
                # 入力画像を取得
                img = cv2.imread(self.txt_filename.get())
                h,w,c = img.shape
                
                if(h<w): #短辺の判断
                    num1 = dotnum / float(h)
                elif(h>=w):
                    num1 = dotnum / float(w)

                num2 = int(self.txt_K.get())
                # ドット絵化
                dst = self.pixel_art(img, num1, num2) #アルファ値：モザイクの大きさ　K値：色の数
                # 結果を出力
                cv2.imwrite("./tmpdot.png", dst)
                # 16進数へ変換してテキストボックスへセット

                self.disp_image("./tmpdot.png")

        else: #もっと書き方あるだろー！！！！！
            if(self.txt_filename.get() == ""):
                self.txt_filename.config(bg="red")
            else:
                self.txt_filename.config(bg="white")
            if(self.txt_dotnum.get() == "" or int(self.txt_dotnum.get()) <= 0):
                self.txt_dotnum.config(bg="red")
            else:
                self.txt_dotnum.config(bg="white")
            if(self.txt_K.get() == "" or int(self.txt_dotnum.get()) <= 0):
                self.txt_K.config(bg="red")
            else:
                self.txt_K.config(bg="white")

    def btn_savefile(self):
        idir = "./" #自分自身のディレクトリ
        filetype = [("png","*.png"), ("jpg","*.jpg"), ("すべて","*")] #ファイルタイプ,追加可能
        fname = filedialog.asksaveasfilename(filetypes = filetype, initialdir = idir)

        if(self.txt_filename.get() != "" and self.txt_dotnum.get() != "" and self.txt_K.get() != ""):
            dotnum = int(self.txt_dotnum.get())
            K = int(self.txt_K.get())
            if(dotnum > 0 and K > 0 and fname != ""): #isinstance(dotnum,int) and isinstance(K,int)
                print(fname)
                # 入力画像を取得
                img = cv2.imread(self.txt_filename.get())
                h,w,c = img.shape
                
                if(h<w): #短辺の判断
                    num1 = dotnum / float(h)
                elif(h>=w):
                    num1 = dotnum / float(w)

                num2 = int(self.txt_K.get())
                # ドット絵化
                dst = self.pixel_art(img, num1, num2) #アルファ値：モザイクの大きさ　K値：色の数

                # 結果を出力
                cv2.imwrite(fname+".png", dst)
                # 16進数へ変換してテキストボックスへセット

                self.disp_image(fname+".png")

        else: #もっと書き方あるだろー！！！！！
            if(self.txt_filename.get() == ""):
                self.txt_filename.config(bg="red")
            else:
                self.txt_filename.config(bg="white")
            if(self.txt_dotnum.get() == "" or int(self.txt_dotnum.get()) <= 0):
                self.txt_dotnum.config(bg="red")
            else:
                self.txt_dotnum.config(bg="white")
            if(self.txt_K.get() == "" or int(self.txt_dotnum.get()) <= 0):
                self.txt_K.config(bg="red")
            else:
                self.txt_K.config(bg="white")

########################################################################################################################## </機能系>

    
########################################################################################################################## <ドット変換>
        # 減色処理
    def sub_color(self,src, K):
        # 次元数を1落とす
        Z = src.reshape((-1,3))

        # float32型に変換
        Z = np.float32(Z)

        # 基準の定義
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        # K-means法で減色
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # UINT8に変換
        center = np.uint8(center)

        res = center[label.flatten()]

        # 配列の次元数と入力画像と同じに戻す
        return res.reshape((src.shape))


    # モザイク処理
    def mosaic(self,img, alpha):
        # 画像の高さ、幅、チャンネル数
        h, w, ch = img.shape

        # 縮小→拡大でモザイク加工
        img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
        img = cv2.resize(img,(w, h), interpolation=cv2.INTER_NEAREST)

        return img


    # ドット絵化
    def pixel_art(self,img, alpha=2, K=4):
        # モザイク処理
        img = self.mosaic(img, alpha)

        # 減色処理
        return self.sub_color(img, K)

########################################################################################################################## </ドット変換>


###################### OMAJINAI ######################
if __name__ == "__main__":

    root = tk.Tk()
    app = Application(master = root) #tk.Frame
    app.mainloop()
