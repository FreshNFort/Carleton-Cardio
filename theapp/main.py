import flet as ft


def  main(page: ft.Page):

   Hola = ft.Text("Hola Senor!", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE)
   Burger = ft.IconButton(ft.Icons.MENU, 
                      icon_color=ft.Colors.BLUE,
                      icon_size=40, 
                      align=ft.Alignment.TOP_RIGHT, 
                      highlight_color=ft.Colors.LIGHT_BLUE_50,
                      )

   #def button_clicked()

   page.add(Burger, Hola)


   
   

ft.run(main)