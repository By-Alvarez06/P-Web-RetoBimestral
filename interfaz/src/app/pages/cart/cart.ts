import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CartService } from '../../shared/services/cart.service';
import { CartItem } from '../../shared/models/product.model';

@Component({
  selector: 'app-cart',
  imports: [RouterLink, TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './cart.html',
  styleUrl: './cart.scss',
})
export class CartComponent {
  readonly cart = inject(CartService);

  readonly TAX_RATE = 0.18;

  get tax(): number {
    return this.cart.subtotal() * this.TAX_RATE;
  }

  get total(): number {
    return this.cart.subtotal() + this.tax;
  }

  updateQty(item: CartItem, value: string): void {
    const n = parseInt(value, 10);
    if (!isNaN(n)) this.cart.updateQuantity(item.product.id, n);
  }

  decrement(item: CartItem): void {
    this.cart.updateQuantity(item.product.id, item.quantity - 1);
  }

  increment(item: CartItem): void {
    if (item.quantity < item.product.stock) {
      this.cart.updateQuantity(item.product.id, item.quantity + 1);
    }
  }

  remove(item: CartItem): void {
    this.cart.removeFromCart(item.product.id);
  }
}
