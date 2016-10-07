# OctoPrint-RaspberryPiApiPlugin

Raspberry PI Api for Automatic On/Off Plugin for OctoPrint
This enables you to specify 2 GPIO pins which switch a relay to turn on/off your printer

It depends on the RPi.GPIO library and the Automatic On/Off Plugin

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/Salandora/OctoPrint-RaspberryPiApiPlugin/archive/master.zip

## Configuration

Settings -> RaspberryPiApi

Select the first GPIO for +/Phase

If you have a second relay for -/Neutral:
 - Click on the second textbox 
 - Select the second GPIO pin
 - If desired set a delay for between turning on and off the relays
   On: -/Neutral turns on, delay, +/Phase turns on
   Off: +/Phase turns off, delay, -/Neutral turns off
