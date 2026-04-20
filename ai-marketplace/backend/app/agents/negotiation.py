def negotiate(price, budget, priority):
    if priority == "cost":
        return budget

    elif priority == "speed":
        return price - 1

    else:
        return (price + budget) / 2