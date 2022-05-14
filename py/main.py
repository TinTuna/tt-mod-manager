import tkinter as tk
import useHelperFunctions
import pageStructs.shipListPage as shipListPage

from pageStructs.mainPage import MainPage
from classes.Page import Page

root = tk.Tk()
root.resizable(False, False)
root.title('Ostranouts Ship Manager')
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root)
frame_main.grid(sticky='news')

# header
header = tk.Label(frame_main,
                  text="Ostranouts Ship Manager",
                  fg="white",
                  bg="black",
                  width=25,
                  height=2
                  )
header.grid(row=1, column=0, pady=(0, 10), sticky='ew')

navigation_buttons_frame = tk.Frame(frame_main)
navigation_buttons_frame.grid(row=2, column=0, pady=(0, 10), sticky='ew')

# pages

page_wrapper = tk.Frame(frame_main)
page_wrapper.grid(row=3, column=0, pady=(0, 10), sticky='ew')

main_page = MainPage(page_wrapper)
ship_derelict_page = shipListPage.ShipListPage(
    page_wrapper, useHelperFunctions.loadShipData('derelict'), 'derelict')
ship_police_page = shipListPage.ShipListPage(page_wrapper, useHelperFunctions.loadShipData('police'), 'police')
ship_scav_page = shipListPage.ShipListPage(page_wrapper, useHelperFunctions.loadShipData('scav'), 'scav')
ship_random_page = shipListPage.ShipListPage(page_wrapper, useHelperFunctions.loadShipData('random'), 'random')
ship_derelict_page.hide()
ship_police_page.hide()
ship_scav_page.hide()
ship_random_page.hide()

# navigation buttons

def togglePage(page):
    main_page.hide()
    ship_derelict_page.hide()
    ship_police_page.hide()
    ship_scav_page.hide()
    ship_random_page.hide()

    match page:
        case 'derelict':
            ship_derelict_page.show()
        case 'police':
            ship_police_page.show()
        case 'scav':
            ship_scav_page.show()
        case 'random':
            ship_random_page.show()
        case _:
            # ship_derelict_page.show()
            main_page.show()

main_page_btn = tk.Button(navigation_buttons_frame,
                        text="Main Page", command=lambda: togglePage('main'))
derelict_page_btn = tk.Button(
    navigation_buttons_frame, text="Derelict Ships", command=lambda: togglePage('derelict'))
police_page_btn = tk.Button(navigation_buttons_frame,
                          text="Police Ships", command=lambda: togglePage('police'))
scav_page_btn = tk.Button(
    navigation_buttons_frame, text="Scav Ships", command=lambda: togglePage('scav'))
random_page_btn = tk.Button(navigation_buttons_frame,
                          text="Random Ships", command=lambda: togglePage('random'))
main_page_btn.grid(row=0, column=0, sticky='ew')
derelict_page_btn.grid(row=0, column=1, sticky='ew')
police_page_btn.grid(row=0, column=2, sticky='ew')
scav_page_btn.grid(row=0, column=3, sticky='ew')
random_page_btn.grid(row=0, column=4, sticky='ew')

# execute
root.mainloop()
