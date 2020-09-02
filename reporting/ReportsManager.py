from reporting import NewsCount

class ReportManager:
    def __init__(self):
        # Main reports storage.
        self.reports = []
        newsCount = NewsCount()
        self.reports.append(newsCount)


