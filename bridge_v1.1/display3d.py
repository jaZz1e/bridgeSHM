#jazzy!
#jazzycui@foxmail.com
 
import vtk
# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget


##load reader
reader_zl1 = vtk.vtkSTLReader()
reader_zl1.SetFileName("./stl/zl_1.stl")
reader_zl2 = vtk.vtkSTLReader()
reader_zl2.SetFileName("./stl/zl_2.stl")
reader_zl3 = vtk.vtkSTLReader()
reader_zl3.SetFileName("./stl/zl_3.stl")
reader_zl4 = vtk.vtkSTLReader()
reader_zl4.SetFileName("./stl/zl_4.stl")
reader_zl5 = vtk.vtkSTLReader()
reader_zl5.SetFileName("./stl/zl_5.stl")
reader_zl6 = vtk.vtkSTLReader()
reader_zl6.SetFileName("./stl/zl_6.stl")
reader_zl7 = vtk.vtkSTLReader()
reader_zl7.SetFileName("./stl/zl_7.stl")
reader_zl8 = vtk.vtkSTLReader()
reader_zl8.SetFileName("./stl/zl_8.stl")
reader_zl9 = vtk.vtkSTLReader()
reader_zl9.SetFileName("./stl/zl_9.stl")
reader_zl10 = vtk.vtkSTLReader()
reader_zl10.SetFileName("./stl/zl_10.stl")
reader_zl11 = vtk.vtkSTLReader()
reader_zl11.SetFileName("./stl/zl_11.stl")

reader_zz1 = vtk.vtkSTLReader()
reader_zz1.SetFileName("./stl/zz_1.stl")
reader_zz2 = vtk.vtkSTLReader()
reader_zz2.SetFileName("./stl/zz_2.stl")
reader_zz3 = vtk.vtkSTLReader()
reader_zz3.SetFileName("./stl/zz_3.stl")
reader_zz4 = vtk.vtkSTLReader()
reader_zz4.SetFileName("./stl/zz_4.stl")
reader_zz5 = vtk.vtkSTLReader()
reader_zz5.SetFileName("./stl/zz_5.stl")
reader_zz6 = vtk.vtkSTLReader()
reader_zz6.SetFileName("./stl/zz_6.stl")
reader_zz7 = vtk.vtkSTLReader()
reader_zz7.SetFileName("./stl/zz_7.stl")
reader_zz8 = vtk.vtkSTLReader()
reader_zz8.SetFileName("./stl/zz_8.stl")
reader_zz9 = vtk.vtkSTLReader()
reader_zz9.SetFileName("./stl/zz_9.stl")
reader_zz10 = vtk.vtkSTLReader()
reader_zz10.SetFileName("./stl/zz_10.stl")
reader_zz11 = vtk.vtkSTLReader()
reader_zz11.SetFileName("./stl/zz_11.stl")
reader_zz12 = vtk.vtkSTLReader()
reader_zz12.SetFileName("./stl/zz_12.stl")

reader_lg1 = vtk.vtkSTLReader()
reader_lg1.SetFileName("./stl/lg_1.stl")
reader_lg2 = vtk.vtkSTLReader()
reader_lg2.SetFileName("./stl/lg_2.stl")

reader_bj1 = vtk.vtkSTLReader()
reader_bj1.SetFileName("./stl/bj_1.stl")
reader_bj2 = vtk.vtkSTLReader()
reader_bj2.SetFileName("./stl/bj_2.stl")

#load mapper
mapper_zl1 = vtk.vtkPolyDataMapper()
mapper_zl2 = vtk.vtkPolyDataMapper()
mapper_zl3 = vtk.vtkPolyDataMapper()
mapper_zl4 = vtk.vtkPolyDataMapper()
mapper_zl5 = vtk.vtkPolyDataMapper()
mapper_zl6 = vtk.vtkPolyDataMapper()
mapper_zl7 = vtk.vtkPolyDataMapper()
mapper_zl8 = vtk.vtkPolyDataMapper()
mapper_zl9 = vtk.vtkPolyDataMapper()
mapper_zl10 = vtk.vtkPolyDataMapper()
mapper_zl11 = vtk.vtkPolyDataMapper()

mapper_zz1 = vtk.vtkPolyDataMapper()
mapper_zz2 = vtk.vtkPolyDataMapper()
mapper_zz3 = vtk.vtkPolyDataMapper()
mapper_zz4 = vtk.vtkPolyDataMapper()
mapper_zz5 = vtk.vtkPolyDataMapper()
mapper_zz6 = vtk.vtkPolyDataMapper()
mapper_zz7 = vtk.vtkPolyDataMapper()
mapper_zz8 = vtk.vtkPolyDataMapper()
mapper_zz9 = vtk.vtkPolyDataMapper()
mapper_zz10 = vtk.vtkPolyDataMapper()
mapper_zz11 = vtk.vtkPolyDataMapper()
mapper_zz12 = vtk.vtkPolyDataMapper()

mapper_lg1 = vtk.vtkPolyDataMapper()
mapper_lg2 = vtk.vtkPolyDataMapper()

mapper_bj1 = vtk.vtkPolyDataMapper()
mapper_bj2 = vtk.vtkPolyDataMapper()

if vtk.VTK_MAJOR_VERSION <= 5:
   mapper_zl1.SetInput(reader_zl1.GetOutput())
   mapper_zl2.SetInput(reader_zl2.GetOutput())
   mapper_zl3.SetInput(reader_zl3.GetOutput())
   mapper_zl4.SetInput(reader_zl4.GetOutput())
   mapper_zl5.SetInput(reader_zl5.GetOutput())
   mapper_zl6.SetInput(reader_zl6.GetOutput())
   mapper_zl7.SetInput(reader_zl7.GetOutput())
   mapper_zl8.SetInput(reader_zl8.GetOutput())
   mapper_zl9.SetInput(reader_zl9.GetOutput())
   mapper_zl10.SetInput(reader_zl10.GetOutput())
   mapper_zl11.SetInput(reader_zl11.GetOutput())

   mapper_zz1.SetInput(reader_zz1.GetOutput())
   mapper_zz2.SetInput(reader_zz2.GetOutput())
   mapper_zz3.SetInput(reader_zz3.GetOutput())
   mapper_zz4.SetInput(reader_zz4.GetOutput())
   mapper_zz5.SetInput(reader_zz5.GetOutput())
   mapper_zz6.SetInput(reader_zz6.GetOutput())
   mapper_zz7.SetInput(reader_zz7.GetOutput())
   mapper_zz8.SetInput(reader_zz8.GetOutput())
   mapper_zz9.SetInput(reader_zz9.GetOutput())
   mapper_zz10.SetInput(reader_zz10.GetOutput())
   mapper_zz11.SetInput(reader_zz11.GetOutput())
   mapper_zz12.SetInput(reader_zz12.GetOutput())

   mapper_lg1.SetInput(reader_lg1.GetOutput())
   mapper_lg2.SetInput(reader_lg2.GetOutput())

   mapper_bj1.SetInput(reader_bj1.GetOutput())
   mapper_bj2.SetInput(reader_bj2.GetOutput())

else:
   mapper_zl1.SetInputConnection(reader_zl1.GetOutputPort())
   mapper_zl2.SetInputConnection(reader_zl2.GetOutputPort())
   mapper_zl3.SetInputConnection(reader_zl3.GetOutputPort())
   mapper_zl4.SetInputConnection(reader_zl4.GetOutputPort())
   mapper_zl5.SetInputConnection(reader_zl5.GetOutputPort())
   mapper_zl6.SetInputConnection(reader_zl6.GetOutputPort())
   mapper_zl7.SetInputConnection(reader_zl7.GetOutputPort())
   mapper_zl8.SetInputConnection(reader_zl8.GetOutputPort())
   mapper_zl9.SetInputConnection(reader_zl9.GetOutputPort())
   mapper_zl10.SetInputConnection(reader_zl10.GetOutputPort())
   mapper_zl11.SetInputConnection(reader_zl11.GetOutputPort())

   mapper_zz1.SetInputConnection(reader_zz1.GetOutputPort())
   mapper_zz2.SetInputConnection(reader_zz2.GetOutputPort())
   mapper_zz3.SetInputConnection(reader_zz3.GetOutputPort())
   mapper_zz4.SetInputConnection(reader_zz4.GetOutputPort())
   mapper_zz5.SetInputConnection(reader_zz5.GetOutputPort())
   mapper_zz6.SetInputConnection(reader_zz6.GetOutputPort())
   mapper_zz7.SetInputConnection(reader_zz7.GetOutputPort())
   mapper_zz8.SetInputConnection(reader_zz8.GetOutputPort())
   mapper_zz9.SetInputConnection(reader_zz9.GetOutputPort())
   mapper_zz10.SetInputConnection(reader_zz10.GetOutputPort())
   mapper_zz11.SetInputConnection(reader_zz11.GetOutputPort())
   mapper_zz12.SetInputConnection(reader_zz12.GetOutputPort())

   mapper_lg1.SetInputConnection(reader_lg1.GetOutputPort())
   mapper_lg2.SetInputConnection(reader_lg2.GetOutputPort())

   mapper_bj1.SetInputConnection(reader_bj1.GetOutputPort())
   mapper_bj2.SetInputConnection(reader_bj2.GetOutputPort())

#create actor
actor_zl1 = vtk.vtkActor()
actor_zl2 = vtk.vtkActor()
actor_zl3 = vtk.vtkActor()
actor_zl4 = vtk.vtkActor()
actor_zl5 = vtk.vtkActor()
actor_zl6 = vtk.vtkActor()
actor_zl7 = vtk.vtkActor()
actor_zl8 = vtk.vtkActor()
actor_zl9 = vtk.vtkActor()
actor_zl10 = vtk.vtkActor()
actor_zl11 = vtk.vtkActor()

actor_zz1 = vtk.vtkActor()
actor_zz2 = vtk.vtkActor()
actor_zz3 = vtk.vtkActor()
actor_zz4 = vtk.vtkActor()
actor_zz5 = vtk.vtkActor()
actor_zz6 = vtk.vtkActor()
actor_zz7 = vtk.vtkActor()
actor_zz8 = vtk.vtkActor()
actor_zz9 = vtk.vtkActor()
actor_zz10 = vtk.vtkActor()
actor_zz11 = vtk.vtkActor()
actor_zz12 = vtk.vtkActor()

actor_lg1 = vtk.vtkActor()
actor_lg2 = vtk.vtkActor()

actor_bj1 = vtk.vtkActor()
actor_bj2 = vtk.vtkActor()

actor_zl1.SetMapper(mapper_zl1)
actor_zl2.SetMapper(mapper_zl2)
actor_zl3.SetMapper(mapper_zl3)
actor_zl4.SetMapper(mapper_zl4)
actor_zl5.SetMapper(mapper_zl5)
actor_zl6.SetMapper(mapper_zl6)
actor_zl7.SetMapper(mapper_zl7)
actor_zl8.SetMapper(mapper_zl8)
actor_zl9.SetMapper(mapper_zl9)
actor_zl10.SetMapper(mapper_zl10)
actor_zl11.SetMapper(mapper_zl11)

actor_zz1.SetMapper(mapper_zz1)
actor_zz2.SetMapper(mapper_zz2)
actor_zz3.SetMapper(mapper_zz3)
actor_zz4.SetMapper(mapper_zz4)
actor_zz5.SetMapper(mapper_zz5)
actor_zz6.SetMapper(mapper_zz6)
actor_zz7.SetMapper(mapper_zz7)
actor_zz8.SetMapper(mapper_zz8)
actor_zz9.SetMapper(mapper_zz9)
actor_zz10.SetMapper(mapper_zz10)
actor_zz11.SetMapper(mapper_zz11)
actor_zz12.SetMapper(mapper_zz12)

actor_lg1.SetMapper(mapper_lg1)
actor_lg2.SetMapper(mapper_lg2)

actor_bj1.SetMapper(mapper_bj1)
actor_bj2.SetMapper(mapper_bj2)

#set color
zl_odd_color_r = 0/255
zl_odd_color_g = 195/255
zl_odd_color_b = 0/255

zl_even_color_r = 0/255
zl_even_color_g = 255/255
zl_even_color_b = 0/255

actor_zl1.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
actor_zl3.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
actor_zl5.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
actor_zl7.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
actor_zl9.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)
actor_zl11.GetProperty().SetColor(zl_odd_color_r,zl_odd_color_g,zl_odd_color_b)

actor_zl2.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
actor_zl4.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
actor_zl6.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
actor_zl8.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)
actor_zl10.GetProperty().SetColor(zl_even_color_r,zl_even_color_g,zl_even_color_b)

actor_lg1.GetProperty().SetColor(255/255,0/255,0/255)
actor_lg2.GetProperty().SetColor(255/255,0/255,0/255)

actor_bj1.GetProperty().SetColor(150/255,70/255,50/255)
actor_bj2.GetProperty().SetColor(150/255,70/255,50/255)
 
# Create a rendering window and renderer
ren = vtk.vtkRenderer()
ren.SetBackground(255/255, 255/255, 255/255)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
# renWin.AddRenderer(ren1)
 
# Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
# Assign actor to the renderer
ren.AddActor(actor_zl1)
ren.AddActor(actor_zl2)
ren.AddActor(actor_zl3)
ren.AddActor(actor_zl4)
ren.AddActor(actor_zl5)
ren.AddActor(actor_zl6)
ren.AddActor(actor_zl7)
ren.AddActor(actor_zl8)
ren.AddActor(actor_zl9)
ren.AddActor(actor_zl10)
ren.AddActor(actor_zl11)

ren.AddActor(actor_zz1)
ren.AddActor(actor_zz2)
ren.AddActor(actor_zz3)
ren.AddActor(actor_zz4)
ren.AddActor(actor_zz5)
ren.AddActor(actor_zz6)
ren.AddActor(actor_zz7)
ren.AddActor(actor_zz8)
ren.AddActor(actor_zz9)
ren.AddActor(actor_zz10)
ren.AddActor(actor_zz11)
ren.AddActor(actor_zz12)

ren.AddActor(actor_lg1)
ren.AddActor(actor_lg2)

ren.AddActor(actor_bj1)
ren.AddActor(actor_bj2)

camera = vtk.vtkCamera()
camera.SetPosition(1,1,1)
camera.SetFocalPoint(0,0,0)

ren.SetActiveCamera(camera)
ren.ResetCamera()


style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
renWin.Render()
iren.Start()
