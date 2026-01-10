'use client';

import { Web3Provider } from '../context/Web3Context';
import { I18nextProvider } from 'react-i18next';
import i18n from '../lib/i18n';
import { useEffect, useState } from 'react';

export function Providers({ children }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Ensure i18n is fully initialized before rendering
    const initI18n = async () => {
      if (!i18n.isInitialized) {
        await i18n.init();
      }
      setMounted(true);
    };
    
    initI18n();
  }, []);

  // Don't render until i18n is ready AND client-side mounted
  if (!mounted) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  return (
    <I18nextProvider i18n={i18n}>
      <Web3Provider>
        {children}
      </Web3Provider>
    </I18nextProvider>
  );
}
