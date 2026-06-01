import { ChangeDetectionStrategy, Component, computed, inject, input, signal } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CartService } from '../../shared/services/cart.service';
import { ProductsService } from '../../shared/services/products.service';

@Component({
  selector: 'app-product-detail',
  imports: [RouterLink, TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './product-detail.html',
  styleUrl: './product-detail.scss',
})
export class ProductDetailComponent {
  private productsService = inject(ProductsService);
  private cart = inject(CartService);

  readonly id = input<string>('');

  readonly product = computed(() => {
    const id = Number(this.id());
    return this.productsService.getById(id) ?? null;
  });

  readonly relatedProducts = computed(() => {
    const p = this.product();
    if (!p) return [];
    return this.productsService.getByCategory(p.category)
      .filter(r => r.id !== p.id)
      .slice(0, 4);
  });

  readonly quantity = signal(1);
  readonly activeTab = signal<'descripcion' | 'especificaciones' | 'envio'>('descripcion');
  readonly addedToCart = signal(false);

  readonly currentPrice = computed(() => {
    const p = this.product();
    if (!p) return 0;
    return this.quantity() >= p.minWholesaleQty ? p.wholesalePrice : p.retailPrice;
  });

  readonly isWholesale = computed(() => {
    const p = this.product();
    if (!p) return false;
    return this.quantity() >= p.minWholesaleQty;
  });

  readonly savings = computed(() => {
    const p = this.product();
    if (!p) return 0;
    return (p.retailPrice - p.wholesalePrice) * this.quantity();
  });

  decrement(): void {
    if (this.quantity() > 1) this.quantity.update(v => v - 1);
  }

  increment(): void {
    const p = this.product();
    if (p && this.quantity() < p.stock) this.quantity.update(v => v + 1);
  }

  setQuantity(value: string): void {
    const n = parseInt(value, 10);
    const p = this.product();
    if (!p || isNaN(n) || n < 1) return;
    this.quantity.set(Math.min(n, p.stock));
  }

  addToCart(): void {
    const p = this.product();
    if (!p) return;
    this.cart.addToCart(p, this.quantity());
    this.addedToCart.set(true);
    setTimeout(() => this.addedToCart.set(false), 2500);
  }

  discountPct(retail: number, wholesale: number): number {
    return Math.round((1 - wholesale / retail) * 100);
  }

  stars(rating: number): string[] {
    return Array.from({ length: 5 }, (_, i) =>
      i < Math.floor(rating) ? '★' : i < rating ? '½' : '☆'
    );
  }
}
