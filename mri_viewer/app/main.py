from .engine import MRIViewerApp

def main(server=None, **kwargs):
    app = MRIViewerApp(server)
    app.server.start(**kwargs)

if __name__ == "__main__":
    main()
