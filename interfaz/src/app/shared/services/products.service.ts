import { Injectable, signal } from '@angular/core';
import { Category, Product } from '../models/product.model';

const MOCK_PRODUCTS: Product[] = [
  {
    id: 1, name: 'Laptop HP Pavilion 15',
    description: 'Potente laptop para trabajo y estudio. Intel Core i7-1255U, 16 GB RAM DDR4, SSD NVMe 512 GB, pantalla FHD IPS 15.6", Windows 11 Home. Ideal para oficina y educación.',
    category: 'electronica',
    image: 'https://picsum.photos/seed/laptop-isben/600/400',
    retailPrice: 1299.99, wholesalePrice: 1049.00, minWholesaleQty: 3,
    stock: 45, rating: 4.7, reviewCount: 234, featured: true, badge: 'Más Vendido',
    sku: 'HP-PAV-15-001', tags: ['laptop', 'intel', 'windows']
  },
  {
    id: 2, name: 'Audífonos Sony WH-1000XM5',
    description: 'Cancelación de ruido líder en la industria. 30 horas de batería, conexión multipunto, micrófono HD. El estándar de oro en audio premium para profesionales.',
    category: 'electronica',
    image: 'https://picsum.photos/seed/headphones-isben/600/400',
    retailPrice: 349.99, wholesalePrice: 279.00, minWholesaleQty: 5,
    stock: 120, rating: 4.9, reviewCount: 567, featured: true, badge: 'Premium',
    sku: 'SONY-WH1000XM5', tags: ['audífonos', 'sony', 'bluetooth', 'noise-cancelling']
  },
  {
    id: 3, name: 'Taladro Percutor Bosch 650W',
    description: 'Taladro percutor profesional con 2 velocidades, mandril de 13 mm y maletín de transporte. Incluye set de 30 brocas HSS y puntas de torque.',
    category: 'herramientas',
    image: 'https://picsum.photos/seed/drill-isben/600/400',
    retailPrice: 89.99, wholesalePrice: 67.50, minWholesaleQty: 10,
    stock: 200, rating: 4.6, reviewCount: 189, featured: true,
    sku: 'BOSCH-TAL-650W', tags: ['taladro', 'bosch', 'profesional']
  },
  {
    id: 4, name: 'Set de Llaves Combinadas 14 pzas',
    description: 'Juego completo de llaves combinadas en acero cromado vanadio. Medidas 6-24 mm con estuche organizador de tela. Norma DIN 3113.',
    category: 'herramientas',
    image: 'https://picsum.photos/seed/wrench-isben/600/400',
    retailPrice: 45.99, wholesalePrice: 31.00, minWholesaleQty: 20,
    stock: 350, rating: 4.4, reviewCount: 98, featured: false,
    sku: 'LLAVES-14PZS', tags: ['llaves', 'herramientas manuales']
  },
  {
    id: 5, name: 'Aceite de Oliva Extra Virgen 1L',
    description: 'Aceite de oliva extra virgen de primera prensada en frío. Origen 100% España. Acidez máx 0.3%. Ideal para cocina gourmet y gastronomía.',
    category: 'alimentos',
    image: 'https://picsum.photos/seed/oliveoil-isben/600/400',
    retailPrice: 12.99, wholesalePrice: 8.20, minWholesaleQty: 48,
    stock: 1200, rating: 4.8, reviewCount: 445, featured: false,
    sku: 'ACEITE-OV-1L', tags: ['aceite', 'oliva', 'gourmet', 'importado']
  },
  {
    id: 6, name: 'Café Colombiano Premium 500g',
    description: 'Café de especialidad 100% colombiano, grano entero. Tostado medio, notas a chocolate y frutas cítricas. Origen Sierra Nevada. Finca directa.',
    category: 'alimentos',
    image: 'https://picsum.photos/seed/coffee-isben/600/400',
    retailPrice: 18.99, wholesalePrice: 13.00, minWholesaleQty: 24,
    stock: 800, rating: 4.9, reviewCount: 712, featured: true, badge: 'Orgánico',
    sku: 'CAFE-COL-500G', tags: ['café', 'colombia', 'orgánico', 'especialidad']
  },
  {
    id: 7, name: 'Detergente Concentrado Industrial 20L',
    description: 'Detergente líquido multiusos de alta concentración. Biodegradable, apto para uso industrial y comercial. Rinde hasta 200 L de producto listo.',
    category: 'limpieza',
    image: 'https://picsum.photos/seed/detergent-isben/600/400',
    retailPrice: 35.99, wholesalePrice: 23.50, minWholesaleQty: 12,
    stock: 500, rating: 4.3, reviewCount: 87, featured: false,
    sku: 'DET-IND-20L', tags: ['detergente', 'industrial', 'limpieza']
  },
  {
    id: 8, name: 'Desinfectante Hospitalario 4L',
    description: 'Desinfectante de amplio espectro, bactericida y viricida al 99.99%. Certificado DIGESA. Elimina SARS-CoV-2. Concentrado, rinde hasta 20 L.',
    category: 'limpieza',
    image: 'https://picsum.photos/seed/disinfectant-isben/600/400',
    retailPrice: 22.99, wholesalePrice: 14.75, minWholesaleQty: 24,
    stock: 750, rating: 4.5, reviewCount: 156, featured: false,
    sku: 'DESINF-HOS-4L', tags: ['desinfectante', 'bactericida', 'covid']
  },
  {
    id: 9, name: 'Resma Papel Bond A4 x500 hojas',
    description: 'Papel bond blanco 75 g/m² ISO brightness 92. Compatible con impresoras láser e inkjet. Libre de ácido. Caja x10 resmas disponible.',
    category: 'oficina',
    image: 'https://picsum.photos/seed/paper-isben/600/400',
    retailPrice: 8.99, wholesalePrice: 5.25, minWholesaleQty: 100,
    stock: 5000, rating: 4.2, reviewCount: 321, featured: false,
    sku: 'PAPEL-A4-500', tags: ['papel', 'impresión', 'bond']
  },
  {
    id: 10, name: 'Bolígrafos BIC Cristal x100 unid',
    description: 'Pack de 100 bolígrafos BIC Cristal punta media 1 mm. Escritura fluida y duradera. Surtido azul/negro/rojo. El clásico de oficina.',
    category: 'oficina',
    image: 'https://picsum.photos/seed/pens-isben/600/400',
    retailPrice: 25.99, wholesalePrice: 16.00, minWholesaleQty: 50,
    stock: 3000, rating: 4.7, reviewCount: 203, featured: true,
    sku: 'BIC-CRIST-100', tags: ['bolígrafos', 'bic', 'escritura']
  },
  {
    id: 11, name: 'Polo Corporativo 100% Algodón',
    description: 'Polo piqué 220 g/m² 100% algodón combed. Cuello reforzado, costuras dobles. Bordado o serigrafía personalizable hasta 4 colores. Tallas XS-3XL.',
    category: 'ropa',
    image: 'https://picsum.photos/seed/polo-isben/600/400',
    retailPrice: 29.99, wholesalePrice: 17.50, minWholesaleQty: 12,
    stock: 600, rating: 4.1, reviewCount: 65, featured: false,
    sku: 'POLO-CORP-001', tags: ['polo', 'ropa corporativa', 'algodón']
  },
  {
    id: 12, name: 'Zapatos de Seguridad Punta Acero',
    description: 'Calzado de seguridad industrial. Punta de acero ASTM F2413, suela antideslizante y antiestática, plantilla antiperforación. Certificado CE.',
    category: 'ropa',
    image: 'https://picsum.photos/seed/safeshoes-isben/600/400',
    retailPrice: 75.99, wholesalePrice: 54.00, minWholesaleQty: 6,
    stock: 200, rating: 4.6, reviewCount: 142, featured: false,
    sku: 'ZAP-SEG-ACERO', tags: ['zapatos', 'seguridad industrial', 'EPP']
  },
];

const MOCK_CATEGORIES: Category[] = [
  { id: 'electronica',  name: 'Electrónica',        icon: '💻', color: '#2563eb', bg: '#eff6ff', productCount: 45 },
  { id: 'herramientas', name: 'Herramientas',        icon: '🔧', color: '#d97706', bg: '#fffbeb', productCount: 38 },
  { id: 'alimentos',    name: 'Alimentos',            icon: '🛒', color: '#16a34a', bg: '#f0fdf4', productCount: 62 },
  { id: 'limpieza',     name: 'Limpieza',             icon: '🧴', color: '#0891b2', bg: '#ecfeff', productCount: 29 },
  { id: 'oficina',      name: 'Oficina',              icon: '📋', color: '#7c3aed', bg: '#f5f3ff', productCount: 54 },
  { id: 'ropa',         name: 'Ropa & Seguridad',    icon: '👕', color: '#db2777', bg: '#fdf2f8', productCount: 33 },
];

@Injectable({ providedIn: 'root' })
export class ProductsService {
  private readonly _products = signal<Product[]>(MOCK_PRODUCTS);
  private readonly _categories = signal<Category[]>(MOCK_CATEGORIES);

  readonly products = this._products.asReadonly();
  readonly categories = this._categories.asReadonly();

  getById(id: number): Product | undefined {
    return this._products().find(p => p.id === id);
  }

  getFeatured(): Product[] {
    return this._products().filter(p => p.featured);
  }

  getByCategory(categoryId: string): Product[] {
    return this._products().filter(p => p.category === categoryId);
  }

  search(query: string): Product[] {
    const q = query.toLowerCase();
    return this._products().filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.tags.some(t => t.includes(q))
    );
  }
}
