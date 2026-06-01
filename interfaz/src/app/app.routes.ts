import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home').then(m => m.HomeComponent),
  },
  {
    path: 'productos',
    loadComponent: () => import('./pages/products/products').then(m => m.ProductsComponent),
  },
  {
    path: 'productos/:id',
    loadComponent: () => import('./pages/product-detail/product-detail').then(m => m.ProductDetailComponent),
  },
  {
    path: 'carrito',
    loadComponent: () => import('./pages/cart/cart').then(m => m.CartComponent),
  },
  {
    path: 'auth',
    loadComponent: () => import('./pages/auth/auth').then(m => m.AuthComponent),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
