class FilterAndSortDecorator:
    def __init__(self, repo, filter_func=None, sort_func=None):
        self.repo = repo
        self.filter_func = filter_func
        self.sort_func = sort_func

    def get_k_n_short_list(self, k, n):
        data = self.repo.get_k_n_short_list(k, n)
        if self.filter_func:
            data = filter(self.filter_func, data)
        if self.sort_func:
            data = sorted(data, key=self.sort_func)
        return data

    def get_count(self):
        data = self.repo.read_all()
        if self.filter_func:
            data = filter(self.filter_func, data)
        return len(data)
