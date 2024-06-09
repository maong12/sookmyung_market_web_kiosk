import chardet
import pymssql
import pandas as pd
import tkinter as tk
from tkinter import ttk

def get_data(code):
    if code=='1': #재고현황
        sqlCmd = "SELECT * FROM stock_view;"   
    elif code=='2': #매출현황
        sqlCmd = "SELECT ordertime, s.pnum, pname, qty, totalprice FROM salesSlip s, product p WHERE s.pnum = p.pnum;"    
    elif code=='3': #재고주문서 - 4개 테이블 join
        sqlCmd = "SELECT stk.pnum, p.pname, w.qty, w.wprice*w.qty, spl.sname, spl.phone FROM stock stk, product p, wholesale w, supplier spl WHERE stk.pnum = p.pnum AND stk.pnum = w.pnum AND p.snum = spl.snum AND stk.qty_current < stk.qty_reorder;"      
    elif code=='4': #재고현황
        sqlCmd = "SELECT pnum FROM stock;"
    else:
        print("ERROR")

    cursor.execute(sqlCmd)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    data_list = df.values.tolist()
    #print(df)
    Make_newWindow(code, data_list)

class Make_newWindow():
    def __init__(self,code, *data):
        if code == '1':
            self.message = "재고현황"
            win_size="700x600"
        elif code == '2':
            self.message = "매출현황"
            win_size="700x600"
        elif code == '3':
            self.message = "재고주문서"
            win_size="700x600"
        elif code == '4':
            self.message = "재고입고"
            win_size="300x400"
        elif code == '5':
            self.message = "신상품입고"
            win_size="300x400"
        #print(message)
        self.newWin = tk.Tk()
        self.newWin.title(self.message)
        self.newWin.geometry(win_size)
        self.newWin.resizable(True,True)
        if code in('1','2','3'): self.make_table(code, data[0])
        elif code == '4': self.get_stock(data[0])
        elif code == '5': self.get_new()
        self.newWin.mainloop()

    def make_table(self, code, treeData):
        ttk.Label(self.newWin, text=self.message).grid(row=0,column=0)

        #self.tree.column("#0", width=10, stretch=True, anchor="w")
        if code == '1':
            treeHeader = ['상품번호', '상품이름', '재고수량', '기본수량']
            treeWidth = [30, 20, 10, 10]
            treeHeight = 0.95
        elif code == '2':
            treeHeader = ['주문시각','상품번호','상품이름', '수량', '가격']
            treeWidth = [40, 10, 20, 10, 12]
            treeHeight = 0.95
        elif code == '3':
            treeHeader = ['상품번호', '상품이름', '주문수량', '도매가격', '공급자이름','공급자전화번호']
            treeWidth = [10,20,10,12,15,30]
            treeHeight = 0.85
            df=pd.DataFrame(treeData,columns=treeHeader)
            tk.Button(self.newWin, text="내보내기", command=lambda:orderSheet_out(df), state=tk.NORMAL).place(relx=0.45, rely=0.90)

        self.tree = tk.ttk.Treeview(self.newWin, columns=treeHeader, displaycolumns=treeHeader)
        self.tree.place(relx=0.02, rely=0.03, relwidth=0.96, relheight=treeHeight)

        self.tree.column("#0", width=2, stretch=True, anchor="w")
        for iCount in range(len(treeHeader)):
            strHdr = treeHeader[iCount]
            self.tree.heading(treeHeader[iCount], text=strHdr.title(), anchor="w")
            self.tree.column(treeHeader[iCount], width=treeWidth[iCount], stretch=True, anchor="w")

        for iCount in range(len(treeData)):
            self.tree.insert("", "end", text=iCount + 1,
                             values=treeData[iCount])

        self.newWin.columnconfigure(4, weight=1)
        self.newWin.rowconfigure(2, weight=1)
        #sb_y = ttk.Scrollbar(self.newWin, orient="vertical", command=self.tree.yview).place(relx=0.93, rely=0.05, relheight=0.85, relwidth=0.05)
        #self.tree.configure(yscrollcommand=sb_y.set)

    def get_stock(self, data):
        ttk.Label(self.newWin, text=self.message).grid(row=0, column=0)
        # combobox
        ttk.Label(self.newWin, text="상품번호").grid(row=1, column=0)
        self.combo = tk.ttk.Combobox(self.newWin)
        self.combo['values']=tuple(data)
        self.combo.current(0)
        self.combo.grid(column=1, row=1)
        #text
        ttk.Label(self.newWin, text="입고수량").grid(row=2, column=0)
        self.text = tk.Text(self.newWin, height=1, width=3)
        self.text.grid(column=1, row=2)
        #button
        tk.Button(self.newWin, text="확인", command=self.cmbtxt_check).grid(column=1, row=3)

    def cmbtxt_check(self):
        pnum = int(self.combo.get())
        qty = int(self.text.get("1.0", "end"))
        #print(pnum)
        #print(qty)
        #SQL
        sqlCmd = "UPDATE stock SET qty_current = qty_current+%d WHERE pnum = %d;"

        try:
            cursor.execute(sqlCmd %(qty, pnum))
            con.commit()
        except: ttk.Label(self.newWin, text="ERROR").grid(row=4, column=1)
        else: ttk.Label(self.newWin, text="정상적으로 처리되었습니다.").grid(row=4, column=1)

    def get_new(self):
        ttk.Label(self.newWin, text="신상품 추가").grid(row=0, column=0)
        self.pnum = tk.Entry(self.newWin)
        self.pnum.grid(column=0, row=2)
        self.pnum.insert(0,"상품번호")
        self.pname = tk.Entry(self.newWin)
        self.pname.grid(column=0, row=3)
        self.pname.insert(0, "상품이름")
        self.price = tk.Entry(self.newWin)
        self.price.grid(column=0, row=4)
        self.price.insert(0, "가격")
        self.qty = tk.Entry(self.newWin)
        self.qty.grid(column=0, row=5)
        self.qty.insert(0, "입고수량")
        self.dqty = tk.Entry(self.newWin)
        self.dqty.grid(column=0, row=6)
        self.dqty.insert(0, "기본수량설정")
        self.wprice = tk.Entry(self.newWin)
        self.wprice.grid(column=0, row=7)
        self.wprice.insert(0, "도매가격")
        self.wqty = tk.Entry(self.newWin)
        self.wqty.grid(column=0, row=8)
        self.wqty.insert(0, "도매수량")
        self.snum = tk.Entry(self.newWin)
        self.snum.grid(column=0, row=9)
        self.snum.insert(0, "공급자번호")
        tk.Button(self.newWin, text="확인", command=self.splr_check).grid(column=0, row=10)

    def splr_check(self):
        snum = int(self.snum.get())
        #print(self.snum)
        sqlCmd = "SELECT * FROM supplier WHERE snum=%d;"
        cursor.execute(sqlCmd % snum)
        rows = cursor.fetchall()
        #print(rows)
        if rows == []:
            self.sname = tk.Entry(self.newWin)
            self.sname.grid(column=0, row=11)
            self.sname.insert(0, "공급자이름")
            self.sphone = tk.Entry(self.newWin)
            self.sphone.grid(column=0, row=12)
            self.sphone.insert(0, "공급자전화번호")
            tk.Button(self.newWin, text="확인", command=self.add_splr).grid(column=0, row=13)
        else : self.add_new()

    def add_splr(self):
        snum=int(self.snum.get())
        sname=self.sname.get()
        sphone= str(self.sphone.get())
        sqlCmd = "set identity_insert supplier on; INSERT INTO supplier ([snum],[sname],[phone]) VALUES (%d, '%s', '%s'); set identity_insert supplier off;"

        try:
            print(chardet.detect(sname.encode()))
            cursor.execute(sqlCmd % (snum, sname, sphone))
            con.commit()
        except: ttk.Label(self.newWin, text="ERROR").grid(row=0, column=14)
        else: self.add_new()
        #print(type(snum), type(sname), type(sphone))
        #cursor.execute(sqlCmd % (snum, sname, sphone))
        #con.commit()
        #self.add_new()

    def add_new(self):
        pnum=int(self.pnum.get())
        pname = self.pname.get()
        price = int(self.price.get())
        qty = int(self.qty.get())
        dqty = int(self.dqty.get())
        wprice = int(self.wprice.get())
        wqty = int(self.wqty.get())
        snum = int(self.snum.get())

        sqlCmd1 = "set identity_insert product on; INSERT INTO product ([pnum], [pname],[price],[snum]) VALUES (%d, '%s', %d, %d); set identity_insert product off;"
        sqlCmd2 = "INSERT INTO stock VALUES (%d, %d, %d);"
        sqlCmd3 = "INSERT INTO wholesale VALUES (%d, %d, %d);"
        try:
            print(pnum, pname, price, snum)
            #print(chardet.detect(pname.encode()))
            cursor.execute(sqlCmd1 % (pnum, pname, price, snum))
            con.commit()
            cursor.execute(sqlCmd2 % (pnum, qty, dqty))
            con.commit()
            cursor.execute(sqlCmd3 % (pnum, wprice, wqty))
            con.commit()
        except:
            ttk.Label(self.newWin, text="ERROR").grid(row=1, column=1)
        else:
            ttk.Label(self.newWin, text="정상 처리 되었습니다.").grid(row=0, column=15)

def orderSheet_out(df):
    #print(df)
    df.to_csv('./ordersheet.csv',index=False, encoding='euc-kr')


con = pymssql.connect('DESKTOP-P5PRM6N','user','0000','ESQL_project',charset='cp949' ) #mssql 접속 EUC-KR
cursor = con.cursor()

window=tk.Tk()

window.title("숙명 매점(관리자용)")
window.geometry("305x485+100+100")
window.resizable(True, True)

tk.Button(window, text="재고현황", overrelief="solid", width=20, height=10, command=lambda: get_data('1')).grid(row=0,column=0)
tk.Button(window, text="매출현황", overrelief="solid", width=20, height=10, command=lambda: get_data('2')).grid(row=0,column=1)
tk.Button(window, text="재고주문서", overrelief="solid", width=20, height=10, command=lambda: get_data('3')).grid(row=1,column=0)
tk.Button(window, text="재고입고", overrelief="solid", width=20, height=10, command=lambda: get_data('4')).grid(row=1,column=1)
tk.Button(window, text="신상품입고", overrelief="solid", width=42, height=10, command=lambda: Make_newWindow('5')).grid(row=2,column=0,columnspan=2)


window.mainloop()
con.close()
