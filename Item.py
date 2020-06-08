class Item():
    '''
    Item contains relevant information about a product:
        Type - The type of item, which a user searches for (hammer, nails, etc.)
        Brand - The name of the product
        Price - The price of the product
        Link - A link to the product

    The class can easily be extended with more relevant information
    '''
    def __init__(self, typ, brand, price, stock, link):
        self.type = typ.lower()
        self.brand = brand
        self.price = price
        self.stock = stock
        self.link = link


    def print_summary(self):
        '''
        Prints a summary of the relevant information
        '''
        #print('Type:', self.type)
        print('Brand:', self.brand)
        print('Price:', self.price, 'kr')
        print('Stock:', self.stock)
        print('Link to item:', self.link)
