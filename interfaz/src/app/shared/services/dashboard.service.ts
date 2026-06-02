import { Injectable, signal } from '@angular/core';

export type OrderStatus = 'pendiente' | 'confirmado' | 'en_proceso' | 'entregado' | 'cancelado';
export type StockStatus = 'normal' | 'bajo' | 'critico';
export type CommissionStatus = 'pendiente' | 'pagada' | 'liquidada';

export interface Order {
  id: string; date: string; customer: string; store: string;
  seller: string; items: number; total: number;
  commission: number; status: OrderStatus;
}

export interface Product {
  id: number; code: string; name: string; category: string;
  wholesalePrice: number; stock: number; stockStatus: StockStatus;
  active: boolean; lastUpdate: string;
}

export interface Commission {
  id: string; order: string; date: string; seller: string;
  amount: number; status: CommissionStatus;
}

export interface InventoryAlert {
  product: string; code: string; stock: number;
  minStock: number; status: StockStatus; category: string;
}

export interface AuditEntry {
  id: string; user: string; action: string;
  module: string; date: string; ip: string;
}

export interface Campaign {
  id: string; name: string; factor: number;
  start: string; end: string; active: boolean;
  products: string[]; description: string;
}

export interface Notification {
  id: string; type: 'pedido' | 'inventario' | 'campana' | 'sistema';
  title: string; message: string; date: string; read: boolean;
}

export interface Seller {
  id: string; name: string; ruc: string; email: string;
  phone: string; store: string; totalSales: number;
  commission: number; points: number; active: boolean;
}

export interface PointTransaction {
  id: string; date: string; order: string; points: number;
  type: 'ganado' | 'canjeado'; description: string;
}

const ORDERS: Order[] = [
  { id:'PED-2026-001', date:'2026-05-20', customer:'Tienda El Progreso', store:'Sucursal Centro', seller:'Carlos Ramírez', items:5, total:450.00, commission:45.00, status:'entregado' },
  { id:'PED-2026-002', date:'2026-05-22', customer:'Comercial Norte Cía.', store:'Local Principal', seller:'María López', items:12, total:1200.00, commission:120.00, status:'confirmado' },
  { id:'PED-2026-003', date:'2026-05-24', customer:'Distribuidora Sur', store:'Bodega Central', seller:'Carlos Ramírez', items:8, total:890.00, commission:89.00, status:'entregado' },
  { id:'PED-2026-004', date:'2026-05-26', customer:'Mini Market 24h', store:'Av. Universitaria', seller:'Juan Torres', items:3, total:215.00, commission:21.50, status:'en_proceso' },
  { id:'PED-2026-005', date:'2026-05-27', customer:'Ferretería El Maestro', store:'Local 2', seller:'Ana García', items:20, total:2340.00, commission:234.00, status:'pendiente' },
  { id:'PED-2026-006', date:'2026-05-28', customer:'Bazar Central', store:'Zona Rosa', seller:'Carlos Ramírez', items:6, total:560.00, commission:56.00, status:'entregado' },
  { id:'PED-2026-007', date:'2026-05-29', customer:'Librería Moderna', store:'Centro Histórico', seller:'María López', items:4, total:320.00, commission:32.00, status:'cancelado' },
  { id:'PED-2026-008', date:'2026-05-30', customer:'Supermercado Loja', store:'Suc. Norte', seller:'Juan Torres', items:15, total:1850.00, commission:185.00, status:'confirmado' },
];

const PRODUCTS: Product[] = [
  { id:1, code:'HP-PAV-15-001', name:'Laptop HP Pavilion 15', category:'Electrónica', wholesalePrice:1049.00, stock:45, stockStatus:'normal', active:true, lastUpdate:'2026-05-30' },
  { id:2, code:'SONY-WH1000XM5', name:'Audífonos Sony WH-1000XM5', category:'Electrónica', wholesalePrice:279.00, stock:8, stockStatus:'bajo', active:true, lastUpdate:'2026-05-28' },
  { id:3, code:'BOSCH-TAL-650W', name:'Taladro Percutor Bosch 650W', category:'Herramientas', wholesalePrice:67.50, stock:200, stockStatus:'normal', active:true, lastUpdate:'2026-05-25' },
  { id:4, code:'LLAVES-14PZS', name:'Set de Llaves Combinadas 14 pzas', category:'Herramientas', wholesalePrice:31.00, stock:3, stockStatus:'critico', active:true, lastUpdate:'2026-05-20' },
  { id:5, code:'ACEITE-OV-1L', name:'Aceite de Oliva Extra Virgen 1L', category:'Alimentos', wholesalePrice:8.20, stock:1200, stockStatus:'normal', active:true, lastUpdate:'2026-05-30' },
  { id:6, code:'CAFE-COL-500G', name:'Café Colombiano Premium 500g', category:'Alimentos', wholesalePrice:13.00, stock:12, stockStatus:'bajo', active:true, lastUpdate:'2026-05-29' },
  { id:7, code:'DET-IND-20L', name:'Detergente Concentrado Industrial 20L', category:'Limpieza', wholesalePrice:23.50, stock:500, stockStatus:'normal', active:true, lastUpdate:'2026-05-27' },
  { id:8, code:'DESINF-HOS-4L', name:'Desinfectante Hospitalario 4L', category:'Limpieza', wholesalePrice:14.75, stock:5, stockStatus:'critico', active:false, lastUpdate:'2026-05-18' },
  { id:9, code:'PAPEL-A4-500', name:'Resma Papel Bond A4 x500', category:'Oficina', wholesalePrice:5.25, stock:5000, stockStatus:'normal', active:true, lastUpdate:'2026-05-30' },
  { id:10, code:'BIC-CRIST-100', name:'Bolígrafos BIC Cristal x100', category:'Oficina', wholesalePrice:16.00, stock:3000, stockStatus:'normal', active:true, lastUpdate:'2026-05-26' },
];

const COMMISSIONS: Commission[] = [
  { id:'COM-001', order:'PED-2026-001', date:'2026-05-20', seller:'Carlos Ramírez', amount:45.00, status:'pagada' },
  { id:'COM-002', order:'PED-2026-002', date:'2026-05-22', seller:'María López', amount:120.00, status:'pagada' },
  { id:'COM-003', order:'PED-2026-003', date:'2026-05-24', seller:'Carlos Ramírez', amount:89.00, status:'pendiente' },
  { id:'COM-004', order:'PED-2026-004', date:'2026-05-26', seller:'Juan Torres', amount:21.50, status:'pendiente' },
  { id:'COM-005', order:'PED-2026-005', date:'2026-05-27', seller:'Ana García', amount:234.00, status:'pendiente' },
  { id:'COM-006', order:'PED-2026-006', date:'2026-05-28', seller:'Carlos Ramírez', amount:56.00, status:'pendiente' },
  { id:'COM-007', order:'PED-2026-008', date:'2026-05-30', seller:'Juan Torres', amount:185.00, status:'pendiente' },
];

const INVENTORY_ALERTS: InventoryAlert[] = [
  { product:'Audífonos Sony WH-1000XM5', code:'SONY-WH1000XM5', stock:8, minStock:15, status:'bajo', category:'Electrónica' },
  { product:'Set de Llaves Combinadas 14 pzas', code:'LLAVES-14PZS', stock:3, minStock:20, status:'critico', category:'Herramientas' },
  { product:'Café Colombiano Premium 500g', code:'CAFE-COL-500G', stock:12, minStock:24, status:'bajo', category:'Alimentos' },
  { product:'Desinfectante Hospitalario 4L', code:'DESINF-HOS-4L', stock:5, minStock:24, status:'critico', category:'Limpieza' },
  { product:'Zapatos de Seguridad Punta Acero', code:'ZAP-SEG-ACERO', stock:4, minStock:10, status:'critico', category:'Ropa & Seguridad' },
];

const AUDIT_LOG: AuditEntry[] = [
  { id:'AUD-001', user:'Admin General', action:'Actualizó precio de Laptop HP Pavilion', module:'Productos', date:'2026-06-01 09:14', ip:'192.168.1.10' },
  { id:'AUD-002', user:'Carlos Ramírez', action:'Registró pedido PED-2026-008', module:'Pedidos', date:'2026-05-30 14:22', ip:'192.168.1.25' },
  { id:'AUD-003', user:'Admin General', action:'Creó campaña Bonificación Junio', module:'Campañas', date:'2026-05-30 11:00', ip:'192.168.1.10' },
  { id:'AUD-004', user:'María López', action:'Registró pedido PED-2026-007', module:'Pedidos', date:'2026-05-29 16:45', ip:'192.168.1.30' },
  { id:'AUD-005', user:'Admin General', action:'Liquidó comisiones de mayo', module:'Comisiones', date:'2026-05-29 10:00', ip:'192.168.1.10' },
  { id:'AUD-006', user:'Juan Torres', action:'Actualizó perfil de usuario', module:'Usuarios', date:'2026-05-28 08:30', ip:'192.168.1.40' },
  { id:'AUD-007', user:'Admin General', action:'Desactivó producto DESINF-HOS-4L', module:'Productos', date:'2026-05-28 09:05', ip:'192.168.1.10' },
  { id:'AUD-008', user:'Ana García', action:'Ingresó al sistema', module:'Autenticación', date:'2026-05-27 07:55', ip:'192.168.1.50' },
];

const CAMPAIGNS: Campaign[] = [
  {
    id:'CAMP-001', name:'Bonificación Junio', factor:1.5,
    start:'2026-06-01', end:'2026-06-30', active:true,
    products:['Laptop HP Pavilion 15','Audífonos Sony WH-1000XM5','Taladro Percutor Bosch'],
    description:'Duplica tus puntos en productos de electrónica y herramientas durante todo junio.'
  },
  {
    id:'CAMP-002', name:'Campaña Limpieza x2', factor:2.0,
    start:'2026-06-01', end:'2026-06-15', active:true,
    products:['Detergente Concentrado Industrial','Desinfectante Hospitalario'],
    description:'Doble puntos en todos los productos de la categoría Limpieza.'
  },
  {
    id:'CAMP-003', name:'Alimentos Premium', factor:1.2,
    start:'2026-05-01', end:'2026-05-31', active:false,
    products:['Aceite de Oliva Extra Virgen','Café Colombiano Premium'],
    description:'Puntos adicionales en productos de la categoría Alimentos. Campaña finalizada.'
  },
];

const NOTIFICATIONS: Notification[] = [
  { id:'N001', type:'pedido', title:'Pedido PED-2026-008 confirmado', message:'Tu pedido fue confirmado y está en proceso de preparación.', date:'2026-05-30 15:00', read:false },
  { id:'N002', type:'campana', title:'Nueva campaña: Bonificación Junio', message:'Empieza el 1 de junio. Gana 1.5x puntos en electrónica.', date:'2026-05-30 11:05', read:false },
  { id:'N003', type:'inventario', title:'Stock crítico: Llaves Combinadas', message:'Quedan solo 3 unidades del código LLAVES-14PZS.', date:'2026-05-29 09:00', read:false },
  { id:'N004', type:'pedido', title:'Pedido PED-2026-006 entregado', message:'El pedido fue marcado como entregado exitosamente.', date:'2026-05-28 17:30', read:true },
  { id:'N005', type:'sistema', title:'Mantenimiento programado', message:'El sistema estará en mantenimiento el domingo 02/06 de 2:00 a 4:00 AM.', date:'2026-05-28 10:00', read:true },
  { id:'N006', type:'pedido', title:'Comisión acreditada', message:'Se acreditó tu comisión de $45.00 por el pedido PED-2026-001.', date:'2026-05-27 12:00', read:true },
];

const SELLERS: Seller[] = [
  { id:'S001', name:'Carlos Ramírez', ruc:'1768123456001', email:'c.ramirez@mail.com', phone:'+593 984 000 111', store:'Tienda Central Ramírez', totalSales:2140.00, commission:214.00, points:1240, active:true },
  { id:'S002', name:'María López', ruc:'1768234567001', email:'m.lopez@mail.com', phone:'+593 984 000 222', store:'Distribuidora López', totalSales:1520.00, commission:152.00, points:890, active:true },
  { id:'S003', name:'Juan Torres', ruc:'1768345678001', email:'j.torres@mail.com', phone:'+593 984 000 333', store:'Mini Market Torres', totalSales:2065.00, commission:206.50, points:1100, active:true },
  { id:'S004', name:'Ana García', ruc:'1768456789001', email:'a.garcia@mail.com', phone:'+593 984 000 444', store:'Ferretería García', totalSales:2340.00, commission:234.00, points:1450, active:true },
  { id:'S005', name:'Pedro Salas', ruc:'1768567890001', email:'p.salas@mail.com', phone:'+593 984 000 555', store:'Bodega Salas', totalSales:0, commission:0, points:50, active:false },
];

const POINT_TRANSACTIONS: PointTransaction[] = [
  { id:'PT001', date:'2026-05-28', order:'PED-2026-006', points:56, type:'ganado', description:'Puntos por venta' },
  { id:'PT002', date:'2026-05-24', order:'PED-2026-003', points:89, type:'ganado', description:'Puntos por venta' },
  { id:'PT003', date:'2026-05-20', order:'PED-2026-001', points:45, type:'ganado', description:'Puntos por venta' },
  { id:'PT004', date:'2026-05-15', order:'-', points:-200, type:'canjeado', description:'Canje por producto incentivo' },
  { id:'PT005', date:'2026-05-10', order:'PED-2026-00X', points:120, type:'ganado', description:'Campaña Alimentos Premium' },
];

@Injectable({ providedIn: 'root' })
export class DashboardService {
  readonly orders = signal<Order[]>(ORDERS);
  readonly products = signal<Product[]>(PRODUCTS);
  readonly commissions = signal<Commission[]>(COMMISSIONS);
  readonly inventoryAlerts = signal<InventoryAlert[]>(INVENTORY_ALERTS);
  readonly auditLog = signal<AuditEntry[]>(AUDIT_LOG);
  readonly campaigns = signal<Campaign[]>(CAMPAIGNS);
  readonly notifications = signal<Notification[]>(NOTIFICATIONS);
  readonly sellers = signal<Seller[]>(SELLERS);
  readonly pointTransactions = signal<PointTransaction[]>(POINT_TRANSACTIONS);

  readonly unreadNotifications = this.notifications()
    .filter(n => !n.read).length;

  markNotificationRead(id: string): void {
    this.notifications.update(list =>
      list.map(n => n.id === id ? { ...n, read: true } : n)
    );
  }

  markAllRead(): void {
    this.notifications.update(list => list.map(n => ({ ...n, read: true })));
  }

  getOrdersByStatus(status: OrderStatus): Order[] {
    return this.orders().filter(o => o.status === status);
  }
}
