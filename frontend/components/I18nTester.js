'use client';

import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';

export default function I18nTester() {
  const { t, i18n } = useTranslation();

  useEffect(() => {
    console.log('🌍 I18n Tester Mounted');
    console.log('Current language:', i18n.language);
    console.log('Is initialized:', i18n.isInitialized);
    
    const handleLanguageChange = (lng) => {
      console.log('🔄 Language changed to:', lng);
    };
    
    i18n.on('languageChanged', handleLanguageChange);
    
    return () => {
      i18n.off('languageChanged', handleLanguageChange);
    };
  }, [i18n]);

  return (
    <div className="fixed bottom-4 left-4 bg-slate-900 border border-cyan-500/30 rounded-lg p-4 shadow-xl z-50 max-w-xs">
      <div className="text-xs font-mono space-y-2">
        <div className="text-cyan-400 font-bold mb-2">🌍 i18n Debug Panel</div>
        
        <div>
          <div className="text-slate-500">Current Language:</div>
          <div className="text-white font-bold">{i18n.language}</div>
        </div>
        
        <div>
          <div className="text-slate-500">Test Translation:</div>
          <div className="text-emerald-400">{t('app.title')}</div>
        </div>
        
        <div>
          <div className="text-slate-500">Wallet Button:</div>
          <div className="text-emerald-400">{t('wallet.connect')}</div>
        </div>
        
        <div className="pt-2 border-t border-slate-700">
          <div className="text-slate-500 mb-1">Quick Switch:</div>
          <div className="flex gap-1">
            <button
              onClick={() => i18n.changeLanguage('en')}
              className={`px-2 py-1 rounded text-[10px] ${
                i18n.language === 'en' ? 'bg-cyan-500 text-white' : 'bg-slate-700 text-slate-300'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => i18n.changeLanguage('vi')}
              className={`px-2 py-1 rounded text-[10px] ${
                i18n.language === 'vi' ? 'bg-cyan-500 text-white' : 'bg-slate-700 text-slate-300'
              }`}
            >
              VI
            </button>
            <button
              onClick={() => i18n.changeLanguage('ko')}
              className={`px-2 py-1 rounded text-[10px] ${
                i18n.language === 'ko' ? 'bg-cyan-500 text-white' : 'bg-slate-700 text-slate-300'
              }`}
            >
              KO
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
