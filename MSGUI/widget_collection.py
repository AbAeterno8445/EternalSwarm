class WidgetCollection(object):
    def __init__(self):
        self.widgets_dict = {}

    def __getitem__(self, item):
        if item in self.widgets_dict:
            return self.widgets_dict[item]
        else:
            raise NameError("Widget " + item + " not found within WidgetCollection.")

    def set_visible(self, visible):
        for widg in self.widgets_dict:
            self.widgets_dict[widg].set_visible(visible)

    def add_widget(self, new_widget, widget_name):
        if widget_name not in self.widgets_dict:
            self.widgets_dict[widget_name] = new_widget
        else:
            raise Exception("Widget with name " + widget_name + " already exists within WidgetCollection.")

    def get_widgets_list(self):
        widg_list = []
        for widg in self.widgets_dict:
            widg_list.append(self.widgets_dict[widg])
        return widg_list