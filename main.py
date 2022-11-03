""" Flet Tutorial: Crypto Tracker Using Flet and Python Threading"""

# The imports we'll use in this video
import flet
from flet import (
    Page,
    UserControl,
    Container,
    border_radius,
    alignment,
    LinearGradient,
    Column,
    colors,
    Row,
    Text,
    icons,
    Card,
    IconButton,
    GridView,
    padding,
    animation,
)
from flet.transform import Scale

# This is the API we'll use to get crypto prices
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

# We'll also be using Python's thread class to run updates of crypto prices in the background
from threading import *
import time

# Before making the grid generator function, let's get the list of crypto we want hte prices of

# This is a python dictionary (nested dictionary) with the list of crypto we want to
# get th prices of.
# We stored the information as such so that when we pass them on to the grid generator, we can easiy access the info.
CryptoList = {
    "Bitcoin": {
        # token is the paramter that will be passed to API to get the prices.
        "Token": "bitcoin",
        "Title": "Bitcoin",
        "symbol": "BTC",
        "price": "",
        "image": f"bitcoin.png",
    },
    "Cardano": {
        "Token": "cardano",
        "Title": "Cardano",
        "symbol": "ADA",
        "price": "",
        "image": f"cardano.png",
    },
    "Ethereum": {
        "Token": "ethereum",
        "Title": "Ethereum",
        "symbol": "ETH",
        "price": "",
        "image": f"ethereum.png",
    },
    "Dogecoin": {
        "Token": "dogecoin",
        "Title": "Dogecoin",
        "symbol": "DOGE",
        "price": "",
        "image": f"dogecoin.png",
    },
    "Solana": {
        "Token": "solana",
        "Title": "Solana",
        "symbol": "SOL",
        "price": "",
        "image": f"solana.png",
    },
    "Avalanche": {
        "Token": "avalanche-2",
        "Title": "Avalanche",
        "symbol": "AVAX",
        "price": "",
        "image": f"avalanche.png",
    },
}

# From the dictionary, you can see that the price key is empty..
# We'll be getting prices and passing them on into the dictionary.
# The overall flow would be get prices in the backgournd => pass them into the dictioanry => update the dashboard

# We will create a seperate function becuase we should have the update running on another thread
# This helps prevent lags and freezes
class CryptoUpdate:
    def KeepTrackOfTime(self):
        # This'll make the thread runn forever
        while True:
            # recall that the price key in the ditionry is empty
            # also recall that we have the ticker name to pass it to the API
            for crypto in CryptoList.keys():
                self.PriceNow = cg.get_price(
                    # the cg.get_price takes two parameters
                    ids=CryptoList[crypto]["Token"],
                    # You can change the currency to whatever suits you
                    vs_currencies="usd",
                )
                # now some formatting
                self.PriceNow = round(
                    self.PriceNow[CryptoList[crypto]["Token"]]["usd"], 2
                )

                # Once we get the price, pass it into the dictionary
                CryptoList[crypto]["price"] = self.PriceNow

            # Now this API is limited to a few requests per minute, so 30 seconds is a good number to wait before updated the price again.

            # set time sleep to wait before updting the price
            time.sleep(30)


# Let's create the class App()
class App(UserControl):

    # animation function
    def scaleUp(self, x):
        if x.control.scale != 1.125:
            x.control.scale = 1.125
        else:
            x.control.scale = 1

        x.control.update()

    # we need a function to keep track of the updates
    def TickUpdates(self):
        # we need to loop through the contorls, clear them and update them with new prices
        for text in self.Cryptocolumn.controls[:]:  # the [:] means all the controls
            self.Cryptocolumn.controls.remove(text)

        # update the clear action
        self.update()
        # re generate the cards anew
        self.GridGenerator()

    # We now need a function that'll create the gridview
    def GridGenerator(self):
        # This function will start once we click the PLUS icon on the app.

        #
        # So first, we want to loop through the dictioanry keys
        for crypto in CryptoList.keys():
            # now inside the for-loop, let's create some variables to pass on
            self.symbol = Text(
                # for the label of the text, it's simply the symbol key of each crypto
                # so as an example: first key is bitcoin which is set as crypto for the variable
                # crypto = bitcoin and e want the value of the 'symbol'.
                # therefore [bitcoin]['symbol] will get BTC
                CryptoList[crypto]["symbol"],
                size=10,
                weight="w700",
                color="#64748b",
            )
            self.price = Text(
                CryptoList[crypto]["price"],
                size=13,
                weight="w700",
            )

            self.currency = Text(
                "USD",
                size=9,
                weight="w700",
                color="#64748b",
            )

            # Let's start adding the info into the grid
            self.CryptoContainer = Card(
                elevation=12,
                content=Container(
                    #
                    # For animation, I've included these attributes for extra UI UX
                    on_hover=lambda x: self.scaleUp(x),
                    scale=Scale(scale=1),
                    animate_scale=animation.Animation(800, "bounceOut"),
                    #
                    border_radius=border_radius.all(18),
                    padding=padding.all(10),
                    width=100,
                    height=110,
                    gradient=LinearGradient(
                        begin=alignment.bottom_left,
                        end=alignment.top_right,
                        colors=["#3f3f46", "#303030"],
                    ),
                    content=Column(
                        horizontal_alignment="center",
                        spacing=0,
                        alignment="center",
                        # Here we pass on the info, mainly he crypto price and other attributes
                        #
                        # Wrap these contianers in a control
                        controls=[
                            Container(
                                alignment=alignment.bottom_center,
                                width=64,
                                content=self.symbol,
                            ),
                            Container(
                                alignment=alignment.top_center,
                                width=120,
                                content=self.price,
                            ),
                            Container(
                                alignment=alignment.top_center,
                                width=120,
                                content=self.currency,
                            ),
                        ],
                    ),
                ),
            )

            # we need to append these to the gridview we created below
            self.Cryptocolumn.controls.append(self.CryptoContainer)
            self.Cryptocolumn.update()

        # Final attribute, let's disable the plus icon so we dont generate extra grids
        if self.DisableIcon.disabled == False:
            self.DisableIcon.disabled = True
        self.update()

        # Now every 30 econds the price updates the dictioanry, but you'll have to pres the refresh button to get them onto the screen

    #
    #
    # Now for the main container
    def MainContainer(self):

        # We'll be using the gridveiw widget as seen by the intro demo.
        #
        self.Cryptocolumn = GridView(
            # exapnds the widgets to fill up the allowed size
            expand=1,
            #
            # The size of each grid
            max_extent=150,
        )

        # One of the icons will need to be disabled when clicked, so we need to set it as a variable to call on later
        self.DisableIcon = IconButton(
            icon=icons.ADD,
            icon_size=16,
            # starts with False, once clicked, it becomes disabled
            disabled=False,
            #
            # we'll create a function for this later on
            on_click=lambda e: self.GridGenerator(),
        )

        # Now for the main container
        self.main_container = Card(
            # I'm using card to get that shadow effect using elevation
            elevation=20,
            content=Container(
                width=350,
                height=620,
                border_radius=border_radius.all(20),
                # some padding
                padding=padding.all(20),
                gradient=LinearGradient(
                    begin=alignment.bottom_left,
                    end=alignment.top_right,
                    colors=["#222121", "#303030"],
                ),
                content=Column(
                    # We'll have a row of titles in this top part
                    controls=[
                        Row(
                            alignment="spaceBetween",
                            controls=[
                                # Title text
                                Text(
                                    "Dashboard",
                                    size=18,
                                ),
                                # We'll place the icons in a container
                                Container(
                                    content=Row(
                                        # Let's align the icons to the far right
                                        alignment="end",
                                        # Remove the spacing between the icons
                                        spacing=0,
                                        controls=[
                                            self.DisableIcon,
                                            IconButton(
                                                icon=icons.UPDATE_ROUNDED,
                                                icon_size=16,
                                                # we'll create this function later also
                                                #
                                                # let's call the generator now
                                                # pass the track function to the update icon
                                                on_click=lambda e: self.TickUpdates(),
                                            ),
                                        ],
                                    )
                                ),
                            ],
                            # Pass the Grid variable here
                        ),
                        #
                        # Add some padding
                        Container(padding=padding.only(top=10)),
                        #
                        self.Cryptocolumn,
                    ],
                ),
            ),
        )

        # return the actual object/widget, not the function!!
        return self.main_container

    #
    # now make the build function to return the controls to the page
    def build(self):
        return Container(
            alignment=alignment.center_right,
            padding=padding.only(right=150),
            width=1500,
            height=1000,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=[colors.PURPLE_700, colors.PURPLE_900],
            ),
            content=Column(
                alignment="center",
                controls=[
                    # we'll pass in the main container here in a bit
                    self.MainContainer()  # pass in the function so we can see the changes
                ],
            ),
        )


# note: to run the app with hot reload: flet -r filename.py

# let's create the main function for the build process
#
def main(page: Page):
    page.title = "Flet: Crypto Dashboard UI/UX"
    page.window_width = 1400
    page.window_height = 1000
    # page.bgcolor = colors.DEEP_PURPLE_600

    # I want to center the main continer  to the center of the Page
    page.vertical_alignment = "center"
    # page.horizontal_alignment = "center"

    # our main class will be called App()
    # let's call it here and create it above
    app = App()
    page.update()

    # Pass the object to display it on the page
    page.add(app)


if __name__ == "__main__":
    # Let's create a thread (specifcally a daemon thread) to run the API
    # we create a thread called timeCount, we set th target, meaining what we want to run to the new class we just created.
    # We set daemon to true to run forever and then start() to begin the thread on launch.
    timeCount = Thread(target=CryptoUpdate().KeepTrackOfTime, daemon=True).start()
    #
    flet.app(target=main)
