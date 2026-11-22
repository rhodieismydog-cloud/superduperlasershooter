import arcade

WIDTH = 800
HEIGHT = 600
TITLE = "Star Defender"

MENU_OPTIONS = ["Play", "How to Play", "Quit"]

class Ship(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png", scale=0.5)
        self.fuel = 100

    def update(self,delta_time: float = 1/60):
        #todo: move,burn fuel

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_MIDNIGHT_BLUE
        self.selected = 0                       # index into MENU_OPTIONS
        self.title_text = arcade.Text("STAR DEFENDER", WIDTH / 2, 430,
                                      arcade.color.GOLD, 54, anchor_x="center",
                                      bold=True)
        self.best_text = arcade.Text("", WIDTH / 2, 80, arcade.color.LIGHT_GRAY, 18,
                                     anchor_x="center")
        # One Text per option, built once
        self.option_texts = []
        for i, option in enumerate(MENU_OPTIONS):
            y = 300 - i * 60
            self.option_texts.append(arcade.Text(option, WIDTH / 2, y,
                                                 arcade.color.WHITE, 28,
                                                 anchor_x="center"))

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        for i, text in enumerate(self.option_texts):
            if i == self.selected:
                text.text = f"> {MENU_OPTIONS[i]} <"    # marker, not just color
                text.color = arcade.color.GOLD
            else:
                text.text = MENU_OPTIONS[i]
                text.color = arcade.color.WHITE
            text.draw()
        self.best_text.text = f"Best: {self.window.best_score}"
        self.best_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.DOWN:
            self.selected = (self.selected + 1) % len(MENU_OPTIONS)   # wrap around
        elif key == arcade.key.UP:
            self.selected = (self.selected - 1) % len(MENU_OPTIONS)
        elif key == arcade.key.ENTER:
            self.choose()

    def choose(self):
        choice = MENU_OPTIONS[self.selected]
        if choice == "Play":
            self.window.show_view(GameView())
        elif choice == "How to Play":
            self.window.show_view(HowToPlayView(self))   # remember the menu
        elif choice == "Quit":
            self.window.close()


class HowToPlayView(arcade.View):
    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view              # where ESC goes back to
        self.background_color = arcade.color.DARK_SLATE_GRAY
        self.lines = arcade.Text(
            "HOW TO PLAY\n\nLEFT / RIGHT   move\nSPACE   shoot\nP   pause\n\n"
            "Shoot the falling ships. Three hits and you're out.\n\nESC to go back",
            WIDTH / 2, 480, arcade.color.WHITE, 22, anchor_x="center",
            multiline=True, width=600, align="center")

    def on_draw(self):
        self.clear()
        self.lines.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu_view)   # same menu, same selection


class GameView(arcade.View):
    """Stand-in for your Mini Shooter's game view."""
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.MIDNIGHT_BLUE
        self.score = 0
        self.score_text = arcade.Text("Score: 0", 20, HEIGHT - 40, arcade.color.WHITE, 20)
        self.hint = arcade.Text("SPACE = +10    X = game over", WIDTH / 2, HEIGHT / 2,
                                arcade.color.LIGHT_GRAY, 20, anchor_x="center")

    def on_draw(self):
        self.clear()
        self.hint.draw()
        self.score_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.score += 10
            self.score_text.text = f"Score: {self.score}"
        elif key == arcade.key.X:
            self.window.show_view(GameOverView(self.score))


class GameOverView(arcade.View):
    def __init__(self, score):
        super().__init__()
        self.background_color = arcade.color.BLACK_BEAN
        self.new_best = score > self.window.best_score
        self.window.best_score = max(self.window.best_score, score)
        headline = "NEW BEST!" if self.new_best else "GAME OVER"
        self.headline = arcade.Text(headline, WIDTH / 2, 380, arcade.color.GOLD, 48,
                                    anchor_x="center", bold=True)
        self.details = arcade.Text(f"Score: {score}     Best: {self.window.best_score}",
                                   WIDTH / 2, 300, arcade.color.WHITE, 24, anchor_x="center")
        self.keys = arcade.Text("R  play again        M  main menu", WIDTH / 2, 200,
                                arcade.color.LIGHT_GRAY, 20, anchor_x="center")

    def on_draw(self):
        self.clear()
        self.headline.draw()
        self.details.draw()
        self.keys.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.window.show_view(GameView())        # restart = a NEW game
        elif key == arcade.key.M:
            self.window.show_view(MenuView())


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    window.best_score = 0          # lives on the window, so every view can see it
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()