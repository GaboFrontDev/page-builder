import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNotification } from '../contexts/NotificationContext';

interface Plan {
  id: string;
  name: string;
  price: number;
  currency: string;
  interval: string;
  features: string[];
  popular?: boolean;
  stripe_price_id: string;
}

const SubscriptionLanding: React.FC = () => {
  const { user } = useAuth();
  const { showNotification } = useNotification();
  const [loading, setLoading] = useState<string | null>(null);

  const plans: Plan[] = [
    {
      id: 'basic',
      name: 'Básico',
      price: 9.99,
      currency: 'USD',
      interval: 'mes',
      stripe_price_id: 'price_basic_monthly',
      features: [
        'Hasta 3 páginas',
        'Subdominios personalizados',
        'Templates básicos',
        'Soporte por email',
        'Deployment automático'
      ]
    },
    {
      id: 'premium',
      name: 'Premium',
      price: 19.99,
      currency: 'USD',
      interval: 'mes',
      stripe_price_id: 'price_premium_monthly',
      popular: true,
      features: [
        'Páginas ilimitadas',
        'Subdominios personalizados',
        'Templates premium',
        'Soporte prioritario',
        'Deployment automático',
        'Analytics básicos',
        'Dominio personalizado'
      ]
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      price: 49.99,
      currency: 'USD',
      interval: 'mes',
      stripe_price_id: 'price_enterprise_monthly',
      features: [
        'Todo de Premium',
        'Soporte 24/7',
        'Analytics avanzados',
        'Integraciones personalizadas',
        'API access',
        'White-label',
        'Onboarding dedicado'
      ]
    }
  ];

  const handleSubscribe = async (plan: Plan) => {
    if (!user) {
      showNotification('error', 'Debes iniciar sesión para suscribirte');
      return;
    }

    setLoading(plan.id);
    try {
      // Aquí iría la lógica para crear checkout session con Stripe
      const response = await fetch('/api/subscription/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          price_id: plan.stripe_price_id,
          plan_type: plan.id
        })
      });

      if (!response.ok) {
        throw new Error('Error al crear sesión de pago');
      }

      const { session_url } = await response.json();
      window.location.href = session_url;
    } catch (error) {
      console.error('Error:', error);
      showNotification('error', 'Error al procesar la suscripción');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Header */}
      <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg border-b border-gray-200/50 dark:border-gray-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <svg className="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">Landing Builder</h1>
            </div>
            <div className="flex items-center space-x-4">
              {user ? (
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  Hola, {user.username}
                </span>
              ) : (
                <a href="/login" className="btn btn-outline">
                  Iniciar Sesión
                </a>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Elige tu Plan
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Construye landing pages profesionales con nuestros planes flexibles. 
            Desde proyectos pequeños hasta empresas, tenemos el plan perfecto para ti.
          </p>
        </div>

        {/* Plans Grid */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border-2 ${
                plan.popular 
                  ? 'border-blue-500 dark:border-blue-400 scale-105' 
                  : 'border-gray-200 dark:border-gray-700'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-4 py-2 rounded-full text-sm font-semibold">
                    Más Popular
                  </span>
                </div>
              )}

              <div className="p-8">
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {plan.name}
                  </h3>
                  <div className="mb-4">
                    <span className="text-4xl font-bold text-gray-900 dark:text-white">
                      ${plan.price}
                    </span>
                    <span className="text-gray-600 dark:text-gray-300">/{plan.interval}</span>
                  </div>
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-center">
                      <svg className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  onClick={() => handleSubscribe(plan)}
                  disabled={loading === plan.id}
                  className={`w-full btn ${
                    plan.popular 
                      ? 'btn-primary' 
                      : 'btn-outline'
                  } ${loading === plan.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {loading === plan.id ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Procesando...
                    </div>
                  ) : (
                    'Suscribirse'
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* FAQ Section */}
        <div className="mt-24 max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            Preguntas Frecuentes
          </h2>
          <div className="space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                ¿Puedo cambiar de plan en cualquier momento?
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Sí, puedes actualizar o cambiar tu plan en cualquier momento desde tu dashboard.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                ¿Hay un período de prueba?
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Ofrecemos 7 días de prueba gratuita en todos nuestros planes.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                ¿Puedo cancelar mi suscripción?
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Sí, puedes cancelar tu suscripción en cualquier momento sin penalizaciones.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriptionLanding; 