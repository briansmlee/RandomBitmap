"""
01/11/2018
by Seungmin Brian Lee
using the HTTP API for random.org,
creates RGB bitmap.
"""

from PIL import Image
import requests

class RandomBitmapGenerator():
    def __init__(self):
        pass

    def create_random_bitmap(self, n):
        """creates random RGB bitmap of size n by n,
        using random numbers from random.org
        """
        img = Image.new('RGB', (n, n), 'black')
        pix = img.load()
        
        ints = self.get_many_random_ints(n * n * 3, 0, 255)
        print('n={}, number of random ints={}'.format(n, len(ints)))
        k = 0

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pix[i,j] = (ints[k], ints[k + 1], ints[k + 2])
                k += 3

        img.show()

    def get_random_ints(self, num=1, low=0, high=255):
        """gets num number of random integers,
        in range [low, high], inclusive,
        using random.org API
        """
        args = {'num': str(num),
                'min': str(low),
                'max': str(high),
                'col': '1',
                'base': '10',
                'format': 'plain',
                'rnd': 'new' 
                }

        r = requests.get('https://www.random.org/integers', params=args)
        # returns list of ints from requested byte-string
        strs = r.content.decode().strip('\n').split('\n') 
        return map(int, strs)

    def get_many_random_ints(self, num=1, low=0, high=255):
        """gets num number of random integers,
        optimized to reduce number of API calls
        """
        MAX = 10000 # random.org returns at most 10,000 integers per call
        ints = []

        while num > 0:
            count = num if num < MAX else MAX
            ints.extend(self.get_random_ints(count, low, high))
            num -= count
        
        return ints

gen = RandomBitmapGenerator()
gen.create_random_bitmap(128)
