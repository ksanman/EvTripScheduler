from decimal import Decimal, ROUND_HALF_UP

def RoundUp(value):
    return int(Decimal(value).quantize(Decimal('0'), rounding=ROUND_HALF_UP))