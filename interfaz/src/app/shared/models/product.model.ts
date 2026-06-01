export interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  image: string;
  retailPrice: number;
  wholesalePrice: number;
  minWholesaleQty: number;
  stock: number;
  rating: number;
  reviewCount: number;
  featured: boolean;
  badge?: string;
  sku: string;
  tags: string[];
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
  bg: string;
  productCount: number;
}
