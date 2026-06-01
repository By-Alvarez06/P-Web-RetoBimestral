import { ChangeDetectionStrategy, Component, inject, input, output } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Product } from '../../models/product.model';
import { CartService } from '../../services/cart.service';

@Component({
  selector: 'app-product-card',
  imports: [RouterLink, TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './product-card.html',
  styleUrl: './product-card.scss',
})
export class ProductCardComponent {
  private cart = inject(CartService);

  readonly product = input.required<Product>();
  readonly added = output<Product>();

  addToCart(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.cart.addToCart(this.product());
    this.added.emit(this.product());
  }

  stars(rating: number): string[] {
    return Array.from({ length: 5 }, (_, i) =>
      i < Math.floor(rating) ? '★' : i < rating ? '½' : '☆'
    );
  }

  get discount(): number {
    const p = this.product();
    return Math.round((1 - p.wholesalePrice / p.retailPrice) * 100);
  }
}
