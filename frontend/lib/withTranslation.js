'use client';

import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

/**
 * HOC to force component re-render when language changes
 * Wraps any component to make it reactive to i18n changes
 */
export function withTranslation(Component) {
  return function TranslatedComponent(props) {
    const { i18n } = useTranslation();
    const [, forceUpdate] = useState({});

    useEffect(() => {
      const handleLanguageChange = () => {
        console.log('🔄 Language changed, forcing re-render');
        forceUpdate({});
      };

      i18n.on('languageChanged', handleLanguageChange);
      
      return () => {
        i18n.off('languageChanged', handleLanguageChange);
      };
    }, [i18n]);

    return <Component {...props} key={i18n.language} />;
  };
}

/**
 * Hook to force component re-render when language changes
 */
export function useLanguageChange() {
  const { i18n } = useTranslation();
  const [language, setLanguage] = useState(i18n.language);

  useEffect(() => {
    const handleLanguageChange = (lng) => {
      console.log('🌍 Language changed to:', lng);
      setLanguage(lng);
    };

    i18n.on('languageChanged', handleLanguageChange);
    
    return () => {
      i18n.off('languageChanged', handleLanguageChange);
    };
  }, [i18n]);

  return language;
}
