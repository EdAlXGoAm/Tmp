import React, { useState } from 'react';
import { writeText } from '@tauri-apps/plugin-clipboard-manager';
import { CustomClipboardButton, MiniFloatingButton } from '../utils/buttonUtils';

interface CodeContainerProps {
  code: string;
  copyable?: boolean;
  expandable?: boolean; // if true, the code container will have a max height of 200px and will show a scrollbar
}

export const CodeContainer: React.FC<CodeContainerProps> = ({ code, copyable = false, expandable = false }) => {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const handleCopy = async () => {
    await writeText(code).
      catch((err) => console.error(err));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const expandCode = () => {
    setExpanded(!expanded);
  }

  return (
    <>
      {expandable && code!=='' && (
        <MiniFloatingButton onClick={() => expandCode()} boolean_var={expanded} text1={'Collapse'} text2={'Expand'} />
      )}
      <div style={{
        position: 'relative',
        border: '1px solid #ddd',
        borderRadius: '5px',
        padding: '10px',
        paddingTop: expandable ? (code==='' ? '10' : '25px') : '10px',
        backgroundColor: '#f5f5f5',
        maxHeight: expandable ? expanded ? '600px' : '75px' : 'auto',
        overflowY: expandable ? 'auto' : 'visible'
      }}>
        <pre style={{ margin: 0 }}>
          <code>{code}</code>
        </pre>
        {copyable && <CustomClipboardButton onClick={handleCopy} copied={copied} />}
      </div>
    </>
  );
};
