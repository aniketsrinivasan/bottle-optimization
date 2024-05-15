DEBUGGING = True


class BottleMonth:
    # Note: import this value from a "manufacturing" module later.
    __MINIMUM_PRODUCTION_DAYS = 10      # minimum number of consecutive production days
    if __MINIMUM_PRODUCTION_DAYS > 28:
        raise ValueError(f"__MINIMUM_PRODUCTION_DAYS cannot exceed 28. "
                         f"Attempted {__MINIMUM_PRODUCTION_DAYS} days.")
    elif __MINIMUM_PRODUCTION_DAYS <= 0:
        raise ValueError(f"__MINIMUM_PRODUCTION_DAYS must be positive. "
                         f"Attempted {__MINIMUM_PRODUCTION_DAYS} days.")

    __MINIMUM_BUFFER_DAYS = 20          # minimum number of excess stock to hold
    __DAYS_IN_MONTH = 30
    __PRODUCTION_BATCH_SIZE = 1000      # cost per batch of "n" bottles is given, where
    #                                       n is __PRODUCTION_BATCH_SIZE

    # Initializing the instance of object "bottle":
    def __init__(self, bottle_type, current_stock, production_capacity,
                 production_cost, purchase_cost):
        # Setting all the object's instance values:
        self.bottle_type = bottle_type                      # type of bottle
        self.initial_stock = current_stock                  # bottles in inventory (start of month)
        self.ending_stock = current_stock                   # bottles in inventory (end of month)
        self.production_capacity = production_capacity      # production capacity of bottles per day

        # Production cost per bottle:
        self.production_cost = production_cost / self.__PRODUCTION_BATCH_SIZE
        # Purchase cost per bottle:
        self.purchase_cost = purchase_cost

        # Initializing a "total cost" so we can keep track of total expenses for this bottle type:
        self.total_cost = 0
        # Creating a "required ending stock" so we know the minimum value of "ending_stock":
        self.required_ending_stock = None
        # Creating a "required month creation" so we know the minimum number of bottles to be
        #   purchased/produced this month:
        self.required_creation = None
        # Keeping track of how many bottles are consumed this month:
        self.consumption = None

        # Tracking how many bottles are produced/purchased:
        self.produced = 0
        self.total_production_days = 0
        self.purchased = 0
        # Creating a "current month creation" to keep track of the number of bottles created:
        self.current_creation = 0

        if DEBUGGING:
            print(f"Initialized bottle with type `{self.bottle_type}`.")

    # bottle_set_requirements(this_month_consumption, next_month_consumption) sets the bottle's targets
    #   for this month. In particular, it updates the required ending stock, and required creation for
    #   this month.
    def bottle_set_requirements(self, this_month_consumption, next_month_consumption):
        # The required_ending_stock is (at minimum) __MINIMUM_BUFFER_DAYS worth of next month's
        #   predicted bottle consumption next_month_consumption.
        self.required_ending_stock = int(next_month_consumption *
                                         (self.__MINIMUM_BUFFER_DAYS / self.__DAYS_IN_MONTH))
        # This month's creation requirement is the minimum number of bottles that must be created
        #   this month in order to end with required_ending_stock, depending on this_month_consumption.
        self.required_creation = int(self.required_ending_stock
                                     + this_month_consumption
                                     - self.initial_stock)

        # Setting this month's bottle consumption:
        self.consumption = this_month_consumption
        # Subtracting the consumption from the ending stock:
        self.ending_stock -= this_month_consumption

        if DEBUGGING:
            print(f"Setting requirements...")
            print(f"Required ending stock: {self.required_ending_stock}.")
            print(f"Ending stock:          {self.ending_stock}.")
            print(f"Required creation:     {self.required_creation}.")

    # bottle_update_current_creation(this_creation) updates the number of bottles "created" this month.
    def bottle_update_current_creation(self, this_creation):
        self.current_creation = self.produced + self.purchased
        self.ending_stock += this_creation

    # bottle_produce(days) produces this type of bottle for "days" days.
    #   Updates self.total_cost, self.produced, self.total_production_days and self.total_creation.
    #   Requires:       0 < days < MINIMUM_PRODUCTION_DAYS
    #                   total_production_days <= self.__DAYS_IN_MONTH after it is updated.
    def bottle_produce(self, days):
        if (days < 0) or (0 < days < self.__MINIMUM_PRODUCTION_DAYS):
            raise ValueError(f"Bottle must be produced for at least "
                             f"{self.__MINIMUM_PRODUCTION_DAYS} (__MINIMUM_PRODUCTION_DAYS) days.")
        # Increase the current creation by the number of bottles produced, and increase total cost:
        self.total_cost += self.production_cost * days * self.production_capacity
        self.produced += self.production_capacity * days

        # Updating total production days and ensuring it is at most 28:
        self.total_production_days += days
        if self.total_production_days > self.__DAYS_IN_MONTH:
            raise ValueError(f"Trying to produce more than {self.__DAYS_IN_MONTH} days in this month.")

        # Updating the total creation:
        self.bottle_update_current_creation(self.production_capacity * days)

        if DEBUGGING:
            print(f"Producing bottle '{self.bottle_type}' for {days} days.")
            print(f"Current creation: {self.current_creation - self.production_capacity * days} "
                  f"==> {self.current_creation}.")
            print(f"Total cost: {self.total_cost - self.production_cost * days * self.production_capacity} "
                  f"==> {self.total_cost}.")
            print(f"Ending stock: {self.ending_stock - self.production_capacity * days} "
                  f"==> {self.ending_stock}.")

    # bottle_purchase(quantity) purchases this type of bottle in "quantity" amount.
    #   Updates self.total_cost, self.purchased and self.total_creation.
    #   Requires:       quantity > 0
    def bottle_purchase(self, quantity):
        if quantity < 0:
            raise ValueError(f"Purchase quantity must be positive.")
        # Increase the current creation by the number of bottles purchased, and increase total cost:
        self.purchased += quantity
        self.total_cost += self.purchase_cost * quantity

        # Updating the total creation:
        self.bottle_update_current_creation(quantity)

        if DEBUGGING:
            print(f"Purchasing bottle '{self.bottle_type}' in quantity of {quantity}.")
            print(f"Current creation: {self.current_creation - quantity} "
                  f"==> {self.current_creation}.")
            print(f"Total cost: {self.total_cost - self.purchase_cost * quantity} "
                  f"==> {self.total_cost}.")

    def bottle_meets_requirements(self):
        if self.current_creation < self.required_creation:
            if DEBUGGING:
                print(f"----------------------------------------------")
                print(f"Creation:               FALSE.")
                print(f"Current creation:       {self.current_creation}")
                print(f"Required creation:      {self.required_creation}")
                print(f"----------------------------------------------")
                print(f"Ending stock:           FALSE.")
                print(f"Current ending stock:   {self.ending_stock}")
                print(f"Required ending stock:  {self.required_ending_stock}")
                print(f"----------------------------------------------")
            return False
        if DEBUGGING:
            print(f"---------------------------")
            print(f"Requirements met. TRUE.")
            print(f"---------------------------")
        return True

    def __str__(self):
        bottle_info = f'''
        ==============================================================================
            Bottle type:        '{self.bottle_type}'
            Current creation:   {self.current_creation} (bottles this month)
            Required creation:  {self.required_creation} (bottles this month)
            
            Produced:           {self.produced} (bottles this month) for {self.total_production_days} days
            Purchased:          {self.purchased} (bottles this month)
            Total cost:         {self.total_cost}
            
            Initial stock:          {self.initial_stock} (bottles)
            Ending stock:           {self.ending_stock} (bottles)
            Required ending stock:  {self.required_ending_stock} (bottles)
        ==============================================================================
        '''
        return bottle_info
