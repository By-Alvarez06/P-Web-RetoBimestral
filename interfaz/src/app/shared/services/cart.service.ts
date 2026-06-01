import { Injectable, computed, signal } from '@angular/core';
import { CartItem, Product } from '../models/product.model';

@Injectable({ providedIn: 'root' })
export class CartService {
  private readonly _items = signal<CartItem[]>([]);

  readonly items = this._items.asReadonly();

  readonly totalItems = computed(() =>
    this._items().reduce((s, i) => s + i.quantity, 0)
  );

  readonly subtotal = computed(() =>
    this._items().reduce((sum, item) => {
      const price = item.quantity >= item.product.minWholesaleQty
        ? item.product.wholesalePrice
        : item.product.retailPrice;
      return sum + price * item.quantity;
    }, 0)
  );

  readonly retailTotal = computed(() =>
    this._items().reduce((sum, item) =>
      sum + item.product.retailPrice * item.quantity, 0)
  );

  readonly savings = computed(() => this.retailTotal() - this.subtotal());

  readonly isEmpty = computed(() => this._items().length === 0);

  addToCart(product: Product, quantity = 1): void {
    this._items.update(items => {
      const existing = items.find(i => i.product.id === product.id);
      if (existing) {
        return items.map(i =>
          i.product.id === product.id
            ? { ...i, quantity: i.quantity + quantity }
            : i
        );
      }
      return [...items, { product, quantity }];
    });
  }

  removeFromCart(productId: number): void {
    this._items.update(items => items.filter(i => i.product.id !== productId));
  }

  updateQuantity(productId: number, quantity: number): void {
    if (quantity <= 0) {
      this.removeFromCart(productId);
      return;
    }
    this._items.update(items =>
      items.map(i => i.product.id === productId ? { ...i, quantity } : i)
    );
  }

  clearCart(): void {
    this._items.set([]);
  }

  getItemPrice(item: CartItem): number {
    return item.quantity >= item.product.minWholesaleQty
      ? item.product.wholesalePrice
      : item.product.retailPrice;
  }

  isWholesale(item: CartItem): boolean {
    return item.quantity >= item.product.minWholesaleQty;
  }
}
