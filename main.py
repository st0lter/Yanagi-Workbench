from app.ui.main_window import App
from app.config import APP_NAME, MIN_SIZE

if __name__ == '__main__':
    app = App()
    app.title(APP_NAME)
    app.minsize(*MIN_SIZE)
    app.mainloop()
