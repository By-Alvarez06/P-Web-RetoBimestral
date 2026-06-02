import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ProductCardComponent } from '../../shared/components/product-card/product-card';
import { ProductsService } from '../../shared/services/products.service';
import { Product } from '../../shared/models/product.model';

@Component({
  selector: 'app-home',
  imports: [RouterLink, ProductCardComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class HomeComponent {
  private productsService = inject(ProductsService);

  readonly featuredProducts = this.productsService.getFeatured();
  readonly categories = this.productsService.categories;
  readonly addedProduct = signal<string | null>(null);

  onProductAdded(product: Product): void {
    this.addedProduct.set(product.name);
    setTimeout(() => this.addedProduct.set(null), 2500);
  }

  readonly stats = [
    { value: '500+',   label: 'Productos' },
    { value: '60+',    label: 'Categorías' },
    { value: '1,200+', label: 'Clientes' },
    { value: '15',     label: 'Años de experiencia' },
  ];

  readonly features = [
    {
      title: 'Precios Mayoristas',
      desc: 'Accede a precios exclusivos de mayorista desde el mínimo de unidades indicado. Ahorra hasta un 40% frente al precio minorista.'
    },
    {
      title: 'Entrega Rápida',
      desc: 'Despacho en 24-48 horas para Loja y provincia. Cobertura nacional con las mejores empresas de courier del Ecuador.'
    },
    {
      title: 'Calidad Garantizada',
      desc: 'Todos nuestros productos cuentan con garantía de fábrica y certificados de calidad. Devolución sin complicaciones en 30 días.'
    },
    {
      title: 'Atención Personalizada',
      desc: 'Asesor comercial dedicado para cuentas mayoristas. Te ayudamos a encontrar el mejor precio para tu volumen de compra.'
    },
  ];

  readonly testimonials = [
    {
      name: 'María González',
      role: 'Gerente de Compras',
      company: 'Distribuidora Norte Cía. Ltda.',
      text: 'ISBEN Solutions ha transformado nuestra cadena de suministro. Los precios mayoristas son competitivos y la entrega siempre puntual. Llevamos 3 años siendo clientes.',
      rating: 5,
      avatar: 'MG'
    },
    {
      name: 'Carlos Mendoza',
      role: 'Propietario',
      company: 'Ferretería El Maestro',
      text: 'La variedad de productos en herramientas es increíble. He podido expandir mi inventario sin necesidad de múltiples proveedores. El servicio post-venta es excelente.',
      rating: 5,
      avatar: 'CM'
    },
    {
      name: 'Ana Torres',
      role: 'Administradora',
      company: 'Restaurantes Unidos de Loja',
      text: 'Compramos insumos mensualmente y siempre llegan a tiempo. Los precios mayoristas nos han permitido reducir costos de manera significativa.',
      rating: 5,
      avatar: 'AT'
    },
  ];
}
