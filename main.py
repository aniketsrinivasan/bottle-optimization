from bottle_type import BottleMonth

sample_predictions = [1000, 1800, 2000, 1500]


def main():
    bottle_A = BottleMonth(bottle_type="A",
                           current_stock=800,
                           production_capacity=50,
                           production_cost=2*20,
                           purchase_cost=0.1)
    print(bottle_A)

    bottle_A.bottle_set_requirements(1000, 1800)
    print(bottle_A)

    bottle_A.bottle_produce(10)
    print(bottle_A)

    bottle_A.bottle_purchase(500)
    print(bottle_A)

    bottle_A.bottle_produce(12)
    print(bottle_A)

    bottle_A.bottle_meets_requirements()

    bottle_A_1 = BottleMonth(bottle_type="A",
                             current_stock=bottle_A.ending_stock,
                             production_capacity=50,
                             production_cost=2 * 20,
                             purchase_cost=0.1)
    bottle_A_1.bottle_set_requirements(1800, 2000)
    print(bottle_A_1)


if __name__ == "__main__":
    main()
