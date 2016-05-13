# -*- coding: utf-8 -*-
__Author__ = 'fangshi.lb'
__Date__ = '12-9-23'




class SimpleQuery():
    """
    simple query object
    """
    page_no = 0
    page_size = 12
    start_row = 0
    end_row = 0


    def __init__(self, page_no=0, page_size=12):
        self.page_no = page_no
        self.page_size = page_size

        if page_no == 0 or page_size == 0:
            self.start_row = 0
            self.end_row = page_size
        else:
            self.start_row = (self.page_no-1) * self.page_size
            self.end_row = self.start_row + self.page_size

    def to_cache_key(self):
        return str(self.start_row) + '_' + str(self.end_row)

    def __str__(self):
        return str(self.start_row) + '_' + str(self.end_row)

