def pick_random_with_weights(options):
    # tally up the total roll by summing all the weight values
    total = sum( weight for key, weight in options )
    roll = random.randint(0, total-1)

    result = None
    # loop through each id/weight item
    for key, weight in options:
        # deduct this weighting from the roll
        roll -= weight
        # if this deduction drops us to zero, then this is our result
        if roll < 0:
            result = key
            break

    return result