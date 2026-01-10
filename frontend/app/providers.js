'use client';

import { Web3Provider } from '../context/Web3Context';
import { I18nextProvider } from 'react-i18next';
import i18n from '../lib/i18n';
import { useEffect, useState } from 'react';

export function Providers({ children }) {
  const [i18nInitialized, setI18nInitialized] = useState(false);

  useEffect(() => {
    // Wait for i18n to initialize
    if (i18n.isInitialized) {
      setI18nInitialized(true);
    } else {
      i18n.on('initialized', () => {
        setI18nInitialized(true);
      });
    }
  }, []);

  // Show loading or children without translations until i18n is ready
  if (!i18nInitialized) {
    return (
      <Web3Provider>
        <div className="flex items-center justify-center min-h-screen bg-gray-900">
          <div className="text-white">Loading...</div>
        </div>
      </Web3Provider>
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
