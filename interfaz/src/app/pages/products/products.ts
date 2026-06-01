import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProductCardComponent } from '../../shared/components/product-card/product-card';
import { ProductsService } from '../../shared/services/products.service';
import { Product } from '../../shared/models/product.model';

type SortKey = 'default' | 'price-asc' | 'price-desc' | 'rating' | 'name';

@Component({
  selector: 'app-products',
  imports: [RouterLink, ProductCardComponent, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './products.html',
  styleUrl: './products.scss',
})
export class ProductsComponent {
  private productsService = inject(ProductsService);

  readonly allProducts = this.productsService.products;
  readonly categories = this.productsService.categories;

  readonly searchQuery = signal('');
  readonly selectedCategory = signal('');
  readonly sortKey = signal<SortKey>('default');
  readonly maxPrice = signal(2000);
  readonly isSidebarOpen = signal(false);
  readonly addedProduct = signal<string | null>(null);

  readonly filteredProducts = computed(() => {
    let list = this.allProducts();
    const q = this.searchQuery().toLowerCase();
    const cat = this.selectedCategory();
    const max = this.maxPrice();
    const sort = this.sortKey();

    if (q) {
      list = list.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.tags.some(t => t.includes(q))
      );
    }
    if (cat) {
      list = list.filter(p => p.category === cat);
    }
    list = list.filter(p => p.retailPrice <= max);

    switch (sort) {
      case 'price-asc':  list = [...list].sort((a, b) => a.retailPrice - b.retailPrice); break;
      case 'price-desc': list = [...list].sort((a, b) => b.retailPrice - a.retailPrice); break;
      case 'rating':     list = [...list].sort((a, b) => b.rating - a.rating); break;
      case 'name':       list = [...list].sort((a, b) => a.name.localeCompare(b.name)); break;
    }
    return list;
  });

  selectCategory(id: string): void {
    this.selectedCategory.set(this.selectedCategory() === id ? '' : id);
  }

  clearFilters(): void {
    this.searchQuery.set('');
    this.selectedCategory.set('');
    this.sortKey.set('default');
    this.maxPrice.set(2000);
  }

  onProductAdded(product: Product): void {
    this.addedProduct.set(product.name);
    setTimeout(() => this.addedProduct.set(null), 2500);
  }

  toggleSidebar(): void {
    this.isSidebarOpen.update(v => !v);
  }

  readonly sortOptions: { value: SortKey; label: string }[] = [
    { value: 'default',    label: 'Relevancia' },
    { value: 'price-asc',  label: 'Precio: menor a mayor' },
    { value: 'price-desc', label: 'Precio: mayor a menor' },
    { value: 'rating',     label: 'Mejor valorados' },
    { value: 'name',       label: 'Nombre A–Z' },
  ];
}
