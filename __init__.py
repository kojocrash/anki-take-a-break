# Simple Anki addon that allows you to postpone a deck
# for a certain amount of days
# Please don't modify if you don't know what you are doing
#
# P.S. I don't have much experience in Python
#      if you don't want to use this addon then don't,
#      there are other similiar addons


from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from anki import decks, cards
from anki.consts import QUEUE_TYPE_REV

# I dont know if simply FONT_SIZE would mess with something so...
# You can adjust this if you want
FONT_SIZE_TAB_ADDON = 12

#!!! I dont advise changing anything bellow this comment
#!!! it could impact the addons functionality or in worst case scenario your decks

## Functions

def show_addon_window() -> None:
    window = window_init()
    mw.takeBrakeWidget = window
    window.show()

def postpone():
    window = mw.takeBrakeWidget

    # Find data boxes in the GUI
    drop_down = window.findChild(QComboBox)
    spin_box = window.findChild(QSpinBox)

    # If boxes found
    if drop_down and spin_box:
        deck = drop_down.currentText()
        days = spin_box.value()

        # Filter cards that are in the deck and are due to review
        card_ids = mw.col.find_cards('"deck:%s" "is:due"' % deck)

        for id in card_ids:
            # Find the coresponding card
            card = mw.col.getCard(id)

            # If it is in review que postpone it by x days
            if card.queue == QUEUE_TYPE_REV:
                card.due += days
                card.flush()

        # Refresh the main window and close the addon
        mw.reset()
        window.close()
    else:
        showInfo("Something went wrong, couldn't find the boxes in addons GUI")

# Internal util for setting font size
def setFontSize(obj):
    font = obj.font()
    font.setPointSize(FONT_SIZE_TAB_ADDON)
    obj.setFont(font)

## Addon Window Setup

def  window_init():
    window = QWidget()
    window.setWindowTitle("Take a Break addon")
    
    layout = QVBoxLayout()
    
    # Confirmation button
    confirm_btn = QPushButton('Postpone')
    setFontSize(confirm_btn)

    # Dropdown menu with decks
    drop_down = QComboBox()
    setFontSize(drop_down)

    # Box for setting the noumer of days to postpone
    days_num = QSpinBox()
    days_num.setRange(1, 9999)
    days_num.setSuffix(" days")
    setFontSize(days_num)

    # A small text explanation
    label = QLabel("Please select the deck to postpone")
    setFontSize(label)

    # Label on top
    layout.addWidget(label)

    # Decks in the dropdown menu
    for deck in mw.col.decks.all_names_and_ids():
        drop_down.addItem(deck.name)

    # Add the dropdown menu to the layout
    layout.addWidget(drop_down)

    # Add the spinbox to the layout
    layout.addWidget(days_num)

    # Add the button at the bottom of the layout
    layout.addWidget(confirm_btn)

    # Link button to afuction
    confirm_btn.clicked.connect(postpone)

    window.setLayout(layout)
    return window


## Main Window Setup

# Add an item to the tools bar in main window
action = QAction("Take a Break", mw)
action.triggered.connect(show_addon_window)

mw.form.menuTools.addAction(action)