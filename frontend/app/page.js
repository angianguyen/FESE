'use client';

import StreamCreditApp from './demo';
import I18nTester from '../components/I18nTester';

export default function Home() {
  return (
    <>
      <StreamCreditApp />
      {/* Debug panel - remove in production */}
      {process.env.NODE_ENV === 'development' && <I18nTester />}
    </>
  );
}
