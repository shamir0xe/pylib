class TerminalProcess:
    def __init__(
        self,
        total_loops,
        prefix="",
        suffix="",
        decimals=1,
        length=100,
        fill="█",
        print_end="\r",
    ):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        self.total = total_loops
        self.iteration = 0
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.print_end = print_end

    def hit(self):
        """
        hit the progress iteration, and update it
        """
        self.iteration += 1
        percent = ("{0:." + str(self.decimals) + "f}").format(
            100 * (self.iteration / float(self.total))
        )
        filledLength = int(self.length * self.iteration // self.total)
        bar = self.fill * filledLength + "-" * (self.length - filledLength)
        print(f"\r{self.prefix} |{bar}| {percent}% {self.suffix}", end=self.print_end)
        # Print New Line on Complete
        if self.iteration == self.total:
            print()

    def clear(self):
        self.iteration = 0

