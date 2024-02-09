# Written by Sean Hart zlite4 copyrite 2024

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage  # Import AsyncImage widget

import subprocess

# Function to generate a random MAC address
def generate_mac_address():
    mac_address = ':'.join(['{:02x}'.format((x * 2) ^ 0x42) for x in range(6)])
    return mac_address

# Function to change the MAC address using root permissions
def change_mac_address():
    new_mac_address = generate_mac_address()
    # Execute the command to change the MAC address using root permissions
    try:
        subprocess.run(['su', '-c', f'ifconfig wlan0 hw ether {new_mac_address}'], check=True)
        return True, new_mac_address
    except subprocess.CalledProcessError:
        return False, ''

# Kivy App Class
class MacAddressApp(App):

    def build(self):
        # Create the main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Create an area to display the icon image
        icon_image = AsyncImage(source='app_icon.png')  # Change 'icon.png' to the path of your icon image

        # Create a label to display the generated MAC address
        self.mac_label = Label(text='Generated MAC Address will appear here')

        # Create a button to generate the MAC address
        self.generate_button = Button(text='Generate MAC Address', size_hint=(None, None), size=(200, 50))
        self.generate_button.bind(on_press=self.generate_mac_address)

        # Create a button to change the MAC address
        self.change_mac_button = Button(text='Change MAC Address', size_hint=(None, None), size=(200, 50))
        self.change_mac_button.bind(on_press=self.change_mac_address)

        # Add widgets to the layout
        layout.add_widget(icon_image)
        layout.add_widget(self.mac_label)
        layout.add_widget(self.generate_button)
        layout.add_widget(self.change_mac_button)

        return layout

    # Function to generate the MAC address and display it in the label
    def generate_mac_address(self, instance):
        # Generate a random MAC address
        mac_address = generate_mac_address()
        # Display the generated MAC address in the label
        self.mac_label.text = f'Generated MAC Address: {mac_address}'

    # Function to change the MAC address and display the result in the label
    def change_mac_address(self, instance):
        success, new_mac_address = change_mac_address()
        if success:
            self.mac_label.text = f'MAC Address Changed to: {new_mac_address}'
        else:
            self.mac_label.text = 'Failed to change MAC Address (requires root permission)'

# Run the app
if __name__ == '__main__':
    MacAddressApp().run()

