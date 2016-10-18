# coding=utf-8
from __future__ import absolute_import
from time import sleep

import octoprint.plugin
import RPi.GPIO as GPIO

try:
	from octoprint_automaticonoff import State
	from octoprint_automaticonoff.api import SwitchOnOffApiPlugin
	_disable = False
except ImportError:
	_disable = True
	class SwitchOnOffApiPlugin(object):
		pass


class RaspberryPiApiPlugin(SwitchOnOffApiPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.TemplatePlugin):
	def __init__(self):
		self._initialized = False

	@property
	def active_low(self):
		return self._settings.get_boolean(["active_low"])

	##~~ SettingsPlugin mixin
	def get_settings_defaults(self):
		return dict(
			gpio_number_plus = -1,
			gpio_number_minus = -1,
			delay = 0.0,
			active_low = False,
		)
		
	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=True),
		]
		
	def get_assets(self):
		return dict(
			js=[
				"js/raspberrypiapi_settings.js"
			],
			css=[
				"css/raspberrypiapi_matrix.css",
				"css/raspberrypiapi_buttons.css"
			]
		)

	##~~ Softwareupdate hook
	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			commandapi=dict(
				displayName="RaspberryPiApi Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Salandora",
				repo="OctoPrint-RaspberryPiApi",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Salandora/OctoPrint-RaspberryPiApi/archive/{target_version}.zip"
			)
		)
		
	##~~ SwitchOnOffApiPlugin mixin
	def setup_gpio(self):
		plus_pin = self._settings.get_int(["gpio_number_plus"])
		if plus_pin == -1:
			return
		
		minus_pin = self._settings.get_int(["gpio_number_minus"])
		
		try:
			GPIO.setwarnings(False)
			GPIO.setmode(GPIO.BOARD)
			
			GPIO.setup(plus_pin, GPIO.OUT)
			if minus_pin != -1:
				GPIO.setup(minus_pin, GPIO.OUT)
			
			self._initialized = True
		except:
			self._logger.exception("Failed to initialize the GPIO")
	
	def on_shutdown(self):
		'''Gets called if this is the active api and the servers is shuting down'''
		try:
			GPIO.cleanup()
			self._initialized = False
		except:
			self._logger.exception("Failed to cleanup the GPIO's")
			
	def set_power(self, power):
		'''Sets the power state either True(On) or False(Off)'''
		## If not already done initialize the necessary GPIOs
		if not self._initialized:
			self.setup_gpio()
			if not self._initialized:
				return

		try:
			plus_pin = self._settings.get_int(["gpio_number_plus"])
			if plus_pin == -1:
				return
			
			minus_pin = self._settings.get_int(["gpio_number_minus"])			
			delay = self._settings.get_float(["delay"])
			
			
			## Depending on the power and active_low variable we set the output 
			## to pull up or pull down. If relays get activated by an pull down
			## to ground (active_low) we need to set the pins to low if we want
			## them to be activated
			if power:
				if minus_pin != -1: 
					## Enable minus first then, plus
					GPIO.output(minus_pin, GPIO.LOW if self.active_low else GPIO.HIGH)
					if delay > 0:
						sleep(delay)
				GPIO.output(plus_pin, GPIO.LOW if self.active_low else GPIO.HIGH)
			else:
				## Turn off plus before minus
				GPIO.output(plus_pin, GPIO.HIGH if self.active_low else GPIO.LOW)
				if minus_pin != -1: 
					if delay > 0:
						sleep(delay)
					GPIO.output(minus_pin, GPIO.HIGH if self.active_low else GPIO.LOW)
		except:
			self._logger.exception("Failed to {}".format("power on" if power else "power off"))
			
	def get_power(self):
		'''Returns the actual state.
		Possible values are: State.ON, State.OFF and State.UNKNOWN'''
		## If not already done initialize the necessary GPIOs
		if not self._initialized:
			self.setup_gpio()
			if not self._initialized:
				return State.UNKNOWN
			
		plus_pin = self._settings.get_int(["gpio_number_plus"])
		if plus_pin == -1:
			return State.UNKNOWN
		
		minus_pin = self._settings.get_int(["gpio_number_minus"])
				
		try:
			## High signal means GPIO is activated and pulled up so set it to True
			state_plus = GPIO.input(plus_pin)
			
			## If minus_pin is -1 then set it as True for the next if case
			state_minus = GPIO.input(minus_pin) if minus_pin != -1 else True
			
			output = state_plus and state_minus
		except:
			self._logger.exception("Failed to read pin state")
		else:
			if output:
				return State.ON if not self.active_low else State.OFF
			else:
				return State.OFF if not self.active_low else State.ON

		return State.UNKNOWN


__plugin_name__ = "RaspberryPi API"

def __plugin_load__():
	if _disable:
		return
	
	global __plugin_implementation__
	__plugin_implementation__ = RaspberryPiApiPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

