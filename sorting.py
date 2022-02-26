import pygame
import random
import math

pygame.init()

class Informations:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (240, 129, 225)
    GREEN = (0, 255, 0)
    X_PADDING = 100
    Y_PADDING_BOTTOM = 100
    FONT = pygame.font.SysFont('dejavusans', 20)
    LARGE_FONT = pygame.font.SysFont('dejavusans', 30)
    BACKGROUND_COLOR = (2, 4, 69)
    GREYS = (
        (45, 62, 214),
        (80, 85, 242),
        (109, 113, 247),
    )
    
    def __init__(self, starting_list, width=900, height=600):
        self.width = width
        self.height = height
        self.set_starting_list(starting_list)
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithms Visualization")
        
    def set_starting_list(self, starting_list):
        self.starting_list = starting_list
        self.min = min(starting_list)
        self.max = max(starting_list)
        self.bar_width = math.floor((self.width - self.X_PADDING) / len(starting_list))
        self.bar_height = math.floor((self.height - self.Y_PADDING_BOTTOM) / self.max)
        
        self.x_start = self.X_PADDING / 2

def draw_list(infos, color_position={}, clear_bg=False):
    _list =infos.starting_list
    x_start = (infos.width - (infos.bar_width * len(_list))) / 2
    if clear_bg:
        clear_rect = (infos.X_PADDING / 2, 0, infos.width, 450)
        pygame.draw.rect(infos.window, infos.BACKGROUND_COLOR, clear_rect)
        
    for i, val in enumerate(_list):
        x = x_start + i * infos.bar_width
        y = (val * 450) / infos.max
        
        color = infos.GREYS[i % 3]
        if i in color_position:
            color = color_position[i]
            
        pygame.draw.rect(infos.window, color, (x, 0, infos.bar_width, y))
        
    if clear_bg:
        pygame.display.update()
              

def draw(infos, sorting_algorithm_name, ascending):
    infos.window.fill(infos.BACKGROUND_COLOR)
    algorithm_info = infos.LARGE_FONT.render(f"{sorting_algorithm_name} {'Ascending' if ascending else 'Descending'}", 1, infos.WHITE)
    infos.window.blit(algorithm_info, (infos.width / 2 - algorithm_info.get_width() / 2, infos.height - 100 ))
    
    texts = infos.FONT.render("R- Reset | SPACE- Start Sorting | A- Ascending | D- Descending", 1, infos.WHITE)
    infos.window.blit(texts, (infos.width / 2 - texts.get_width() / 2, infos.height - 60 ))
    
    sortings = infos.FONT.render("B- Bubble Sort | I- Insertion Sort", 1, infos.WHITE)
    infos.window.blit(sortings, (infos.width / 2 - sortings.get_width() / 2, infos.height - 30 ))
    draw_list(infos)
    pygame.display.update() 


def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]


def bubble_sort(infos, ascending=True):
    _list = infos.starting_list
    for i in range(len(_list) - 1):
        for j in range(len(_list) - 1 - i):
            num1, num2 = _list[j], _list[ j + 1 ]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                _list[j], _list[ j + 1 ] = _list[ j + 1 ], _list[j]
                color_position = {j: infos.GREEN, j+1:infos.RED}
                draw_list(infos, color_position=color_position, clear_bg=True )
                yield True
                
    return _list

def insertion_sort(infos, ascending=True):
    _list = infos.starting_list
    for i in range(len(_list)):
        current = _list[i]
        while True:
            # get the two conditions
            ascending_sort = i > 0 and _list[i -1 ] > current and ascending
            descending_sort = i > 0 and _list[i -1 ] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            
            _list[i] = _list[i - 1]
            i = i - 1
            _list[i] = current
            color_position = {i: infos.GREEN, i-1:infos.RED}
            draw_list(infos, color_position=color_position, clear_bg=True )
            yield True
            
    return _list
    
def main():
    run, sorting, ascending = True, False, True
    n, _min, _max =150, 10, 200
    _list = generate_starting_list(n, _min, _max)
    infos = Informations(_list)
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm = bubble_sort
    sorting_algorithm_generator = None
    while run:
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:           
            draw(infos, sorting_algorithm_name, ascending)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                sorting = False
                new_list = generate_starting_list(n, _min, _max)
                infos.set_starting_list(new_list)
                
            elif event.key == pygame.K_d and not sorting:
                ascending = False
                draw(infos, sorting_algorithm_name, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
                draw(infos, sorting_algorithm_name, ascending)

            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(infos, ascending)
                
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm, sorting_algorithm_name = insertion_sort, "Insertion Sort"
                draw(infos, sorting_algorithm_name, ascending)

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm, sorting_algorithm_name = bubble_sort, "Bubble Sort"
                draw(infos, sorting_algorithm_name, ascending)
                
    pygame.quit()
    
    
if __name__ == '__main__':
    main()