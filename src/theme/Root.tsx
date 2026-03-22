import React from 'react';
import type {PropsWithChildren} from '@docusaurus/types';
import ChatWidget from '@site/src/components/ChatWidget';

// Default implementation, that you can customize
// If you want to customize the Footer, use the Footer instead.
export default function Root({children}: PropsWithChildren): JSX.Element {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}