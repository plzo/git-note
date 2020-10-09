import xlwt
import os
workbook=xlwt.Workbook(encoding='utf-8')
booksheet=workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
DATA=(('学号','姓名','年龄','性别','成绩'),
   ('1001','A','11','男','12'),
   ('1002','B','12','女','22'),
   ('1003','C','13','女','32'),
   ('1004','D','14','男','52'),
   )
for i,row in enumerate(DATA):
  for j,col in enumerate(row):
    booksheet.write(i,j,col)
workbook.save('grade.xlsx')
print (os.getcwd())