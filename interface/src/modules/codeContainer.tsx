import React, { useState } from 'react';
import { writeText } from '@tauri-apps/plugin-clipboard-manager';
import { CustomClipboardButton } from '../utils/formatUtils';

interface CodeContainerProps {
  code: string;
}

export const CodeContainer: React.FC<CodeContainerProps> = ({ code }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await writeText(code).
      catch((err) => console.error(err));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ position: 'relative', border: '1px solid #ddd', borderRadius: '5px', padding: '10px', backgroundColor: '#f5f5f5' }}>
      <pre style={{ margin: 0 }}>
        <code>{code}</code>
      </pre>
      <CustomClipboardButton onClick={handleCopy} copied={copied} />
    </div>
  );
};
