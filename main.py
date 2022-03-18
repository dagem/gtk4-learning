import gi
import os
import sys
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio


class SettingsWindow(Gtk.ApplicationWindow):
    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.add(Gtk.Label("Settings"))
        self.show_all()


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

        self.header = Gtk.HeaderBar()                            # creates a new header bar
        self.set_titlebar(self.header)                           # sets the titlebar to be the newly created header
        self.eject_button = Gtk.Button(label="Eject")            # creates a new button named eject_button
        self.eject_button.set_icon_name("media-eject-symbolic")  # sets the icon of eject_button to be one of an eject_button
        self.header.pack_start(self.eject_button)                # puts eject_button at the start of the header bar
        self.eject_button.connect('clicked', self.eject_call)    # connects eject_button to the eject_call method

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_clicked)
        self.add_action(about_action)

        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.open_window)
        self.add_action(settings_action)

        self.toggle_theme = Gtk.Switch()

        self.toggle_theme.set_active(False)
        self.toggle_theme.connect("state-set", self.theme_toggle)

        menu = Gio.Menu.new()                    # creates a new menu
        menu.append("Settings", "win.settings")  # adds the "Settings" option to the menu
        menu.append("About", "win.about")        # adds the "About" option to the menu

        self.popover = Gtk.PopoverMenu()   # creates a popover menu
        self.popover.set_menu_model(menu)  # sets the model of the menu to be our previously created menu

        hamburger = Gtk.MenuButton()                   # creates a new hamburger menu
        hamburger.set_popover(self.popover)            # sets that hamburger menu's popover menu to be our menu object
        hamburger.set_icon_name("open-menu-symbolic")  # sets the icon of the hamburger menu to be "open-menu-symbolic"
        self.header.pack_end(hamburger)                # sets the hamburger menu to be at the end of the header, you can use pack_start for beginning

        self.about = Gtk.AboutDialog.new()         # creates a new about dialog

        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # creates a new box
        self.switch_box.append(self.toggle_theme)
        self.header.pack_end(self.switch_box)

        self.app = self.get_application()

    def open_window(self, win, param):
        settings_window = SettingsWindow()

    def on_about_clicked(self, action, param):
        self.about.set_authors(["Dagem Mesfin"])                # creates a new field on the credits' page with the author's name
        self.about.set_website("https://github.com/dagem")      # sets the website to be my GitHub
        self.about.set_license_type(Gtk.License(3))
        self.about.set_logo_icon_name(None)                     # sets the icon in the about menu
        self.about.show()                                       # tells the window to show itself
        self.popover.hide()                                     # sets the window to be hidden, rather than destroyed, upon pressing the exit button

    @staticmethod
    def eject_call(button):
        os.system("eject cdrom")  # calls system and tells it to run the 'eject' command with the parameter 'cdrom'
        print("eject was called")

    def theme_toggle(self, switch, state):
        manager = self.app.get_style_manager()

        if state:
            manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)
        else:
            manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
