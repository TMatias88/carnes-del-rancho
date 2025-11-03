from decimal import Decimal
from catalog.models import Product

CART_SESSION_ID = "cart"

class CartService:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, qty=1, override_qty=False):
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = {"qty": 0}
        if override_qty:
            self.cart[pid]["qty"] = qty
        else:
            self.cart[pid]["qty"] += qty
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        pids = self.cart.keys()
        products = Product.objects.filter(id__in=pids)
        for p in products:
            item = self.cart[str(p.id)]
            qty = item["qty"]
            total = p.price_crc * qty
            yield { "product": p, "qty": qty, "total": total }

    def summary(self):
        total = Decimal("0.00")
        count = 0
        for item in self:
            total += item["total"]
            count += item["qty"]
        return {"items_count": count, "total_crc": total}
