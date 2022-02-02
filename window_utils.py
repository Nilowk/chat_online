class WindowUtils:

    def clear_window(self):
        for element in self.elements:
            element.destroy()

    def erase(self, e, placeholder):
        if e.get() == placeholder:
            e.config(fg="black")
            e.delete(0, "end")

    def add(self, e, placeholder):
        if e.get() == "":
            e.config(fg="grey")
            e.insert(0, placeholder)

    def is_default_message(self, entry):
        if entry["fg"] != "grey":
            return entry.get()
        else:
            return ""