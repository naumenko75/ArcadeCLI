def count_divisors(n):
    """
    Counts the number of divisors of a given positive integer.
    """
    if n <= 0:
        return 0

    count = 0
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            count += 1
            if i != n // i:
                count += 1
    return count


def find_number_with_most_divisors(start, end):
    """
    Finds the number with the most divisors in the given range.
    Returns a tuple (number, divisor_count).
    """
    if start > end:
        start, end = end, start

    max_divisors = 0
    best_number = start

    for num in range(start, end + 1):
        divisors_count = count_divisors(num)
        if divisors_count > max_divisors:
            max_divisors = divisors_count
            best_number = num

    return best_number, max_divisors


def divisors_mode(args):
    """
    Handles the divisors command with different numbers of arguments.
    """
    if len(args) == 0:
        print("Usage: divisors [number] OR divisors [start] [end]")
        return

    try:
        if len(args) == 1:
            # Single argument: count divisors of the given number
            number = int(args[0])
            if number <= 0:
                print("Please enter a positive integer.")
                return

            divisor_count = count_divisors(number)
            print(f"Number {number} has {divisor_count} divisors.")

        elif len(args) == 2:
            # Two arguments: find number with most divisors in range
            start = int(args[0])
            end = int(args[1])

            if start <= 0 or end <= 0:
                print("Please enter positive integers for the range.")
                return

            number, divisor_count = find_number_with_most_divisors(start, end)
            print(f"Number with most divisors in range [{start}, {end}]: {number} ({divisor_count} divisors)")

        else:
            print("Too many arguments. Usage: divisors [number] OR divisors [start] [end]")

    except ValueError:
        print("Please enter valid integers.")
    except Exception as e:
        print(f"Error: {e}")
