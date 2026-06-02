import { ChangeDetectionStrategy, Component, inject, signal, computed } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DashboardService } from '../../../shared/services/dashboard.service';
import type { Product } from '../../../shared/services/dashboard.service';

interface OrderLine { product: Product; quantity: number; }

@Component({
  selector: 'app-vendedor-nuevo-pedido',
  imports: [RouterLink, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-nuevo-pedido.html',
  styles: [],
})
export class VendedorNuevoPedidoComponent {
  private dash = inject(DashboardService);
  private router = inject(Router);

  readonly products = this.dash.products().filter(p => p.active);
  readonly customer = signal('');
  readonly lines = signal<OrderLine[]>([]);
  readonly submitted = signal(false);

  readonly subtotal = computed(() =>
    this.lines().reduce((s, l) => s + l.product.wholesalePrice * l.quantity, 0)
  );
  readonly commission = computed(() => this.subtotal() * 0.1);

  addLine(productId: string): void {
    const id = Number(productId);
    const product = this.products.find(p => p.id === id);
    if (!product) return;
    this.lines.update(ls => {
      const exists = ls.find(l => l.product.id === id);
      if (exists) return ls.map(l => l.product.id === id ? { ...l, quantity: l.quantity + 1 } : l);
      return [...ls, { product, quantity: 1 }];
    });
  }

  removeLine(id: number): void {
    this.lines.update(ls => ls.filter(l => l.product.id !== id));
  }

  updateQty(id: number, val: string): void {
    const q = parseInt(val, 10);
    if (q <= 0) { this.removeLine(id); return; }
    this.lines.update(ls => ls.map(l => l.product.id === id ? { ...l, quantity: q } : l));
  }

  submit(): void {
    this.submitted.set(true);
    setTimeout(() => this.router.navigate(['/dashboard/vendedor/pedidos']), 1500);
  }
}
