class WidgetCollection(object):
    def __init__(self):
        self.widgets_dict = {}
        self.inv_widgets = []

    def __getitem__(self, item):
        if item in self.widgets_dict:
            return self.widgets_dict[item][0]
        else:
            raise NameError("Widget " + item + " not found within WidgetCollection.")

    def add_widget(self, new_widget, widget_name, layer=0):
        if widget_name not in self.widgets_dict:
            self.widgets_dict[widget_name] = (new_widget, layer)
        else:
            raise Exception("Widget with name " + widget_name + " already exists within WidgetCollection.")

    def set_widget_visible(self, widget, visible):
        if not visible:
            if widget not in self.inv_widgets:
                self.inv_widgets.append(widget)
            self[widget].set_visible(False)
        else:
            if widget in self.inv_widgets:
                self.inv_widgets.remove(widget)
            self[widget].set_visible(True)

    def set_visible(self, visible):
        for widg in self.widgets_dict:
            if not visible or visible and widg not in self.inv_widgets:
                self[widg].set_visible(visible)

    def get_widgets_list(self):
        widg_list = []
        for widg in self.widgets_dict:
            widg_list.append(self.widgets_dict[widg])
        return widg_list