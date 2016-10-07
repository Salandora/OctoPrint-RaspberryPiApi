$(function() {
    function RaspberryPiApiSettingsViewModel(parameters) {
        var self = this;
        
        self.settings = parameters[0];
        self.show_bcm = ko.observable(false);
        
        self.gpio_to_change = undefined;
        
        self.isSelected = function(e) {
            if (e === undefined)
                return;
                
            var child = $(e);            
            var pin_number = child.index() + 1;
            
            return self.settings.settings.plugins.raspberrypiapi.gpio_number_plus() == pin_number ||
                   self.settings.settings.plugins.raspberrypiapi.gpio_number_minus() == pin_number;
        };
        self.selectPin = function(sender, e) {
            if (e.target === undefined || self.gpio_to_change === undefined)
                return;
                
            var child = $(e.target);            
            var pin_number = child.index() + 1;
            
            self.gpio_to_change(pin_number);
        };
        self.onStartup = function() {
            $(".btn-matrix > .3v3, .btn-matrix > .5v, .btn-matrix > .gnd").prop("disabled", true);
            
            $("input[type=text]").focus(function() {
                if ($(this).attr('id') == "gpio_number_plus")
                {
                    self.gpio_to_change = self.settings.settings.plugins.raspberrypiapi.gpio_number_plus;
                }
                else if ($(this).attr('id') == "gpio_number_minus")
                {
                    self.gpio_to_change = self.settings.settings.plugins.raspberrypiapi.gpio_number_minus;
                }
            });
        };
        
        self.onSettingsShown = function() {
            self.gpio_to_change = self.settings.settings.plugins.raspberrypiapi.gpio_number_plus;
        };
    }

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([
        RaspberryPiApiSettingsViewModel,
        ["settingsViewModel"],
        ["#settings_plugin_raspberrypiapi"]
    ]);
});
