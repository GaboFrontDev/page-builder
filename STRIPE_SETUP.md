# Configuración de Stripe

## Pasos para configurar Stripe

### 1. Crear cuenta en Stripe
- Ve a [stripe.com](https://stripe.com) y crea una cuenta
- Activa tu cuenta completando la información requerida

### 2. Obtener las claves de API
1. Ve al Dashboard de Stripe
2. En el menú lateral, ve a "Developers" > "API keys"
3. Copia las claves:
   - **Publishable key** (pk_test_...)
   - **Secret key** (sk_test_...)

### 3. Crear los productos y precios
1. Ve a "Products" en el Dashboard de Stripe
2. Crea 3 productos:
   - **Básico** ($9.99/mes)
   - **Premium** ($19.99/mes)
   - **Enterprise** ($49.99/mes)
3. Para cada producto, crea un precio recurrente mensual
4. Copia los **Price IDs** (price_...)

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# Stripe API Keys
STRIPE_PUBLISHABLE_KEY=pk_test_tu_clave_aqui
STRIPE_SECRET_KEY=sk_test_tu_clave_aqui

# Stripe Price IDs
STRIPE_PRICE_BASIC=price_basic_monthly
STRIPE_PRICE_PREMIUM=price_premium_monthly
STRIPE_PRICE_ENTERPRISE=price_enterprise_monthly

# URLs de redirección
SUCCESS_URL=http://localhost:3000/dashboard?success=true
CANCEL_URL=http://localhost:3000/subscription?canceled=true
```

### 5. Configurar webhook (OPCIONAL - No es necesario)
Si quieres actualizaciones automáticas del estado de suscripción:

1. En el Dashboard de Stripe, ve a "Developers" > "Webhooks"
2. Crea un nuevo endpoint: `http://localhost:8000/api/subscription/webhook`
3. Selecciona estos eventos:
   - `customer.created`
   - `customer.subscription.created`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`
4. Copia el **Webhook signing secret** (whsec_...)
5. Agrégalo a tu `.env`:
   ```env
   STRIPE_WEBHOOK_SECRET=whsec_tu_secret_aqui
   ```

**Nota:** El sistema funciona perfectamente sin webhook. Cuando el usuario regresa después del pago, verificamos manualmente el estado de la suscripción.

### 6. Instalar dependencias
```bash
pip install stripe
```

### 7. Probar la integración
1. Inicia el servidor backend
2. Ve a `http://localhost:3000/subscription`
3. Prueba suscribirte con una tarjeta de prueba:
   - Número: `4242 4242 4242 4242`
   - Fecha: cualquier fecha futura
   - CVC: cualquier 3 dígitos

## Tarjetas de prueba de Stripe

### Tarjetas que funcionan:
- `4242 4242 4242 4242` - Pago exitoso
- `4000 0000 0000 0002` - Pago rechazado
- `4000 0000 0000 9995` - Pago rechazado (insuficiente)

### Códigos de error comunes:
- `card_declined` - Tarjeta rechazada
- `insufficient_funds` - Fondos insuficientes
- `expired_card` - Tarjeta expirada

## Estructura de archivos

```
backend/
├── config/
│   └── stripe_config.py      # Configuración de Stripe
├── routers/
│   └── subscription.py       # Endpoints de suscripción
├── subscription_manager/
│   ├── stripe_integration.py # Integración con Stripe
│   └── stripe_event_handler.py # Manejo de eventos
└── stripe_module/            # Módulo completo de Stripe
    ├── domain/
    ├── infrastructure/
    └── application/

frontend/
├── src/
│   ├── components/
│   │   ├── SubscriptionLanding.tsx    # Landing de suscripciones
│   │   └── dashboard/
│   │       └── SubscriptionStatus.tsx # Estado de suscripción
│   └── App.tsx                        # Rutas
```

## Flujo de suscripción

1. **Usuario visita `/subscription`**
   - Ve los planes disponibles
   - Selecciona un plan

2. **Usuario hace clic en "Suscribirse"**
   - Frontend llama a `/api/subscription/create-checkout-session`
   - Backend crea customer en Stripe (si no existe)
   - Backend crea checkout session
   - Usuario es redirigido a Stripe Checkout

3. **Usuario completa el pago**
   - Stripe procesa el pago
   - Usuario es redirigido a success_url con session_id

4. **Verificación manual del pago**
   - Frontend detecta session_id en URL
   - Llama a `/api/subscription/verify-payment/{session_id}`
   - Backend verifica el pago con Stripe
   - Actualiza `subscription_active = True`
   - Usuario tiene acceso a funcionalidades premium

**Alternativa con webhook:**
- Si configuras webhook, el estado se actualiza automáticamente
- Sin webhook, se verifica manualmente cuando el usuario regresa

## Troubleshooting

### Error: "No such price: price_..."
- Verifica que los Price IDs en `.env` coincidan con los de Stripe
- Asegúrate de que los precios estén activos en Stripe

### Error: "Invalid API key"
- Verifica que las claves de API estén correctas
- Asegúrate de usar claves de test para desarrollo

### Webhook no funciona
- Usa ngrok para exponer tu localhost: `ngrok http 8000`
- Actualiza la URL del webhook en Stripe
- Verifica que el webhook secret esté correcto

### Usuario no se actualiza después del pago
- Verifica que el webhook esté configurado correctamente
- Revisa los logs del backend para errores
- Asegúrate de que el customer_id coincida 