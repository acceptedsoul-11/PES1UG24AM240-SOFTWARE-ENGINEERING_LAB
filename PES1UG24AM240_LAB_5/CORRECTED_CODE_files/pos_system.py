"""Retail point-of-sale system."""
import re
import secrets
import logging

# Global state
price_list = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}
sales_total = 0.0
receipt_lines = []


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Calculate a cart total, record the receipt, and update sales."""
    global sales_total

    if receipts is None:
        receipts = []

    subtotal = 0.0

    for item, quantity in cart_items:
        if item not in price_list:
            logging.warning("Unknown item: %s", item)
            continue

        if not isinstance(quantity, int) or quantity < 0:
            logging.warning("Invalid quantity for %s: %s", item, quantity)
            continue

        subtotal += price_list[item] * quantity

    if not isinstance(tax_rate, (int, float)) or not 0 <= tax_rate <= 1:
        raise ValueError("Tax rate must be between 0 and 1.")

    total = subtotal * (1 + tax_rate)
    receipts.append(total)
    sales_total += total

    receipt_number = secrets.randbelow(9000) + 1000
    receipt_lines.append(
        f"Receipt #{receipt_number} total={total:.2f}"
    )

    return total


def apply_promo_code(code_str):
    """Apply a supported promotional discount to total sales."""
    match = re.fullmatch(
        r"\s*total\s*([*-])\s*(\d+(?:\.\d+)?)\s*",
        code_str,
    )

    if not match:
        raise ValueError("Invalid promo code format.")

    operator, value_text = match.groups()
    value = float(value_text)

    if operator == "*":
        if not 0 <= value <= 1:
            raise ValueError(
                "Discount multiplier must be between 0 and 1."
            )
        return sales_total * value

    if value < 0:
        raise ValueError("Discount amount cannot be negative.")

    return max(0.0, sales_total - value)


def update_stock(item, qty):
    """Validate and report a stock update request."""
    if item not in price_list:
        logging.warning("Cannot update stock: unknown item %s", item)
        return

    if not isinstance(qty, int) or qty < 0:
        logging.warning("Invalid stock quantity: %s", qty)
        return

    print("Stock update requested for", item, "by", qty)


def save_receipt_log(file="pos_log.txt"):
    """Append receipt lines to the receipt log file."""
    try:
        with open(file, "a", encoding="utf-8") as receipt_file:
            for line in receipt_lines:
                receipt_file.write(line + "\n")
    except OSError as error:
        logging.error("Could not save receipt log: %s", error)


def print_sales():
    """Print the cumulative sales total."""
    print(f"Sales so far: {sales_total:.2f}")


def main():
    """Run the sample checkout transactions and promotions."""
    print("Bill 1:", process_checkout([("pen", 3), ("notebook", 2)]))
    print("Bill 2:", process_checkout([("bag", 1), ("laptop", 1)]))
    print("Bill 3:", process_checkout([("bottle", -4)]))
    print("Bill 4:", process_checkout([("pen", "2")], tax_rate=-1))
    update_stock("laptop", 5)
    print("After promo:", apply_promo_code("total * 0.9"))
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    print("After your promo:", apply_promo_code(code))
    save_receipt_log()
    print_sales()


main()
