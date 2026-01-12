

class Egg:
    def __init__(self, group: int, position: tuple[int, int]):
        self.group = group
        self.position = position


    def get_group(self):
        return self.group
    
    def __repr__(self):
        return "⚪" if self.group == 1 else "⚫"

def main():
    ...


if __name__ == "__main__":
    main()