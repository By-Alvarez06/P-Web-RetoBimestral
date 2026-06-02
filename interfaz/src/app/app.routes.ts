import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent) },
  { path: 'productos', loadComponent: () => import('./pages/products/products').then(m => m.ProductsComponent) },
  { path: 'productos/:id', loadComponent: () => import('./pages/product-detail/product-detail').then(m => m.ProductDetailComponent) },
  { path: 'carrito', loadComponent: () => import('./pages/cart/cart').then(m => m.CartComponent) },
  { path: 'auth', loadComponent: () => import('./pages/auth/auth').then(m => m.AuthComponent) },
  {
    path: 'dashboard/vendedor',
    loadComponent: () => import('./dashboard/vendedor/vendedor-shell').then(m => m.VendedorShellComponent),
    children: [
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
      { path: 'inicio', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-inicio').then(m => m.VendedorInicioComponent) },
      { path: 'catalogo', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-catalogo').then(m => m.VendedorCatalogoComponent) },
      { path: 'pedido/nuevo', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-nuevo-pedido').then(m => m.VendedorNuevoPedidoComponent) },
      { path: 'pedidos', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-pedidos').then(m => m.VendedorPedidosComponent) },
      { path: 'comisiones', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-comisiones').then(m => m.VendedorComisionesComponent) },
      { path: 'puntos', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-puntos').then(m => m.VendedorPuntosComponent) },
      { path: 'recompensas', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-recompensas').then(m => m.VendedorRecompensasComponent) },
      { path: 'notificaciones', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-notificaciones').then(m => m.VendedorNotificacionesComponent) },
      { path: 'perfil', loadComponent: () => import('./dashboard/vendedor/pages/vendedor-perfil').then(m => m.VendedorPerfilComponent) },
    ]
  },
  {
    path: 'dashboard/comercializadora',
    loadComponent: () => import('./dashboard/comercializadora/com-shell').then(m => m.ComShellComponent),
    children: [
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
      { path: 'inicio', loadComponent: () => import('./dashboard/comercializadora/pages/com-inicio').then(m => m.ComInicioComponent) },
      { path: 'productos', loadComponent: () => import('./dashboard/comercializadora/pages/com-productos').then(m => m.ComProductosComponent) },
      { path: 'inventario', loadComponent: () => import('./dashboard/comercializadora/pages/com-inventario').then(m => m.ComInventarioComponent) },
      { path: 'pedidos', loadComponent: () => import('./dashboard/comercializadora/pages/com-pedidos').then(m => m.ComPedidosComponent) },
      { path: 'vendedores', loadComponent: () => import('./dashboard/comercializadora/pages/com-vendedores').then(m => m.ComVendedoresComponent) },
      { path: 'reportes', loadComponent: () => import('./dashboard/comercializadora/pages/com-reportes').then(m => m.ComReportesComponent) },
      { path: 'comisiones', loadComponent: () => import('./dashboard/comercializadora/pages/com-comisiones').then(m => m.ComComisionesComponent) },
      { path: 'auditoria', loadComponent: () => import('./dashboard/comercializadora/pages/com-auditoria').then(m => m.ComAuditoriaComponent) },
      { path: 'configuracion', loadComponent: () => import('./dashboard/comercializadora/pages/com-configuracion').then(m => m.ComConfiguracionComponent) },
    ]
  },
  { path: '**', redirectTo: '' },
];
