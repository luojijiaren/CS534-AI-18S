import tkinter  # 导入Tkinter模块
from PIL import Image, ImageTk
import io

root = tkinter.Tk()
canvas = tkinter.Canvas(root,
                        width=760,  # 指定Canvas组件的宽度
                        height=760,  # 指定Canvas组件的高度
                        bg='white')  # 指定Canvas组件的背景色
# im = Tkinter.PhotoImage(file='img.gif')     # 使用PhotoImage打开图片
image = Image.open("/home/jiaming/WPI/CS534/CS534-AI-18S/Final Project/DrawBoardwithTinker/background_1.jpg")
width,height = image.size
print("width,height",width,height)
im = ImageTk.PhotoImage(image)

canvas.create_image(300, 300, image=im)

canvas.pack()


#canvas.create_line(20,20,970,20)

lengt = 40
w_ = 2

for i in range(19):
    canvas.create_line(20,20+i*lengt,20+18*lengt,20+i*lengt,width = w_)
    canvas.create_line(20+i*lengt,20,20+i*lengt,20+18*lengt,width = w_)

# x_cor = 20 + 3*lengt
# y_cor = 20 + 3*lengt

radius = 5
for i in range(3):
    x_cor_1 = 20+3*lengt
    y_cor_1 = 20 + 3*lengt + i*6*lengt
    for j in range(3):
        x_cor = x_cor_1 + j*6*lengt
        y_cor = y_cor_1
        canvas.create_oval(x_cor-radius,y_cor-radius,x_cor+radius,y_cor+radius,outline = 'black',fill='black')


    #canvas.create_line(20+i*50,20,20+i*50,970)

# ps = canvas.postscript(colormode='color')
# img = Image.open(io.BytesIO(ps.encode('utf-8')))
# img.save('test.jpg')

#### Convert the canvas into .ps, convert it to .jpg file
# canvas.update()
# canvas.postscript(file="board.ps", colormode='color')

root.mainloop()